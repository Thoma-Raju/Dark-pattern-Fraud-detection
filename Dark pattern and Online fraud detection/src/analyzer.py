import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36"
)

RULES = [
    {
        "key": "countdown",
        "name": "Fake Countdown Timer",
        "icon": "⏱️",
        "weight": 30,
        "severity": "HIGH",
        "description": "Countdown or timer language can create artificial urgency and push users toward immediate purchase decisions.",
        "patterns": [
            r"\bonly\s+\d+\s*(minutes?|hours?|seconds?)\s*(left|remaining)?\b",
            r"\b\d{1,2}:\d{2}:\d{2}\b",
            r"\bcountdown\b",
            r"\btime\s+is\s+running\s+out\b",
        ],
    },
    {
        "key": "charges",
        "name": "Hidden Charges",
        "icon": "💰",
        "weight": 25,
        "severity": "HIGH",
        "description": "Additional fee language may indicate costs that are introduced later in the purchase process.",
        "patterns": [
            r"\bservice\s+fee\b",
            r"\bhandling\s+fee\b",
            r"\bconvenience\s+fee\b",
            r"\bprocessing\s+fee\b",
            r"\badditional\s+charges?\b",
            r"\bextra\s+charges?\b",
            r"\bfee\s+may\s+apply\b",
            r"\bcharges?\s+apply\b",
        ],
    },
    {
        "key": "subscription",
        "name": "Pre-ticked Subscription",
        "icon": "☑️",
        "weight": 30,
        "severity": "HIGH",
        "description": "Pre-selected subscription or recurring-consent controls can cause users to agree without intentionally selecting the option.",
        "patterns": [
            r"\bauto[\s-]?renew\b",
            r"\brecurring\b",
            r"\bsubscribe\b",
            r"\bsubscription\b",
            r"\bnewsletter\b",
            r"\bmembership\b",
        ],
    },
    {
        "key": "urgency",
        "name": "Urgency Language",
        "icon": "⚡",
        "weight": 15,
        "severity": "MEDIUM",
        "description": "Pressure language such as limited-time offers or scarcity messages can influence users to act quickly.",
        "patterns": [
            r"\blimited\s+time\b",
            r"\bonly\s+\d+\s+left\b",
            r"\bdon'?t\s+miss\s+out\b",
            r"\bbuy\s+now\b",
            r"\bact\s+now\b",
            r"\bhurry\b",
            r"\blast\s+chance\b",
            r"\blimited\s+offer\b",
            r"\bending\s+soon\b",
        ],
    },
    {
        "key": "manipulative",
        "name": "Manipulative Wording",
        "icon": "⚠️",
        "weight": 10,
        "severity": "MEDIUM",
        "description": "Emotionally pressuring or manipulative wording may be used to discourage careful consideration.",
        "patterns": [
            r"\byou'?ll\s+regret\b",
            r"\bmissing\s+out\b",
            r"\bexclusive\s+deal\b",
            r"\bsecret\s+offer\b",
            r"\bclaim\s+before\b",
            r"\bwhile\s+supplies\s+last\b",
        ],
    },
]


def normalize_url(url):
    url = url.strip()
    if not re.match(r"^https?://", url, re.I):
        url = "https://" + url
    return url


def fetch_page(url):
    response = requests.get(
        normalize_url(url),
        headers={"User-Agent": USER_AGENT},
        timeout=15,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response


def clean_text(soup):
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return " ".join(soup.stripped_strings)


def detect_rules(text):
    lower = text.lower()
    findings = []
    evidence = []
    seen = set()

    for rule in RULES:
        matched = []
        for pattern in rule["patterns"]:
            m = re.search(pattern, lower, re.I)
            if m:
                matched.append(m)
                if len(matched) >= 2:
                    break

        if matched:
            findings.append({
                "key": rule["key"],
                "name": rule["name"],
                "icon": rule["icon"],
                "weight": rule["weight"],
                "severity": rule["severity"],
                "description": rule["description"],
            })

            for m in matched[:2]:
                start = max(0, m.start() - 55)
                end = min(len(text), m.end() + 70)
                snippet = " ".join(text[start:end].split())
                marker = (rule["key"], snippet)
                if marker not in seen:
                    evidence.append({
                        "snippet": snippet,
                        "label": rule["name"],
                    })
                    seen.add(marker)

    return findings, evidence


def detect_checkboxes(soup):
    result = []
    for checkbox in soup.find_all("input"):
        if checkbox.get("type", "").lower() != "checkbox":
            continue
        if not checkbox.has_attr("checked"):
            continue

        parent_text = " ".join(checkbox.parent.stripped_strings).lower()
        nearby = " ".join(checkbox.parent.parent.stripped_strings).lower() if checkbox.parent.parent else parent_text

        if any(word in (parent_text + " " + nearby) for word in
               ["subscribe", "subscription", "newsletter", "membership", "recurring", "renew"]):
            result.append({
                "name": "Pre-ticked Subscription",
                "icon": "☑️",
                "severity": "HIGH",
                "weight": 30,
                "description": "A subscription-related checkbox was already selected in the HTML.",
                "key": "subscription",
            })
            break
    return result


def calculate_score(findings):
    # Count each rule once and cap at 100.
    score = sum(item["weight"] for item in findings)
    return min(score, 100)


def severity_for(score):
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    if score > 0:
        return "LOW"
    return "NONE"


def build_report(result):
    lines = [
        "DARK PATTERN & ONLINE FRAUD DETECTOR",
        "Part 1 - Rule Based Scan",
        "=" * 55,
        f"URL: {result['final_url']}",
        f"Scan time: {result['scan_time']}",
        f"Risk score: {result['risk_score']}%",
        f"Severity: {result['severity']}",
        "",
        "DETECTED PATTERNS",
        "-" * 55,
    ]

    if result["patterns"]:
        for p in result["patterns"]:
            lines += [f"- {p['name']} [{p['severity']}]", f"  {p['description']}"]
    else:
        lines.append("- No configured rule matched.")

    lines += ["", "EVIDENCE", "-" * 55]
    for e in result["evidence"]:
        lines.append(f"- {e['label']}: {e['snippet']}")

    lines += [
        "",
        "NOTE",
        "-" * 55,
        "A rule match is an indicator for investigation and is not proof that a website is fraudulent.",
    ]
    return "\n".join(lines)


def analyze_url(url):
    try:
        response = fetch_page(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = clean_text(soup)

        findings, evidence = detect_rules(text)

        checkbox_findings = detect_checkboxes(soup)
        existing_keys = {p["key"] for p in findings}
        for p in checkbox_findings:
            if p["key"] not in existing_keys:
                findings.append(p)
                existing_keys.add(p["key"])
                evidence.append({
                    "snippet": "Pre-ticked subscription-related checkbox found in HTML.",
                    "label": p["name"],
                })

        score = calculate_score(findings)
        severity = severity_for(score)

        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        result = {
            "success": True,
            "final_url": response.url,
            "title": title,
            "risk_score": score,
            "severity": severity,
            "patterns": findings,
            "evidence": evidence[:10],
            "html_kb": round(len(response.content) / 1024, 1),
            "status_code": response.status_code,
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        result["report_text"] = build_report(result)
        return result

    except requests.exceptions.RequestException as exc:
        return {
            "success": False,
            "error": (
                "Could not fetch this website. It may block automated requests, "
                "require JavaScript, be offline, or have an invalid URL.\n\n"
                f"Technical detail: {exc}"
            ),
        }
    except Exception as exc:
        return {
            "success": False,
            "error": f"Analysis failed: {exc}",
        }
