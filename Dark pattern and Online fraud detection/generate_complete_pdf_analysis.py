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
    Two-pass canvas to dynamically compute total pages and add running headers/footers.
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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "DARK PATTERN & ONLINE FRAUD DETECTOR — COMPLETE TECHNICAL ANALYSIS")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "JNTUK R23 PROJECT 29")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.75)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "Comprehensive System Specification & Architecture Report")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(54, 46, letter[0] - 54, 46)

        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    navy_dark = colors.HexColor("#0f172a")      # Primary Title / Headers
    blue_accent = colors.HexColor("#0284c7")    # Subtitles & Highlights
    text_slate = colors.HexColor("#334155")     # Body text
    bg_code = colors.HexColor("#f8fafc")        # Code block background
    border_slate = colors.HexColor("#cbd5e1")   # Dividers & Borders
    red_high = colors.HexColor("#dc2626")       # High Severity
    amber_mid = colors.HexColor("#d97706")      # Medium Severity
    green_safe = colors.HexColor("#16a34a")     # Low/Safe Severity

    # Paragraph Styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=navy_dark,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'MainSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=blue_accent,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=navy_dark,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=blue_accent,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_slate,
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3.5
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=navy_dark,
        backColor=bg_code,
        borderColor=border_slate,
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0369a1"),
        backColor=colors.HexColor("#f0f9ff"),
        borderColor=colors.HexColor("#bae6fd"),
        borderWidth=0.75,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=8
    )

    story = []

    # Document Header Banner
    story.append(Paragraph("Dark Pattern & Online Fraud Detector", title_style))
    story.append(Paragraph("Complete Comprehensive Technical Analysis, System Architecture & Implementation Report", subtitle_style))
    story.append(Paragraph("<b>Academic Context:</b> JNTUK R23 Curriculum — Project 29 Implementation &nbsp;|&nbsp; <b>Framework:</b> Python, Streamlit, Scikit-Learn", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=blue_accent, spaceBefore=4, spaceAfter=12))

    # SECTION 1: INTRODUCTION & THEORETICAL FOUNDATIONS
    story.append(Paragraph("1. Introduction & Theoretical Foundations", h1_style))
    intro_p1 = (
        "Modern e-commerce and digital service platforms increasingly utilize subtle user interface design choices "
        "crafted to influence user decision-making. When these designs exploit human psychological cognitive biases to "
        "trick users into taking actions they might not otherwise choose (such as purchasing unnecessary add-ons, "
        "signing up for hidden recurring subscriptions, or disclosing private data), they are termed <b>Dark Patterns</b>."
    )
    story.append(Paragraph(intro_p1, body_style))

    story.append(Paragraph("Cognitive Biases Exploited by Dark Patterns:", h2_style))
    biases = [
        "<b>Urgency Bias & Scarcity Mindset:</b> Artificial countdown timers or false inventory alerts ('Only 2 items left!') trigger fear of missing out (FOMO) and prompt impulsive purchases.",
        "<b>Loss Aversion & Confirmshaming:</b> Emotional guilt-tripping language ('No thanks, I hate saving money') forces users toward options favorable to the business.",
        "<b>Status Quo Bias & Default Opt-Ins:</b> Pre-ticked checkboxes rely on user inertia, causing users to passively consent to recurring newsletters, insurances, or subscriptions.",
        "<b>Hidden Costs & Price Anchoring:</b> Additional convenience fees, service charges, or processing costs introduced late in checkout obscure the true transaction cost."
    ]
    for b in biases:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(Spacer(1, 6))

    # SECTION 2: SYSTEM ARCHITECTURE & PARADIGM
    story.append(Paragraph("2. System Architecture & Detection Framework", h1_style))
    arch_p = (
        "The application implements a <b>hybrid detection paradigm</b> comprising two distinct sub-systems: "
        "a transparent, rule-based deterministic scanner (Part 1) and a statistical Natural Language Processing (NLP) "
        "machine learning classification pipeline (Part 2)."
    )
    story.append(Paragraph(arch_p, body_style))

    # Architecture Overview Table
    arch_table_data = [
        [Paragraph("<b>Layer / Module</b>", body_style), Paragraph("<b>Components & Libraries</b>", body_style), Paragraph("<b>Technical Functionality</b>", body_style)],
        [
            Paragraph("<b>User Interface (UI)</b>", body_style),
            Paragraph("Streamlit 1.38+, Custom CSS (Inter font, Glassmorphism)", body_style),
            Paragraph("Renders a dark cybersecurity dashboard. Accepts input URLs, displays live indicators, risk gauge, HTML metrics, evidence log, and text report export.", body_style)
        ],
        [
            Paragraph("<b>Scraper & DOM Parser</b>", body_style),
            Paragraph("Requests 2.32+, BeautifulSoup4 4.12+", body_style),
            Paragraph("Issues HTTP GET with modern Chrome User-Agent. Cleans HTML by stripping &lt;script&gt;, &lt;style&gt;, &lt;svg&gt;, &lt;noscript&gt; tags.", body_style)
        ],
        [
            Paragraph("<b>Part 1: Rule Engine</b>", body_style),
            Paragraph("Python <code>re</code> Regex, DOM Input Inspector", body_style),
            Paragraph("Applies 5 regex rule groups on cleaned text. Traverses BeautifulSoup DOM tree for <code>&lt;input type='checkbox' checked&gt;</code> near subscription keywords.", body_style)
        ],
        [
            Paragraph("<b>Part 2: ML Pipeline</b>", body_style),
            Paragraph("Scikit-Learn, TF-IDF Vectorizer, Logistic Regression, Joblib", body_style),
            Paragraph("Transforms text into TF-IDF unigram/bigram features. Classifies snippets into <i>neutral</i> vs. <i>dark_pattern</i> with confidence scores.", body_style)
        ]
    ]

    arch_table = Table(arch_table_data, colWidths=[1.5*inch, 1.8*inch, 3.7*inch])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_slate),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_table)

    story.append(Spacer(1, 10))

    # SECTION 3: RULE ENGINE & RISK MATHEMATICS
    story.append(Paragraph("3. Rule Engine Specifications & Risk Mathematics", h1_style))
    story.append(Paragraph("The deterministic engine inspects extracted text and DOM elements across 5 weighted rule categories:", body_style))

    # Rules Detail Table
    rules_table_data = [
        [Paragraph("<b>Rule Name</b>", body_style), Paragraph("<b>Key</b>", body_style), Paragraph("<b>Weight</b>", body_style), Paragraph("<b>Severity</b>", body_style), Paragraph("<b>Regex Patterns / Detection Heuristic</b>", body_style)],
        [
            Paragraph("<b>Fake Countdown</b>", body_style),
            Paragraph("<code>countdown</code>", body_style),
            Paragraph("<b>30%</b>", body_style),
            Paragraph("<font color='#dc2626'><b>HIGH</b></font>", body_style),
            Paragraph("<code>only \\d+ (minutes|hours|seconds) left<br/>\\d{1,2}:\\d{2}:\\d{2}, countdown, time is running out</code>", body_style)
        ],
        [
            Paragraph("<b>Hidden Charges</b>", body_style),
            Paragraph("<code>charges</code>", body_style),
            Paragraph("<b>25%</b>", body_style),
            Paragraph("<font color='#dc2626'><b>HIGH</b></font>", body_style),
            Paragraph("<code>service fee, handling fee, convenience fee, processing fee, additional charges, fee may apply</code>", body_style)
        ],
        [
            Paragraph("<b>Pre-ticked Checkbox</b>", body_style),
            Paragraph("<code>subscription</code>", body_style),
            Paragraph("<b>30%</b>", body_style),
            Paragraph("<font color='#dc2626'><b>HIGH</b></font>", body_style),
            Paragraph("DOM Inspection: <code>input[type=checkbox][checked]</code> with parent text containing <i>subscribe, renew, recurring</i>", body_style)
        ],
        [
            Paragraph("<b>Urgency Language</b>", body_style),
            Paragraph("<code>urgency</code>", body_style),
            Paragraph("<b>15%</b>", body_style),
            Paragraph("<font color='#d97706'><b>MEDIUM</b></font>", body_style),
            Paragraph("<code>limited time, only \\d+ left, don't miss out, buy now, act now, hurry, last chance, ending soon</code>", body_style)
        ],
        [
            Paragraph("<b>Manipulative Wording</b>", body_style),
            Paragraph("<code>manipulative</code>", body_style),
            Paragraph("<b>10%</b>", body_style),
            Paragraph("<font color='#d97706'><b>MEDIUM</b></font>", body_style),
            Paragraph("<code>you'll regret, missing out, exclusive deal, secret offer, claim before, while supplies last</code>", body_style)
        ]
    ]

    rules_table = Table(rules_table_data, colWidths=[1.3*inch, 0.9*inch, 0.6*inch, 0.8*inch, 3.4*inch])
    rules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_slate),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
    ]))
    story.append(rules_table)

    story.append(Spacer(1, 8))

    math_box = (
        "<b>Mathematical Risk Scoring Formulation:</b><br/>"
        "Let <i>R</i> be the set of configured rules, and <i>M ⊆ R</i> be the subset of rules matched during scan.<br/>"
        "Each rule <i>r ∈ R</i> has an assigned numeric weight <i>w(r)</i>.<br/>"
        "The page <b>Risk Score (S)</b> is calculated as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>S = min( 100,  Σ <sub>r ∈ M</sub>  w(r) )</b><br/><br/>"
        "<b>Severity Classification Function:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>HIGH Severity:</b> S ≥ 70% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (High risk of deception or financial trap)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>MEDIUM Severity:</b> 40% ≤ S &lt; 70% &nbsp;&nbsp; (Moderate pressuring tactics present)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>LOW Severity:</b> 0% &lt; S &lt; 40% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (Minor promotional wording matched)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>NONE Severity:</b> S = 0% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (No configured dark pattern indicators found)"
    )
    story.append(Paragraph(math_box, callout_style))

    story.append(PageBreak())

    # SECTION 4: MACHINE LEARNING PIPELINE
    story.append(Paragraph("4. Machine Learning NLP Pipeline (Part 2)", h1_style))
    ml_intro = (
        "To complement static regex rules, Part 2 incorporates a supervised Machine Learning pipeline designed "
        "to classify arbitrary web text snippets based on learned n-gram term frequencies."
    )
    story.append(Paragraph(ml_intro, body_style))

    story.append(Paragraph("TF-IDF Vectorization & Classification Mathematics:", h2_style))
    ml_math_desc = (
        "Term Frequency-Inverse Document Frequency (TF-IDF) converts raw text into numerical feature vectors by weighting "
        "term frequency against its inverse document frequency across the training corpus:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>TF-IDF(t, d, D) = TF(t, d) × log( |D| / |{d ∈ D : t ∈ d}| )</b><br/><br/>"
        "The vectorized feature vector <b>x</b> is passed to a <b>Logistic Regression</b> classifier, which calculates "
        "the posterior probability of a snippet containing a dark pattern using the sigmoid activation function:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(y = 1 | x) = 1 / ( 1 + e<sup>-(w<sup>T</sup>x + b)</sup> )</b>"
    )
    story.append(Paragraph(ml_math_desc, callout_style))

    story.append(Paragraph("Model Training & Persistence Pipeline:", h2_style))
    ml_code_snippet = (
        "# src/train_model.py (Excerpt)\n"
        "from sklearn.feature_extraction.text import TfidfVectorizer\n"
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.pipeline import make_pipeline\n"
        "import joblib\n\n"
        "# Create TF-IDF + Logistic Regression pipeline\n"
        "model = make_pipeline(\n"
        "    TfidfVectorizer(ngram_range=(1, 2), stop_words='english'),\n"
        "    LogisticRegression(C=1.0, max_iter=1000)\n"
        ")\n\n"
        "# Train model on labeled dataset\n"
        "model.fit(X_train, y_train)\n"
        "# Serialize trained model pipeline\n"
        "joblib.dump(model, 'models/dark_pattern_model.joblib')"
    )
    story.append(Paragraph(ml_code_snippet, code_style))

    story.append(Spacer(1, 8))

    # SECTION 5: COMPREHENSIVE REPOSITORY STRUCTURE
    story.append(Paragraph("5. Project File Hierarchy & Component Mapping", h1_style))
    tree_text = (
        "Dark pattern and Online fraud detection/\n"
        "│\n"
        "├── app.py                          # Streamlit Part 1 Dashboard (586 lines)\n"
        "├── requirements.txt                # Core Dependencies (Streamlit, Requests, BS4)\n"
        "├── README.md                       # Windows 11 PowerShell Setup Guide\n"
        "├── generate_pdf.py                 # Automated Report Generation Utility\n"
        "│\n"
        "├── src/\n"
        "│   ├── __init__.py\n"
        "│   └── analyzer.py                 # Scraping Engine, Regex Parser & Scoring Logic\n"
        "│\n"
        "├── data/\n"
        "│   └── README.txt                  # Dataset Storage Information\n"
        "│\n"
        "└── second/\n"
        "    └── dark_pattern_detector_part2/\n"
        "        ├── app.py                  # Part 2 Hybrid ML Dashboard\n"
        "        ├── requirements.txt        # Scikit-Learn & ML Dependencies\n"
        "        ├── README.md               # Part 2 Execution Overview\n"
        "        ├── data/\n"
        "        │   └── dark_patterns.csv   # Labeled Dataset (Neutral vs. Dark Pattern)\n"
        "        ├── models/\n"
        "        │   └── dark_pattern_model.joblib # Serialized Scikit-Learn Model\n"
        "        └── src/\n"
        "            ├── __init__.py\n"
        "            ├── analyzer.py         # Extended Analyzer\n"
        "            ├── predictor.py        # Real-time ML Inference Engine\n"
        "            └── train_model.py      # Model Training & Vectorizer Script"
    )
    story.append(Paragraph(tree_text, code_style))

    story.append(Spacer(1, 10))

    # SECTION 6: CODE DEEP-DIVE
    story.append(Paragraph("6. Key Implementation Code Walkthrough", h1_style))
    story.append(Paragraph("Below are key extracts demonstrating the HTML cleaning, DOM checkbox parsing, and evidence extraction logic from <code>src/analyzer.py</code>:", body_style))

    analyzer_code = (
        "# src/analyzer.py (Core Analysis Engine Extract)\n"
        "def clean_text(soup):\n"
        "    # Decompose script, style, noscript, and svg elements\n"
        "    for tag in soup([\"script\", \"style\", \"noscript\", \"svg\"]):\n"
        "        tag.decompose()\n"
        "    return \" \".join(soup.stripped_strings)\n\n"
        "def detect_checkboxes(soup):\n"
        "    # Traverse DOM for pre-checked subscription input boxes\n"
        "    result = []\n"
        "    for checkbox in soup.find_all(\"input\"):\n"
        "        if checkbox.get(\"type\", \"\").lower() != \"checkbox\": continue\n"
        "        if not checkbox.has_attr(\"checked\"): continue\n"
        "        parent_text = \" \".join(checkbox.parent.stripped_strings).lower()\n"
        "        if any(w in parent_text for w in [\"subscribe\", \"subscription\", \"recurring\", \"renew\"]):\n"
        "            result.append({\"key\": \"subscription\", \"name\": \"Pre-ticked Subscription\",\n"
        "                           \"severity\": \"HIGH\", \"weight\": 30})\n"
        "            break\n"
        "    return result"
    )
    story.append(Paragraph(analyzer_code, code_style))

    story.append(Spacer(1, 10))

    # SECTION 7: STEP-BY-STEP OPERATIONAL GUIDE
    story.append(Paragraph("7. Operational Guide & Execution Commands", h1_style))
    ops_guide = (
        "To run the complete system locally on Windows 11 using PowerShell:"
    )
    story.append(Paragraph(ops_guide, body_style))

    cmd_box = (
        "# Step 1: Open PowerShell in project directory\n"
        "cd \"c:\\Dark pattern and Online fraud detection\"\n\n"
        "# Step 2: Initialize & Activate Virtual Environment\n"
        "python -m venv .venv\n"
        ".\\.venv\\Scripts\\Activate.ps1\n\n"
        "# Step 3: Install Required Dependencies\n"
        "pip install -r requirements.txt\n\n"
        "# Step 4: Run Part 1 Rule-Based Streamlit App\n"
        "streamlit run app.py\n\n"
        "# Step 5: Run Part 2 Machine Learning App\n"
        "cd second\\dark_pattern_detector_part2\n"
        "python src/train_model.py\n"
        "streamlit run app.py"
    )
    story.append(Paragraph(cmd_box, code_style))

    story.append(Spacer(1, 8))

    # SECTION 8: LIMITATIONS & FUTURE ENHANCEMENTS
    story.append(Paragraph("8. Technical Limitations & Future Roadmap", h1_style))

    limits_roadmap = [
        "<b>Single-Page Application (SPA) Limitations:</b> Heavy JavaScript frameworks (React/Vue/Angular) rendering content dynamically client-side may require headless browser automation (Playwright/Selenium) for complete DOM analysis.",
        "<b>Anti-Bot Protections:</b> Websites protected by Cloudflare, Akamai, or CAPTCHAs may block automated HTTP GET requests (HTTP 403/503).",
        "<b>Future Browser Extension Integration:</b> Packaging the detection engine into a Chromium Manifest V3 browser extension to enable real-time on-page visual highlighting for end users during shopping sessions.",
        "<b>Transformer-Based NLP Models:</b> Upgrading the classifier from TF-IDF + Logistic Regression to fine-tuned RoBERTa or DeBERTa models for contextual ambiguity resolution."
    ]
    for lr in limits_roadmap:
        story.append(Paragraph(f"• {lr}", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully created exhaustive PDF report at: {filename}")

if __name__ == "__main__":
    pdf_path = r"c:\Dark pattern and Online fraud detection\Dark_Pattern_and_Online_Fraud_Detection_Comprehensive_Analysis.pdf"
    build_pdf(pdf_path)
