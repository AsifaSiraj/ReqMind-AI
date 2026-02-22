import gradio as gr
import os, json, tempfile
from groq import Groq
import pdfplumber
from analyzer import analyze_requirements, compare_documents
from pdf_generator import generate_pdf

try:
    from docx import Document as DocxDocument
    DOCX_OK = True
except ImportError:
    DOCX_OK = False


# ── Text extraction ───────────────────────────────────────────────────────────
def extract_text(file_path: str) -> str:
    if not file_path:
        return ""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text.strip()
    elif ext == ".docx" and DOCX_OK:
        doc = DocxDocument(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif ext in (".txt", ".md"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    return ""


# ── Main analyze handler ──────────────────────────────────────────────────────
def analyze(text_input, file_input):
    source = ""
    if file_input is not None:
        source = extract_text(file_input)
        if not source:
            return None, None, "❌ Could not extract text from file."
    elif text_input and text_input.strip():
        source = text_input.strip()
    else:
        return None, None, "⚠️ Please paste requirements OR upload a file."

    if len(source) < 30:
        return None, None, "⚠️ Text too short. Please provide more detailed requirements."

    try:
        result = analyze_requirements(source)
    except json.JSONDecodeError:
        return None, None, "❌ AI returned invalid response. Please try again."
    except Exception as e:
        return None, None, f"❌ Error: {str(e)}"

    try:
        pdf_path = generate_pdf(result)
    except Exception as e:
        pdf_path = None

    qs      = result.get("quality_score", {})
    score   = qs.get("overall", "N/A")
    pi      = result.get("project_info", {})
    ptype   = pi.get("detected_type", "N/A")
    comp    = pi.get("complexity", "N/A")
    summ    = result.get("summary", {})
    quality = summ.get("overall_quality", "N/A")

    status = (
        f"✅ **Analysis Complete!**  |  "
        f"🏷️ Type: **{ptype}**  |  "
        f"📊 Score: **{score}/100**  |  "
        f"📦 Complexity: **{comp}**  |  "
        f"Overall: **{quality}**"
    )
    return result, pdf_path, status


# ── Version comparison handler ────────────────────────────────────────────────
def compare(old_file, new_file, old_text, new_text):
    old = extract_text(old_file) if old_file else old_text.strip()
    new = extract_text(new_file) if new_file else new_text.strip()

    if not old or not new:
        return None, "⚠️ Please provide both Old and New documents."

    try:
        result = compare_documents(old, new)
        return result, "✅ Comparison complete!"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


# ── Score card HTML ───────────────────────────────────────────────────────────
def score_html(analysis):
    if not analysis:
        return ""
    qs    = analysis.get("quality_score", {})
    pi    = analysis.get("project_info", {})
    summ  = analysis.get("summary", {})
    score = qs.get("overall", 0)
    color = "#16a34a" if score >= 70 else ("#d97706" if score >= 40 else "#dc2626")

    def bar(val):
        c = "#16a34a" if val >= 70 else ("#d97706" if val >= 40 else "#dc2626")
        return f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
          <div style="flex:1;background:#e2e8f0;border-radius:4px;height:8px;">
            <div style="width:{val}%;background:{c};border-radius:4px;height:8px;"></div>
          </div>
          <span style="font-size:0.78rem;font-weight:700;color:{c};width:32px;">{val}</span>
        </div>"""

    sc_rows = "".join(
        f"<tr><td style='padding:4px 8px;color:#475569;font-size:0.82rem;'>{k}</td>"
        f"<td style='padding:4px 8px;'>{bar(v)}</td></tr>"
        for k, v in [
            ("Clarity",       qs.get("clarity",0)),
            ("Completeness",  qs.get("completeness",0)),
            ("Consistency",   qs.get("consistency",0)),
            ("Testability",   qs.get("testability",0)),
        ]
    )

    risks      = analysis.get("risks", [])
    high_risks = [r for r in risks if r.get("severity","").lower() == "high"]
    scope_cnt  = len(analysis.get("scope_creep", []))

    return f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">

      <!-- Score Circle -->
      <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:1.25rem;text-align:center;">
        <div style="width:90px;height:90px;border-radius:50%;background:conic-gradient({color} {score*3.6}deg,#e2e8f0 0deg);
             display:flex;align-items:center;justify-content:center;margin:0 auto 0.75rem;position:relative;">
          <div style="width:70px;height:70px;border-radius:50%;background:white;
               display:flex;align-items:center;justify-content:center;">
            <span style="font-size:1.3rem;font-weight:800;color:{color};">{score}</span>
          </div>
        </div>
        <p style="font-weight:700;color:#1e293b;margin:0 0 0.2rem;">Quality Score</p>
        <p style="color:#64748b;font-size:0.78rem;margin:0;">{qs.get('breakdown','')[:80]}...</p>
      </div>

      <!-- Score Breakdown -->
      <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:1.25rem;">
        <p style="font-weight:700;color:#1e293b;margin:0 0 0.75rem;font-size:0.9rem;">Score Breakdown</p>
        <table style="width:100%;">{sc_rows}</table>
      </div>

      <!-- Project Info -->
      <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:1.25rem;">
        <p style="font-weight:700;color:#1e293b;margin:0 0 0.75rem;font-size:0.9rem;">🏷️ Project Info</p>
        <p style="color:#64748b;font-size:0.82rem;margin:0 0 0.3rem;"><b>Type:</b> {pi.get('detected_type','N/A')}</p>
        <p style="color:#64748b;font-size:0.82rem;margin:0 0 0.3rem;"><b>Complexity:</b> {pi.get('complexity','N/A')}</p>
        <p style="color:#64748b;font-size:0.82rem;margin:0;"><b>Reason:</b> {pi.get('complexity_reason','N/A')}</p>
      </div>

      <!-- Alerts -->
      <div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:1.25rem;">
        <p style="font-weight:700;color:#1e293b;margin:0 0 0.75rem;font-size:0.9rem;">🚨 Key Alerts</p>
        <div style="background:#fee2e2;border-radius:8px;padding:0.5rem 0.75rem;margin-bottom:0.4rem;">
          <span style="color:#dc2626;font-size:0.82rem;font-weight:600;">
            🔴 {len(high_risks)} High Severity Risk(s)
          </span>
        </div>
        <div style="background:#fef3c7;border-radius:8px;padding:0.5rem 0.75rem;margin-bottom:0.4rem;">
          <span style="color:#d97706;font-size:0.82rem;font-weight:600;">
            ⚠️ {len(analysis.get('ambiguities',[]))} Ambiguit(ies) Found
          </span>
        </div>
        <div style="background:#dbeafe;border-radius:8px;padding:0.5rem 0.75rem;">
          <span style="color:#2563eb;font-size:0.82rem;font-weight:600;">
            🎯 {scope_cnt} Scope Creep Warning(s)
          </span>
        </div>
      </div>

    </div>
    """


# ── UI ────────────────────────────────────────────────────────────────────────
with gr.Blocks(
    title="ReqMind AI",
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="purple",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
    )
) as app:

    # ── Header ──
    gr.HTML("""
    <div style="
        background:linear-gradient(135deg,#4338ca,#6366f1);
        padding:1.2rem 2rem;
        display:flex; align-items:center; justify-content:space-between;
        border-radius:12px; margin-bottom:1rem;
    ">
      <div style="display:flex;align-items:center;gap:0.75rem;">
        <span style="font-size:2rem;">🧠</span>
        <div>
          <h1 style="color:white;font-size:1.6rem;font-weight:800;margin:0;">ReqMind AI</h1>
          <p style="color:rgba(255,255,255,0.75);font-size:0.8rem;margin:0;">AI-Powered Software Requirements Analyzer</p>
        </div>
      </div>
      <span style="background:rgba(255,255,255,0.15);color:white;font-size:0.72rem;
            font-weight:700;letter-spacing:0.08em;padding:0.4rem 1rem;
            border-radius:100px;border:1px solid rgba(255,255,255,0.25);">
        HEC HACKATHON 2026 · GROUP 26
      </span>
    </div>
    """)

    with gr.Tabs():

        # ════════════════════════════════════════
        # TAB 1 — ANALYZER
        # ════════════════════════════════════════
        with gr.Tab("⚡ Analyzer"):

            with gr.Row():
                # LEFT — Input
                with gr.Column(scale=1):
                    gr.Markdown("### 📂 Upload Document")
                    file_input = gr.File(
                        label="Upload PDF / DOCX / TXT",
                        file_types=[".pdf", ".docx", ".txt", ".md"],
                    )
                    gr.HTML('<div style="text-align:center;color:#94a3b8;font-size:0.82rem;margin:0.25rem 0;">— OR paste text below —</div>')
                    gr.Markdown("### 📝 Paste Requirements")
                    text_input = gr.Textbox(
                        lines=14,
                        placeholder=(
                            "Paste your software requirements here...\n\n"
                            "Example:\n"
                            "1. The system shall allow users to register with email and password.\n"
                            "2. Users can login and logout from the system.\n"
                            "3. The system must send order confirmation emails.\n"
                            "4. Admin can manage products and users.\n"
                            "5. The system should be fast and secure.\n"
                            "6. Payment should be handled somehow.\n"
                            "7. In future we may add AI recommendations.\n"
                            "8. System may include reporting module later."
                        ),
                        label="Requirements Text",
                        show_label=False,
                    )
                    analyze_btn = gr.Button("🔍 Analyze", variant="primary", size="lg")
                    status_box  = gr.Markdown("")

                # RIGHT — Output
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 Quality Dashboard")
                    score_card = gr.HTML("")

                    with gr.Tabs():
                        with gr.Tab("📋 Full JSON"):
                            output_json = gr.JSON(label="Full Analysis", show_label=False)
                        with gr.Tab("📥 Download PDF"):
                            gr.Markdown("Click below to download your full analysis report:")
                            pdf_output = gr.File(label="PDF Report", interactive=False)

        # ════════════════════════════════════════
        # TAB 2 — VERSION COMPARISON
        # ════════════════════════════════════════
        with gr.Tab("🔄 Version Compare"):
            gr.Markdown("### Compare Old vs New Requirements Document")
            gr.Markdown("Upload or paste both versions — AI will detect what changed, what was added/removed, and if scope shifted.")

            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 📄 Old Version")
                    old_file = gr.File(label="Upload Old Doc", file_types=[".pdf",".docx",".txt"])
                    old_text = gr.Textbox(lines=8, placeholder="Or paste old requirements here...", label="Old Text", show_label=False)

                with gr.Column():
                    gr.Markdown("#### 📄 New Version")
                    new_file = gr.File(label="Upload New Doc", file_types=[".pdf",".docx",".txt"])
                    new_text = gr.Textbox(lines=8, placeholder="Or paste new requirements here...", label="New Text", show_label=False)

            compare_btn    = gr.Button("🔄 Compare Documents", variant="primary", size="lg")
            compare_status = gr.Markdown("")
            compare_output = gr.JSON(label="Comparison Result", show_label=False)

        # ════════════════════════════════════════
        # TAB 3 — ABOUT
        # ════════════════════════════════════════
        with gr.Tab("📖 Explore"):
            gr.HTML("""
            <div style="max-width:820px;margin:0 auto;padding:1.5rem 0;">

              <div style="background:linear-gradient(135deg,#4338ca,#6366f1);border-radius:16px;
                          padding:2.5rem;text-align:center;margin-bottom:1.5rem;color:white;">
                <div style="font-size:3rem;margin-bottom:0.75rem;">🧠</div>
                <h2 style="font-size:2rem;font-weight:800;margin:0 0 0.5rem;">ReqMind AI</h2>
                <p style="opacity:0.85;margin:0;line-height:1.6;">
                  AI-powered Software Requirements Analyzer.<br>
                  Upload your document — get structured, professional insights instantly.
                </p>
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">🔍</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Functional Extraction</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Identifies requirements with priority & category.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">📊</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Quality Score</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">0-100 score with clarity, completeness & testability.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">🚨</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Risk Analysis</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Security, scalability, performance & privacy risks.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">🎯</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Scope Creep Detector</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Flags "may include" / "future" style statements.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">💬</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Stakeholder Questions</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Questions per role: Client, Dev, Tester, PM.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">🔄</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Version Comparison</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Compare old vs new docs — see what changed.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">🏷️</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Project Type Detection</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Auto-detects E-commerce, LMS, FinTech, etc.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">📦</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">Complexity Estimation</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Small / Medium / Large project sizing.</div>
                </div>
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;">
                  <div style="font-size:1.4rem;margin-bottom:0.4rem;">📥</div>
                  <div style="font-weight:700;color:#1e293b;margin-bottom:0.2rem;font-size:0.88rem;">PDF Report Export</div>
                  <div style="color:#64748b;font-size:0.78rem;line-height:1.5;">Professional colored PDF with all sections.</div>
                </div>
              </div>

              <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;text-align:center;">
                <p style="color:#64748b;font-size:0.8rem;font-weight:600;margin-bottom:0.75rem;">POWERED BY</p>
                <div style="display:flex;gap:0.75rem;justify-content:center;flex-wrap:wrap;">
                  <span style="background:#ede9fe;color:#4338ca;font-size:0.82rem;font-weight:600;padding:0.35rem 1rem;border-radius:100px;">🤖 Groq API</span>
                  <span style="background:#ede9fe;color:#4338ca;font-size:0.82rem;font-weight:600;padding:0.35rem 1rem;border-radius:100px;">🦙 LLaMA 3.3 70B</span>
                  <span style="background:#ede9fe;color:#4338ca;font-size:0.82rem;font-weight:600;padding:0.35rem 1rem;border-radius:100px;">🎨 Gradio</span>
                  <span style="background:#ede9fe;color:#4338ca;font-size:0.82rem;font-weight:600;padding:0.35rem 1rem;border-radius:100px;">🤗 HuggingFace</span>
                </div>
              </div>

              <p style="text-align:center;color:#94a3b8;font-size:0.78rem;margin-top:1rem;">
                HEC Hackathon 2026 Official Entry · Cohort 02 · Group 26
              </p>
            </div>
            """)

    # ── Events ──
    def full_analyze(text_input, file_input):
        result, pdf_path, status = analyze(text_input, file_input)
        html = score_html(result) if result else ""
        return result, pdf_path, status, html

    analyze_btn.click(
        fn=full_analyze,
        inputs=[text_input, file_input],
        outputs=[output_json, pdf_output, status_box, score_card]
    )

    compare_btn.click(
        fn=compare,
        inputs=[old_file, new_file, old_text, new_text],
        outputs=[compare_output, compare_status]
    )

if __name__ == "__main__":
    app.launch()