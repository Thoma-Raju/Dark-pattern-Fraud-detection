import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def build_analysis_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor("#334155"),
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=8
    )

    story = []

    # Title
    story.append(Paragraph("Technical & Architectural Analysis Report", title_style))
    story.append(Paragraph("Project: Dark Pattern & Online Fraud Detection", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=15))

    # Section 1
    story.append(Paragraph("1. Codebase Architecture & Modularity", h1_style))
    story.append(Paragraph("The system is divided into two major components: a deterministic rule-based scraper (Part 1) and a machine learning Natural Language Processing pipeline (Part 2). "
                           "The separation of concerns is generally well-maintained. The Streamlit dashboards (`app.py`) correctly delegate processing logic "
                           "to backend service modules (`src/analyzer.py` and `predictor.py`). However, deploying them as two separate Streamlit runtimes "
                           "introduces fragmentation in the user experience.", body_style))

    # Section 2
    story.append(Paragraph("2. Deterministic Rule Engine Analysis", h1_style))
    story.append(Paragraph("The rule engine relies heavily on Regular Expressions (Regex) and BeautifulSoup4 DOM traversal. "
                           "While regex offers extremely fast parsing (O(N) time complexity relative to text length), it is inflexible. "
                           "The current regex patterns for 'fake countdowns' and 'hidden charges' are tightly coupled to English syntax. "
                           "The DOM traversal for `input[type='checkbox']` is effective, but vulnerable to Single Page Applications (SPAs) "
                           "that dynamically inject checkboxes into the DOM using JavaScript, which `requests.get()` cannot evaluate.", body_style))

    # Section 3
    story.append(Paragraph("3. Machine Learning NLP Integration", h1_style))
    story.append(Paragraph("The machine learning pipeline implements a classical NLP workflow: TF-IDF vectorization followed by Logistic Regression. "
                           "This approach is lightweight and provides excellent prediction latency, making it highly suitable for real-time web execution. "
                           "Because Logistic Regression is explainable, feature coefficients can be extracted to understand which specific dark web vocabulary "
                           "triggers the highest predictive weights. However, the limitation of TF-IDF is context-blindness. Phrases like 'Don't sign up' "
                           "might incorrectly trigger 'sign up' rules if n-grams are not correctly tuned.", body_style))

    # Section 4
    story.append(Paragraph("4. Code Quality, Security & Posture", h1_style))
    story.append(Paragraph("<b>Dependencies:</b> The libraries utilized (Streamlit, Scikit-learn, BeautifulSoup) are industry-standard and secure. "
                           "There are no custom unsafe execution pathways.<br/>"
                           "<b>Security:</b> The scraper uses a modern 'User-Agent' header, which helps bypass basic bot protections, but it lacks advanced "
                           "mechanisms like proxy rotation or headless browser orchestration (e.g., Selenium/Playwright) to bypass Cloudflare. "
                           "Parsing untrusted HTML with BeautifulSoup is strictly safe because it builds a DOM tree rather than executing scripts.<br/>"
                           "<b>Maintainability:</b> The code is moderately structured. Moving forward, type-hinting (PEP 484) and comprehensive docstrings "
                           "should be added to all `src/` modules to improve developer handover.", body_style))
                           
    # Section 5
    story.append(Paragraph("5. Scalability & Deployment Assessment", h1_style))
    story.append(Paragraph("Currently, the system is designed to run locally. To deploy this to a production environment (like AWS or Heroku), "
                           "the scraping logic might become a bottleneck. Synchronous `requests.get()` commands block the Streamlit thread. "
                           "For scale, the HTTP scraping module should be converted to asynchronous processing using `aiohttp` or offloaded "
                           "to a background task queue like Celery.", body_style))

    doc.build(story)
    print(f"Technical Analysis PDF generated at: {filename}")

if __name__ == "__main__":
    pdf_path = r"c:\Dark pattern and Online fraud detection\Project_Technical_Analysis.pdf"
    build_analysis_pdf(pdf_path)
