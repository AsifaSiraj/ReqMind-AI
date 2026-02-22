import tempfile, os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

INDIGO       = colors.HexColor("#4338ca")
INDIGO_LIGHT = colors.HexColor("#ede9fe")
PURPLE       = colors.HexColor("#6366f1")
SLATE_DARK   = colors.HexColor("#1e293b")
SLATE_MID    = colors.HexColor("#475569")
SLATE_LIGHT  = colors.HexColor("#f8faff")
GREEN        = colors.HexColor("#16a34a")
GREEN_LIGHT  = colors.HexColor("#dcfce7")
AMBER        = colors.HexColor("#d97706")
AMBER_LIGHT  = colors.HexColor("#fef3c7")
RED          = colors.HexColor("#dc2626")
RED_LIGHT    = colors.HexColor("#fee2e2")
BLUE         = colors.HexColor("#2563eb")
BLUE_LIGHT   = colors.HexColor("#dbeafe")
BORDER       = colors.HexColor("#e2e8f0")
WHITE        = colors.white


def _priority_color(p):
    p = (p or "").lower()
    if p == "high":   return RED
    if p == "medium": return AMBER
    return GREEN


def _severity_color(s):
    s = (s or "").lower()
    if s == "high":   return RED
    if s == "medium": return AMBER
    return GREEN


