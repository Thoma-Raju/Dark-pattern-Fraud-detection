import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page numbers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))

        # Draw header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Dark Pattern & Online Fraud Detector — Project Documentation")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Draw footer on all pages
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_str)
        self.drawString(54, 36, "JNTUK R23 Project 29 Concept Implementation | Confidential & Proprietary")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, letter[0] - 54, 48)

        self.restoreState()


def create_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f172a")    # Slate 900
    secondary_color = colors.HexColor("#0284c7")  # Sky 600
    dark_bg = colors.HexColor("#1e293b")         # Slate 800
    text_dark = colors.HexColor("#334155")       # Slate 700
    code_bg = colors.HexColor("#f8fafc")         # Slate 50
    border_color = colors.HexColor("#e2e8f0")    # Slate 200

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_dark,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=code_bg,
        borderColor=border_color,
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=body_style,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0369a1"),
        backColor=colors.HexColor("#f0f9ff"),
        borderColor=colors.HexColor("#bae6fd"),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=8
    )

    story = []

    # Title Banner
    story.append(Paragraph("Dark Pattern & Online Fraud Detector", title_style))
    story.append(Paragraph("Complete Technical Project Documentation — JNTUK R23 Project 29 Implementation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=secondary_color, spaceBefore=0, spaceAfter=15))

    # Executive Overview
    story.append(Paragraph("1. Executive Overview", h1_style))
    overview_text = (
        "The <b>Dark Pattern & Online Fraud Detector</b> is a specialized cybersecurity and consumer protection "
        "application developed in alignment with the <i>JNTUK R23 Project 29</i> specification. Its primary objective "
        "is to audit e-commerce websites and web pages to automatically detect user interface designs that mislead, "
        "coerce, or manipulate users into unintended financial or privacy commitments (commonly known as <b>Dark Patterns</b>)."
    )
    story.append(Paragraph(overview_text, body_style))

    key_caps = [
        "<b>Rule-Based DOM & Text Inspection Engine:</b> Scans page HTML for patterns including urgency timers, hidden fees, pre-checked boxes, and manipulative phrasing.",
        "<b>Machine Learning Classification Core:</b> Utilizes Natural Language Processing (NLP) with TF-IDF vectorization and Logistic Regression to categorize text snippets into neutral vs. dark patterns.",
        "<b>Transparent Risk Scoring System:</b> Computes a weighted risk score (0–100%) and maps it to standardized severity levels (HIGH, MEDIUM, LOW, NONE).",
        "<b>Cybersecurity Dashboard:</b> Interactive Streamlit web interface featuring real-time visual alerts, HTML metrics, extracted evidence snippets, and downloadable scan reports."
    ]
    for cap in key_caps:
        story.append(Paragraph(f"• {cap}", bullet_style))

    story.append(Spacer(1, 10))

    # System Architecture
    story.append(Paragraph("2. System Architecture & Detection Workflow", h1_style))
    arch_desc = (
        "The project is structured into a two-part hybrid framework that combines immediate heuristic rule matching "
        "with statistical machine learning model predictions:"
    )
    story.append(Paragraph(arch_desc, body_style))

    # Architecture Table
    arch_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology Stack</b>", body_style), Paragraph("<b>Function & Description</b>", body_style)],
        [Paragraph("<b>Web Frontend UI</b>", body_style), Paragraph("Streamlit, HTML5, Custom CSS", body_style), Paragraph("Modern cybersecurity dark-themed UI providing URL entry, live indicators, risk gauge, and evidence views.", body_style)],
        [Paragraph("<b>HTTP & HTML Parser</b>", body_style), Paragraph("Requests, BeautifulSoup4", body_style), Paragraph("Fetches target Web pages with custom User-Agent headers, strips non-content tags (script, style), and cleans text.", body_style)],
        [Paragraph("<b>Rule Engine (Part 1)</b>", body_style), Paragraph("Python re (Regex), DOM Parser", body_style), Paragraph("Performs pattern matching on cleaned text and DOM elements (e.g. pre-selected checkbox input tags).", body_style)],
        [Paragraph("<b>ML Pipeline (Part 2)</b>", body_style), Paragraph("Scikit-Learn, Joblib, TF-IDF", body_style), Paragraph("Vectorizes word unigrams/bigrams and applies a trained Logistic Regression model to compute dark pattern probability.", body_style)],
    ]
    arch_table = Table(arch_data, colWidths=[1.4*inch, 1.6*inch, 4.0*inch])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('TEXTCOLOR', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)

    story.append(Spacer(1, 12))

    # Rule Engine Details
    story.append(Paragraph("3. Rule Engine & Risk Scoring Methodology", h1_style))
    story.append(Paragraph("Part 1 evaluates web pages against five core dark pattern categories, assigning specific weights and severity levels:", body_style))

    rules_data = [
        [Paragraph("<b>Pattern Category</b>", body_style), Paragraph("<b>Severity</b>", body_style), Paragraph("<b>Weight</b>", body_style), Paragraph("<b>Example Regex / Indicators</b>", body_style)],
        [Paragraph("<b>Fake Countdown Timer</b>", body_style), Paragraph("<font color='#d90429'><b>HIGH</b></font>", body_style), Paragraph("30%", body_style), Paragraph("<code>only \\d+ minutes left, \\d{1,2}:\\d{2}:\\d{2}, countdown</code>", body_style)],
        [Paragraph("<b>Hidden Charges</b>", body_style), Paragraph("<font color='#d90429'><b>HIGH</b></font>", body_style), Paragraph("25%", body_style), Paragraph("<code>service fee, handling fee, convenience fee, extra charges</code>", body_style)],
        [Paragraph("<b>Pre-ticked Subscription</b>", body_style), Paragraph("<font color='#d90429'><b>HIGH</b></font>", body_style), Paragraph("30%", body_style), Paragraph("HTML <code>&lt;input type='checkbox' checked&gt;</code> near renewal/subscription text", body_style)],
        [Paragraph("<b>Urgency Language</b>", body_style), Paragraph("<font color='#d4a373'><b>MEDIUM</b></font>", body_style), Paragraph("15%", body_style), Paragraph("<code>limited time, don't miss out, hurry, last chance</code>", body_style)],
        [Paragraph("<b>Manipulative Wording</b>", body_style), Paragraph("<font color='#d4a373'><b>MEDIUM</b></font>", body_style), Paragraph("10%", body_style), Paragraph("<code>you'll regret, secret offer, claim before, supplies last</code>", body_style)],
    ]
    rules_table = Table(rules_data, colWidths=[1.6*inch, 0.9*inch, 0.7*inch, 3.8*inch])
    rules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(rules_table)

    story.append(Spacer(1, 8))

    formula_text = (
        "<b>Risk Score Calculation:</b><br/>"
        "The overall Risk Score is derived by summing the weights of all matched rules, capped at 100%:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Risk Score = min( 100, Σ Weight<sub>i</sub> )</b><br/><br/>"
        "<b>Severity Threshold Mapping:</b><br/>"
        "• <b>HIGH Risk:</b> Score ≥ 70% (Multiple deceptive tactics or explicit forced continuity detected)<br/>"
        "• <b>MEDIUM Risk:</b> 40% ≤ Score &lt; 70% (Pressure selling or subtle urgency cues found)<br/>"
        "• <b>LOW Risk:</b> 0% &lt; Score &lt; 40% (Minor promotional wording matched)<br/>"
        "• <b>NONE Risk:</b> Score = 0% (No dark pattern indicators matched)"
    )
    story.append(Paragraph(formula_text, callout_style))

    story.append(PageBreak())

    # Part 2 ML Details
    story.append(Paragraph("4. Machine Learning Pipeline (Part 2)", h1_style))
    ml_text = (
        "In Part 2, the system extends rule-based detection with a machine learning classification engine designed "
        "to evaluate text snippets dynamically without relying solely on rigid regex patterns."
    )
    story.append(Paragraph(ml_text, body_style))

    ml_steps = [
        "<b>Text Cleaning & Normalization:</b> Strips HTML markup, scripts, and non-alphanumeric noise.",
        "<b>Feature Extraction:</b> TF-IDF (Term Frequency-Inverse Document Frequency) Vectorizer configured with word unigrams and bigrams to capture phrase context.",
        "<b>Model Training:</b> Binary Logistic Regression classifier trained to output class probabilities for <i>neutral</i> vs. <i>dark_pattern</i>.",
        "<b>Model Serialization:</b> Trained pipeline saved as a Joblib artifact (<code>models/dark_pattern_model.joblib</code>) for quick runtime inference."
    ]
    for step in ml_steps:
        story.append(Paragraph(f"1. {step}", bullet_style))

    story.append(Spacer(1, 10))

    # Project Directory Layout
    story.append(Paragraph("5. Project Repository Structure", h1_style))
    tree_code = (
        "Dark pattern and Online fraud detection/\n"
        "├── app.py                          # Streamlit Main Application (Part 1 Dashboard)\n"
        "├── requirements.txt                # Python Dependency Definitions\n"
        "├── README.md                       # Installation and Overview Guide\n"
        "├── src/\n"
        "│   ├── __init__.py\n"
        "│   └── analyzer.py                 # Core Fetching, Rule Engine & Risk Scoring\n"
        "├── data/\n"
        "│   └── README.txt                  # Dataset Storage Information\n"
        "└── second/\n"
        "    └── dark_pattern_detector_part2/\n"
        "        ├── app.py                  # Part 2 ML Streamlit Dashboard\n"
        "        ├── requirements.txt\n"
        "        ├── README.md\n"
        "        ├── data/\n"
        "        │   └── dark_patterns.csv   # Training Dataset\n"
        "        ├── models/\n"
        "        │   └── dark_pattern_model.joblib # Trained Machine Learning Model Artifact\n"
        "        └── src/\n"
        "            ├── analyzer.py\n"
        "            ├── predictor.py        # ML Inference Engine\n"
        "            └── train_model.py      # ML Model Training Script"
    )
    story.append(Paragraph(tree_code, code_style))

    story.append(Spacer(1, 10))

    # User Setup & Execution Guide
    story.append(Paragraph("6. Installation & Operating Instructions", h1_style))
    story.append(Paragraph("Follow these steps to setup and launch the project on Windows 11 / PowerShell:", body_style))

    setup_cmd = (
        "# 1. Navigate to project root directory\n"
        "cd \"c:\\Dark pattern and Online fraud detection\"\n\n"
        "# 2. Create Python Virtual Environment\n"
        "python -m venv .venv\n\n"
        "# 3. Activate Virtual Environment\n"
        ".\\.venv\\Scripts\\Activate.ps1\n\n"
        "# 4. Install Dependencies\n"
        "pip install -r requirements.txt\n\n"
        "# 5. Launch Part 1 Streamlit App\n"
        "streamlit run app.py\n\n"
        "# 6. (Optional) Train & Launch Part 2 ML App\n"
        "cd second\\dark_pattern_detector_part2\n"
        "python src/train_model.py\n"
        "streamlit run app.py"
    )
    story.append(Paragraph(setup_cmd, code_style))

    story.append(Spacer(1, 10))

    # Safe Testing & Disclaimer
    story.append(Paragraph("7. Safe Testing & Academic Disclaimer", h1_style))
    disclaimer_text = (
        "<b>Important Note:</b> This system serves as a rule-based and machine-learning prototype for research "
        "and educational demonstration. Detection of a dark pattern indicator signifies a potential issue for user "
        "investigation rather than definitive legal proof of fraudulent intent. Website structures and third-party "
        "anti-scraping protections (e.g. Cloudflare, JavaScript rendering requirements) may impact fetching accuracy."
    )
    story.append(Paragraph(disclaimer_text, callout_style))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report at: {filename}")

if __name__ == "__main__":
    out_pdf = r"c:\Dark pattern and Online fraud detection\Dark_Pattern_and_Online_Fraud_Detection_Project_Details.pdf"
    create_pdf(out_pdf)
