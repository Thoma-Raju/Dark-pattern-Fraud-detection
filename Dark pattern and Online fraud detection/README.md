# Dark Pattern & Online Fraud Detector — Part 1

A professional Streamlit implementation of the JNTUK R23 Project 29 concept.

## Part 1 features

- URL input and website fetching
- Rule-based dark-pattern detection
- Fake countdown / artificial urgency detection
- Hidden or additional charge language detection
- Subscription / recurring-consent detection
- Pre-ticked subscription checkbox detection
- Manipulative wording detection
- Transparent risk score
- HIGH / MEDIUM / LOW / NONE severity
- Evidence snippets
- Website analysis summary
- Text report download
- Professional dark cybersecurity dashboard

## Important

This is a rule-based prototype. A detected pattern is an indicator for investigation, not proof that a website is fraudulent.

Some websites block automated requests or require JavaScript. In that case the application may not be able to fetch enough HTML for analysis.

## Windows 11 setup

Open PowerShell in this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL shown by Streamlit, normally:

http://localhost:8501

## Project structure

```text
dark_pattern_detector_part1_pro/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── __init__.py
│   └── analyzer.py
│
└── data/
    └── README.txt
```

## Safe testing

For reliable demonstrations, use a local HTML test page or a website you are authorized to analyze. Public websites can change their HTML or block automated requests.