def generate_pdf(analysis: dict, out_path: str = None) -> str:
    if out_path is None:
        out_path = os.path.join(tempfile.gettempdir(), "reqMind_Report.pdf")

    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch,  bottomMargin=0.75*inch,
    )

    styles = getSampleStyleSheet()
    W = letter[0] - 1.5*inch

    def S(name, **kw):
        base = kw.pop("parent", "Normal")
        return ParagraphStyle(name, parent=styles[base], **kw)

    sTitle  = S("sTitle",  parent="Title", fontSize=20, textColor=WHITE, spaceAfter=2, leading=24)
    sSub    = S("sSub",    fontSize=9,  textColor=colors.HexColor("#c7d2fe"))
    sH2     = S("sH2",     fontSize=12, textColor=INDIGO, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=5)
    sBody   = S("sBody",   fontSize=8.5, textColor=SLATE_DARK, leading=12)
    sSmall  = S("sSmall",  fontSize=8,  textColor=SLATE_MID)
    sWhite  = S("sWhite",  fontSize=8.5, textColor=WHITE, fontName="Helvetica-Bold")
    sFoot   = S("sFoot",   fontSize=7.5, textColor=SLATE_MID, alignment=1)

    story = []

    # ── HEADER ──────────────────────────────────────────────────────────────
    hdr = Table([[
        Paragraph("🧠  reqMind AI — Requirements Analysis Report", sTitle),
        Paragraph("HEC Hackathon 2026 · Group 26", sSub),
    ]], colWidths=[W])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), INDIGO),
        ("TOPPADDING",   (0,0),(-1,-1), 16),
        ("BOTTOMPADDING",(0,0),(-1,-1), 16),
        ("LEFTPADDING",  (0,0),(-1,-1), 18),
        ("RIGHTPADDING", (0,0),(-1,-1), 18),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 10))

    # ── PROJECT INFO BANNER ─────────────────────────────────────────────────
    pi = analysis.get("project_info", {})
    ptype  = pi.get("detected_type", "N/A")
    comp   = pi.get("complexity", "N/A")
    creason= pi.get("complexity_reason", "")
    total  = pi.get("total_requirements_count", "N/A")

    pi_data = [[
        Paragraph(f"<b>Project Type</b><br/><font size='9'>{ptype}</font>",    sBody),
        Paragraph(f"<b>Complexity</b><br/><font size='9'>{comp}</font>",       sBody),
        Paragraph(f"<b>Total Requirements</b><br/><font size='9'>{total}</font>", sBody),
        Paragraph(f"<b>Reason</b><br/><font size='8'>{creason}</font>",        sSmall),
    ]]
    pi_tbl = Table(pi_data, colWidths=[W/4]*4)
    pi_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), INDIGO_LIGHT),
        ("ALIGN",        (0,0),(-1,-1), "CENTER"),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("BOX",          (0,0),(-1,-1), 1, BORDER),
        ("INNERGRID",    (0,0),(-1,-1), 0.4, BORDER),
    ]))
    story.append(pi_tbl)
    story.append(Spacer(1, 8))

    # ── QUALITY SCORE ───────────────────────────────────────────────────────
    qs = analysis.get("quality_score", {})
    overall   = qs.get("overall", 0)
    clarity   = qs.get("clarity", 0)
    complete  = qs.get("completeness", 0)
    consist   = qs.get("consistency", 0)
    testabil  = qs.get("testability", 0)
    breakdown = qs.get("breakdown", "")

    score_color = GREEN if overall >= 70 else (AMBER if overall >= 40 else RED)

    score_data = [[
        Paragraph(f"<b><font size='22'>{overall}</font>/100</b><br/><font size='8'>Overall Score</font>", sBody),
        Paragraph(f"<b>Clarity:</b> {clarity}/100<br/><b>Completeness:</b> {complete}/100<br/><b>Consistency:</b> {consist}/100<br/><b>Testability:</b> {testabil}/100", sBody),
        Paragraph(f"<b>Assessment:</b><br/>{breakdown}", sSmall),
    ]]
    score_tbl = Table(score_data, colWidths=[W*0.18, W*0.27, W*0.55])
    score_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,0), score_color),
        ("TEXTCOLOR",    (0,0),(0,0), WHITE),
        ("BACKGROUND",   (1,0),(2,0), SLATE_LIGHT),
        ("ALIGN",        (0,0),(0,0), "CENTER"),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("BOX",          (0,0),(-1,-1), 1, BORDER),
        ("INNERGRID",    (0,0),(-1,-1), 0.4, BORDER),
    ]))
    story.append(Paragraph("📊  Requirement Quality Score", sH2))
    story.append(score_tbl)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width=W, color=BORDER, thickness=0.5))

    # ── HELPER: generic table section ───────────────────────────────────────
    def section(title, rows, headers, widths):
        story.append(Paragraph(title, sH2))
        if not rows:
            story.append(Paragraph("No items identified.", sSmall))
            story.append(Spacer(1, 6))
            return
        data = [[Paragraph(f"<b>{h}</b>", sWhite) for h in headers]] + rows
        tbl = Table(data, colWidths=widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),  INDIGO),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, SLATE_LIGHT]),
            ("GRID",          (0,0),(-1,-1), 0.4, BORDER),
            ("FONTSIZE",      (0,0),(-1,-1), 8),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 7),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 8))

    # ── SUMMARY STATS ───────────────────────────────────────────────────────
    summ = analysis.get("summary", {})
    story.append(Paragraph("📋  Summary", sH2))
    sum_data = [[
        Paragraph(f"<b>{summ.get('total_fr', len(analysis.get('functional_requirements',[])))}</b><br/><font size='7'>Functional</font>",     sBody),
        Paragraph(f"<b>{summ.get('total_nfr', len(analysis.get('non_functional_requirements',[])))}</b><br/><font size='7'>Non-Functional</font>", sBody),
        Paragraph(f"<b>{summ.get('total_ambiguities', len(analysis.get('ambiguities',[])))}</b><br/><font size='7'>Ambiguities</font>",          sBody),
        Paragraph(f"<b>{summ.get('total_risks', len(analysis.get('risks',[])))}</b><br/><font size='7'>Risks</font>",                             sBody),
        Paragraph(f"<b>{summ.get('total_scope_creep', len(analysis.get('scope_creep',[])))}</b><br/><font size='7'>Scope Creep</font>",           sBody),
        Paragraph(f"<b>{summ.get('overall_quality','N/A')}</b><br/><font size='7'>Quality</font>",                                                sBody),
    ]]
    s_tbl = Table(sum_data, colWidths=[W/6]*6)
    s_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), SLATE_LIGHT),
        ("ALIGN",        (0,0),(-1,-1), "CENTER"),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("BOX",          (0,0),(-1,-1), 1, BORDER),
        ("INNERGRID",    (0,0),(-1,-1), 0.4, BORDER),
    ]))
    story.append(s_tbl)
    if summ.get("recommendation"):
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"<b>Recommendation:</b> {summ['recommendation']}", sSmall))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width=W, color=BORDER, thickness=0.5))

    # ── FUNCTIONAL REQUIREMENTS ─────────────────────────────────────────────
    fr_rows = []
    for r in analysis.get("functional_requirements", []):
        p = r.get("priority","Low")
        pc = _priority_color(p)
        fr_rows.append([
            Paragraph(r.get("id",""),           sBody),
            Paragraph(r.get("description",""),  sBody),
            Paragraph(r.get("category",""),     sBody),
            Paragraph(f'<font color="{pc.hexval() if hasattr(pc,"hexval") else "black"}"><b>{p}</b></font>', sBody),
        ])
    section("🔍  Functional Requirements", fr_rows,
            ["ID","Description","Category","Priority"],
            [0.45*inch, W-2.1*inch, 0.9*inch, 0.75*inch])

    # ── NON-FUNCTIONAL REQUIREMENTS ─────────────────────────────────────────
    nfr_rows = [
        [Paragraph(r.get("id",""), sBody),
         Paragraph(r.get("category",""), sBody),
         Paragraph(r.get("description",""), sBody)]
        for r in analysis.get("non_functional_requirements", [])
    ]
    section("⚙️  Non-Functional Requirements", nfr_rows,
            ["ID","Category","Description"],
            [0.45*inch, 1.1*inch, W-1.55*inch])

    # ── CONSTRAINTS ─────────────────────────────────────────────────────────
    con_rows = [
        [Paragraph(r.get("id",""), sBody),
         Paragraph(r.get("description",""), sBody)]
        for r in analysis.get("constraints", [])
    ]
    section("🔒  Constraints", con_rows, ["ID","Description"], [0.45*inch, W-0.45*inch])

    # ── RISK ANALYSIS ───────────────────────────────────────────────────────
    risk_rows = []
    for r in analysis.get("risks", []):
        sev = r.get("severity","Low")
        sc  = _severity_color(sev)
        risk_rows.append([
            Paragraph(r.get("id",""),          sBody),
            Paragraph(r.get("type",""),        sBody),
            Paragraph(r.get("description",""), sBody),
            Paragraph(f'<font color="{sc.hexval() if hasattr(sc,"hexval") else "black"}"><b>{sev}</b></font>', sBody),
        ])
    section("🚨  Risk Analysis", risk_rows,
            ["ID","Type","Description","Severity"],
            [0.45*inch, 1.0*inch, W-2.2*inch, 0.75*inch])

    # ── AMBIGUITIES (highlighted) ───────────────────────────────────────────
    amb_rows = [
        [Paragraph(r.get("id",""),         sBody),
         Paragraph(r.get("text",""),       sBody),
         Paragraph(r.get("issue",""),      sBody),
         Paragraph(r.get("suggestion",""), sBody)]
        for r in analysis.get("ambiguities", [])
    ]
    story.append(Paragraph("⚠️  Detected Ambiguities", sH2))
    if not amb_rows:
        story.append(Paragraph("No ambiguities found.", sSmall))
    else:
        data = [[Paragraph(f"<b>{h}</b>", sWhite) for h in ["ID","Statement","Issue","Suggestion (Fix)"]]] + amb_rows
        tbl = Table(data, colWidths=[0.45*inch, W*0.28, W*0.25, W*0.28], repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),   AMBER),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),  [AMBER_LIGHT, WHITE]),
            ("GRID",          (0,0),(-1,-1),  0.4, BORDER),
            ("FONTSIZE",      (0,0),(-1,-1),  8),
            ("TOPPADDING",    (0,0),(-1,-1),  5),
            ("BOTTOMPADDING", (0,0),(-1,-1),  5),
            ("LEFTPADDING",   (0,0),(-1,-1),  7),
            ("VALIGN",        (0,0),(-1,-1),  "TOP"),
        ]))
        story.append(tbl)
    story.append(Spacer(1, 8))

    # ── MISSING INFORMATION (red highlight) ─────────────────────────────────
    mi_rows = [
        [Paragraph(r.get("id",""),          sBody),
         Paragraph(r.get("area",""),        sBody),
         Paragraph(r.get("description",""), sBody),
         Paragraph(r.get("impact",""),      sBody)]
        for r in analysis.get("missing_information", [])
    ]
    story.append(Paragraph("🔎  Missing Information", sH2))
    if not mi_rows:
        story.append(Paragraph("No missing information identified.", sSmall))
    else:
        data = [[Paragraph(f"<b>{h}</b>", sWhite) for h in ["ID","Area","Description","Impact"]]] + mi_rows
        tbl = Table(data, colWidths=[0.45*inch, 0.9*inch, W-1.9*inch, 0.55*inch], repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),   RED),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),  [RED_LIGHT, WHITE]),
            ("GRID",          (0,0),(-1,-1),  0.4, BORDER),
            ("FONTSIZE",      (0,0),(-1,-1),  8),
            ("TOPPADDING",    (0,0),(-1,-1),  5),
            ("BOTTOMPADDING", (0,0),(-1,-1),  5),
            ("LEFTPADDING",   (0,0),(-1,-1),  7),
            ("VALIGN",        (0,0),(-1,-1),  "TOP"),
        ]))
        story.append(tbl)
    story.append(Spacer(1, 8))

    # ── SCOPE CREEP ─────────────────────────────────────────────────────────
    sc_rows = [
        [Paragraph(r.get("id",""),        sBody),
         Paragraph(r.get("statement",""), sBody),
         Paragraph(r.get("reason",""),    sBody)]
        for r in analysis.get("scope_creep", [])
    ]
    section("🎯  Scope Creep Warnings", sc_rows,
            ["ID","Statement","Reason"],
            [0.45*inch, W*0.45, W*0.42])

    # ── STAKEHOLDER QUESTIONS ───────────────────────────────────────────────
    story.append(Paragraph("💬  Stakeholder Clarification Questions", sH2))
    cq = analysis.get("clarification_questions", {})
    role_colors = {
        "client":          (BLUE,        BLUE_LIGHT,  "👤 Client"),
        "developer":       (GREEN,       GREEN_LIGHT, "💻 Developer"),
        "tester":          (PURPLE,      INDIGO_LIGHT,"🧪 Tester"),
        "project_manager": (AMBER,       AMBER_LIGHT, "📋 Project Manager"),
    }
    for role, (hc, bc, label) in role_colors.items():
        questions = cq.get(role, [])
        if not questions:
            continue
        q_rows = [[Paragraph(q.get("id",""), sBody), Paragraph(q.get("question",""), sBody)]
                  for q in questions]
        data = [[Paragraph(f"<b>{label}</b>", sWhite), Paragraph("<b>Question</b>", sWhite)]] + q_rows
        tbl = Table(data, colWidths=[0.7*inch, W-0.7*inch], repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),  hc),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [bc, WHITE]),
            ("GRID",          (0,0),(-1,-1), 0.4, BORDER),
            ("FONTSIZE",      (0,0),(-1,-1), 8),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 7),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 5))

    # ── FOOTER ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width=W, color=BORDER, thickness=0.5))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Generated by reqMind AI  ·  HEC Hackathon 2026  ·  Cohort 02 · Group 26",
        sFoot
    ))

    doc.build(story)
    return out_path