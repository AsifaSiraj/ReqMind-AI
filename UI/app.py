import gradio as gr

# Temporary placeholder function
# Member 2 will replace this with actual API connection
def analyze_requirements(text):
    if not text.strip():
        return {"error": "Please enter requirement text."}
    
    return {
        "message": "Backend connection successful.",
        "preview_input_length": len(text),
        "status": "Awaiting AI integration"
    }

# Define a high-end theme for a premium, warm feel
theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Plus Jakarta Sans"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill="linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%)",
    block_background_fill="rgba(255, 255, 255, 0.6)",
    block_label_text_weight="600",
    block_title_text_weight="700",
    block_border_width="1px",
    block_border_color="rgba(0, 0, 0, 0.05)",
    button_primary_background_fill="linear-gradient(90deg, #4338ca 0%, #6366f1 100%)",
    button_primary_background_fill_hover="linear-gradient(90deg, #3730a3 0%, #4338ca 100%)",
    button_primary_text_color="white",
    input_background_fill="rgba(255, 255, 255, 0.9)",
    input_border_color="rgba(0, 0, 0, 0.1)",
)


# Advanced CSS for a Classy, Warm, and Light Interface
advanced_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

:root {
    --brand-gradient: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
    --glass-bg: rgba(255, 255, 255, 0.5);
    --glass-border: rgba(255, 255, 255, 0.3);
    --text-main: #1e293b;
    --text-muted: #475569;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-15px) rotate(1deg); }
}

@keyframes orbit {
    from { transform: rotate(0deg) translateX(45px) rotate(0deg); }
    to { transform: rotate(360deg) translateX(45px) rotate(-360deg); }
}

@keyframes shine {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

.animate-up { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Fix for Textbox Interaction & Readability */
#input-terminal textarea {
    background: white !important;
    color: var(--text-main) !important;
    border: 1px solid rgba(0,0,0,0.05) !important;
    z-index: 10 !important;
    position: relative !important;
}

.glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid var(--glass-border);
    border-radius: 28px;
    padding: 2.5rem;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.05);
}

.hero-section {
    padding: 5rem 2rem 6rem;
    text-align: center;
}

.hero-title {
    font-size: clamp(3.5rem, 8vw, 5.5rem) !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #1e1b4b 20%, #4338ca 50%, #1e1b4b 80%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 5s linear infinite;
    letter-spacing: -0.04em;
    margin-bottom: 0.75rem !important;
}

.ai-orb-container {
    perspective: 1200px;
    margin-bottom: 2.5rem;
    display: flex;
    justify-content: center;
}

.ai-orb {
    width: 140px;
    height: 140px;
    background: radial-gradient(circle at 35% 35%, #6366f1, #3730a3);
    border-radius: 50%;
    position: relative;
    box-shadow: 0 15px 45px rgba(67, 56, 202, 0.2);
    animation: float 5s ease-in-out infinite;
}

.ai-orb::before {
    content: '';
    position: absolute;
    inset: -15px;
    border: 1.5px solid rgba(67, 56, 202, 0.15);
    border-radius: 50%;
    animation: orbit 10s linear infinite;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2.5rem;
    margin: 4rem 0;
}

.premium-card {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.04);
    padding: 3rem;
    border-radius: 24px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.03);
}

.premium-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 25px 50px -12px rgba(67, 56, 202, 0.08);
    border-color: rgba(67, 56, 202, 0.2);
}

.analyze-btn-outer {
    background: var(--brand-gradient);
    padding: 1.5px;
    border-radius: 16px;
    transition: all 0.3s ease;
}

.analyze-btn-outer:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 30px -10px rgba(67, 56, 202, 0.3);
}

.analyze-btn {
    background: white !important;
    color: #3730a3 !important;
    border: none !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    height: 3.75rem !important;
    width: 100% !important;
    border-radius: 14px !important;
}

.footer-v2 {
    background: rgba(255, 255, 255, 0.3);
    padding: 5rem 2rem;
    text-align: center;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}

/* Global Markdown Overrides for Dark Text on Light BG */
.prose, .gr-markdown {
    color: var(--text-main) !important;
}
.prose h3, .gr-markdown h3 {
    color: #1e1b4b !important;
    font-weight: 700 !important;
}
"""

with gr.Blocks(
    title="ReqMind AI | Competition Edition"
) as app:

    # Hero Section with Floating AI Orb
    with gr.Column(elem_classes="hero-section"):
        gr.HTML("""
        <div class="ai-orb-container animate-up">
            <div class="ai-orb"></div>
        </div>
        <div class="animate-up">
            <div class="hero-badge" style="background: rgba(67, 56, 202, 0.05); color: #4338ca; padding: 0.6rem 1.2rem; border-radius: 100px; font-weight: 700; font-size: 0.85rem; display: inline-block; margin-bottom: 1.5rem; border: 1px solid rgba(67, 56, 202, 0.1);">
                PREMIUM ENGINEERING SUITE
            </div>
            <h1 class="hero-title">ReqMind AI</h1>
            <p style="color: #475569; font-size: 1.4rem; max-width: 800px; margin: 0 auto 3rem; font-weight: 400; line-height: 1.6;">
                Intelligent Requirement Engineering for professional software teams. 
                Clarify complexity and accelerate your development lifecycle.
            </p>
        </div>
        """)

    # Authentic Value Props
    with gr.Row(elem_classes="feature-grid animate-up"):
        gr.HTML("""
        <div class="premium-card">
            <div style="font-size: 2.8rem; margin-bottom: 2rem;">🔍</div>
            <h3 style="color: #1e1b4b; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Semantic Audit</h3>
            <p style="color: #64748b; line-height: 1.6; font-size: 1.05rem;">Deep linguistic parsing to extract functional requirements and entity relationships with technical accuracy.</p>
        </div>
        <div class="premium-card">
            <div style="font-size: 2.8rem; margin-bottom: 2rem;">⚡</div>
            <h3 style="color: #1e1b4b; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Logic Verification</h3>
            <p style="color: #64748b; line-height: 1.6; font-size: 1.05rem;">Heuristic checks designed to identify potential gaps or contradictions in complex documentation streams.</p>
        </div>
        <div class="premium-card">
            <div style="font-size: 2.8rem; margin-bottom: 2rem;">💎</div>
            <h3 style="color: #1e1b4b; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">Standardization</h3>
            <p style="color: #64748b; line-height: 1.6; font-size: 1.05rem;">Converts raw stakeholder input into structured, enterprise-ready data formats for downstream engineering.</p>
        </div>
        """)

    # Main Workspace
    with gr.Row(elem_classes="animate-up"):
        with gr.Column(scale=5):
            with gr.Column(elem_classes="glass-panel"):
                gr.Markdown("### 🛠️ Requirement Input")
                input_text = gr.Textbox(
                    lines=16,
                    placeholder="Provide your software requirements or user stories here...",
                    label="Input Terminal",
                    show_label=False,
                    elem_id="input-terminal"
                )
                with gr.Column(elem_classes="analyze-btn-outer"):
                    analyze_btn = gr.Button(
                        "ANALYZE PROJECT SCOPE",
                        variant="primary",
                        elem_classes="analyze-btn"
                    )

        with gr.Column(scale=4):
            with gr.Column(elem_classes="glass-panel"):
                gr.Markdown("### 📊 Engineering Insights")
                output_json = gr.JSON(
                    label="Structured Analysis",
                    show_label=False
                )
                gr.Markdown("""
                <div style="margin-top: 1.5rem; padding: 1.2rem; background: rgba(67, 56, 202, 0.04); border-radius: 16px; border: 1px solid rgba(67, 56, 202, 0.08);">
                    <p style="color: #4338ca; font-size: 0.95rem; margin: 0; display: flex; align-items: center; gap: 0.6rem;">
                        <span style="display: inline-block; width: 10px; height: 10px; background: #4338ca; border-radius: 50%;"></span>
                        <strong>Status:</strong> Intelligence Engine Active
                    </p>
                </div>
                """, sanitize_html=False)

    # Global Footer
    with gr.Column(elem_classes="footer-v2"):
        gr.HTML("""
        <div style="display: flex; justify-content: center; gap: 4rem; opacity: 0.7; margin-bottom: 3.5rem;">
            <div style="text-align: center;">
                <p style="color: #1e1b4b; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.2rem;">HEC HACKATHON</p>
                <p style="color: #64748b; font-size: 0.8rem; font-weight: 500;">OFFICIAL ENTRY 2026</p>
            </div>
            <div style="text-align: center;">
                <p style="color: #1e1b4b; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.2rem;">COHORT 02</p>
                <p style="color: #64748b; font-size: 0.8rem; font-weight: 500;">GROUP 26</p>
            </div>
        </div>
        <p style="color: #94a3b8; font-size: 0.85rem; letter-spacing: 0.05em; font-weight: 500;">© 2026 REQMIND AI. ALL RIGHTS RESERVED.</p>
        """)

    analyze_btn.click(
        analyze_requirements,
        inputs=input_text,
        outputs=output_json
    )

if __name__ == "__main__":
    app.launch(theme=theme, css=advanced_css)


