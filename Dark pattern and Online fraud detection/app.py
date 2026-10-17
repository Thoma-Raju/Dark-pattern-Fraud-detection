import streamlit as st
from urllib.parse import urlparse
from src.analyzer import analyze_url

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dark Pattern Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session state defaults ────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "scan_history" not in st.session_state:
    st.session_state["scan_history"] = []

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #071426;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091b35 0%, #061329 100%);
    border-right: 1px solid #18365c;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Hide default streamlit button styling inside sidebar, replace with nav look */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #d9e7f8 !important;
    text-align: left !important;
    padding: 11px 14px !important;
    border-radius: 10px !important;
    margin: 4px 0 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    width: 100% !important;
    box-shadow: none !important;
    transition: background 0.18s ease !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(21,87,187,0.35) !important;
    color: white !important;
}

section[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
    border: none !important;
}

.nav-active-btn > button {
    background: linear-gradient(90deg, #1557bb, #0f47a0) !important;
    color: white !important;
}

.brand {
    padding: 8px 8px 20px 8px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: #eef7ff;
    color: #0b4fa3;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    margin-bottom: 12px;
}

.brand-title {
    color: white;
    font-size: 20px;
    line-height: 1.15;
    font-weight: 800;
}

.brand-sub {
    color: #a9c1df;
    font-size: 13px;
    line-height: 1.55;
    margin-top: 10px;
}

.side-bottom {
    color: #8da8c9;
    text-align: center;
    font-size: 12px;
    padding: 12px 8px;
}

/* ── Typography ── */
h1 {
    color: #f5f9ff;
    font-size: 35px !important;
    font-weight: 800 !important;
    margin-bottom: 0.15rem !important;
}

.subtitle {
    color: #9eb9dc;
    font-size: 15px;
    margin-bottom: 18px;
}

.part-badge {
    display: inline-block;
    background: #0753b8;
    color: white;
    padding: 7px 13px;
    border-radius: 18px;
    font-weight: 700;
    font-size: 12px;
    margin-left: 10px;
    vertical-align: middle;
}

/* ── URL card / input ── */
.url-card {
    background: linear-gradient(135deg, #0d213d, #0a1a31);
    border: 1px solid #234b7b;
    border-radius: 12px;
    padding: 17px;
    margin-bottom: 15px;
}

.label {
    color: #dfeeff;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 6px;
}

.example {
    color: #89a9cf;
    font-size: 12px;
    margin-top: 6px;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #122746 !important;
    color: #f4f8ff !important;
    border: 1px solid #2e5687 !important;
    border-radius: 9px !important;
}

.stButton > button {
    background: linear-gradient(90deg, #0b75ff, #1260dc);
    color: white;
    border: 0;
    border-radius: 9px;
    font-weight: 700;
    min-height: 42px;
}

/* ── Result banners ── */
.result-danger {
    background: linear-gradient(135deg, #271a2a, #1d1727);
    border: 1px solid #f2385c;
    border-radius: 12px;
    padding: 18px;
    margin-top: 5px;
}

.result-safe {
    background: linear-gradient(135deg, #102a2b, #0d2227);
    border: 1px solid #23c98a;
    border-radius: 12px;
    padding: 18px;
    margin-top: 5px;
}

.result-title {
    color: #ff4264;
    font-size: 20px;
    font-weight: 800;
}

.result-safe .result-title {
    color: #29d995;
}

.result-sub {
    color: #c3d2e4;
    font-size: 13px;
    margin-top: 6px;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(145deg, #0e2039, #0a192e);
    border: 1px solid #21436b;
    border-radius: 10px;
    padding: 14px;
    min-height: 115px;
}

.metric-label {
    color: #b2c8e2;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: white;
    font-size: 25px;
    font-weight: 800;
    margin-top: 10px;
}

.metric-caption {
    color: #ff516e;
    font-size: 12px;
    font-weight: 700;
}

/* ── Section / pattern cards ── */
.section-card {
    background: #091b31;
    border: 1px solid #1d426c;
    border-radius: 11px;
    padding: 15px;
    margin-top: 12px;
}

.section-title {
    color: #f2f7ff;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 12px;
}

.pattern {
    background: linear-gradient(90deg, #102744, #0c2038);
    border: 1px solid #1c436d;
    border-radius: 10px;
    padding: 13px;
    margin: 8px 0;
}

.pattern-name {
    color: #eef6ff;
    font-weight: 750;
    font-size: 14px;
}

.pattern-desc {
    color: #9fb8d6;
    font-size: 12px;
    line-height: 1.45;
    margin-top: 4px;
}

.high   { background: #ff3157; color: white; }
.medium { background: #f5bd21; color: #172033; }
.low    { background: #24c78a; color: #08251c; }
.none   { background: #2e5687; color: #c8ddf5; }

.tag {
    float: right;
    padding: 4px 9px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 800;
}

.evidence {
    background: #061426;
    border: 1px solid #173b63;
    border-radius: 9px;
    padding: 13px;
    color: #86b9e8;
    font-family: Consolas, monospace;
    font-size: 12px;
    line-height: 1.75;
    white-space: pre-wrap;
}

.arrow {
    color: #ff4c68;
    font-weight: 800;
}

/* ── Info / summary cards ── */
.info-card {
    background: #0a1d34;
    border: 1px solid #20476f;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 12px;
}

.info-title {
    color: white;
    font-weight: 800;
    font-size: 15px;
    margin-bottom: 8px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    color: #a9c0dc;
    font-size: 12px;
    padding: 8px 0;
    border-bottom: 1px solid #183451;
}

.info-row:last-child { border-bottom: 0; }

.risk-big {
    color: #ff3d60;
    font-size: 22px;
    font-weight: 800;
}

.progress {
    height: 10px;
    background: #183554;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #31e56f, #ffd429, #ff3c5d);
    border-radius: 10px;
}

.safe-box {
    border: 1px solid #1268a8;
    background: #08233b;
    border-radius: 10px;
    padding: 13px;
    color: #b5d8f4;
    font-size: 12px;
    line-height: 1.5;
}

.small-note {
    color: #7e9abb;
    font-size: 11px;
}

/* ── Report table ── */
.report-row {
    background: linear-gradient(90deg, #0e2341, #091c35);
    border: 1px solid #1e426a;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 8px 0;
    display: flex;
    align-items: center;
    gap: 14px;
}

.report-url  { color: #7ec8ff; font-size: 13px; font-weight: 600; flex: 1; word-break: break-all; }
.report-time { color: #6f8fae; font-size: 11px; white-space: nowrap; }
.report-score{ color: white; font-size: 18px; font-weight: 800; min-width: 55px; text-align: right; }

/* ── About page ── */
.about-card {
    background: linear-gradient(145deg, #0c1f38, #091829);
    border: 1px solid #1f4571;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 18px;
}

.about-title {
    color: #e8f4ff;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 10px;
}

.about-body {
    color: #9dbad8;
    font-size: 13px;
    line-height: 1.75;
}

.rule-card {
    background: #0d2040;
    border: 1px solid #1c4272;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 9px 0;
}

.rule-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}

.rule-icon  { font-size: 22px; }
.rule-name  { color: #e6f2ff; font-weight: 700; font-size: 14px; }
.rule-weight{ margin-left: auto; }
.rule-desc  { color: #8fb5d9; font-size: 12px; line-height: 1.6; }

.tech-badge {
    display: inline-block;
    background: #0e3060;
    color: #7ec8ff;
    border: 1px solid #1d5499;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    margin: 4px;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════

def go(page: str):
    st.session_state["page"] = page
    st.rerun()


def render_result_block(result, url):
    """Shared function that renders the full analysis result dashboard."""
    score    = result["risk_score"]
    severity = result["severity"]
    patterns = result["patterns"]

    if severity == "HIGH":
        result_class = "result-danger"
        title = "⚠️ POTENTIAL DARK PATTERNS DETECTED"
        sub   = "We found multiple indicators of deceptive design and potentially fraudulent behavior on this website."
    elif severity == "MEDIUM":
        result_class = "result-danger"
        title = "⚠️ DARK PATTERN INDICATORS FOUND"
        sub   = "Some design patterns may pressure, mislead, or manipulate users."
    else:
        result_class = "result-safe"
        title = "✓ NO MAJOR DARK PATTERNS DETECTED"
        sub   = "The rule-based scan did not find strong indicators in the fetched page."

    st.markdown(f"""
    <div class="{result_class}">
        <div class="result-title">{title}
            <span class="tag {'high' if severity=='HIGH' else 'medium' if severity=='MEDIUM' else 'low'}">{severity}</span>
        </div>
        <div class="result-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Indicators</div>
            <div class="metric-value">{len(patterns)}</div>
            <div class="metric-caption">Detected</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Risk Score</div>
            <div class="metric-value">{score}%</div>
            <div class="metric-caption">{severity.title()}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Page Status</div>
            <div class="metric-value">{result.get("status_code", 200)}</div>
            <div class="metric-caption">Fetched</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">HTML Size</div>
            <div class="metric-value">{result["html_kb"]} KB</div>
            <div class="metric-caption">Analyzed</div>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1.65, 0.9])

    with left:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">🔍 Detected Dark Patterns</div>
        """, unsafe_allow_html=True)

        if patterns:
            for p in patterns:
                cls = p["severity"].lower()
                st.markdown(f"""
                <div class="pattern">
                    <span class="tag {cls}">{p["severity"]}</span>
                    <div class="pattern-name">{p["icon"]} {p["name"]}</div>
                    <div class="pattern-desc">{p["description"]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="pattern">
                <div class="pattern-name">✓ No rule matched</div>
                <div class="pattern-desc">No configured dark-pattern indicators were detected.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
            <div class="section-title">⌘ Evidence Found</div>
            <div class="evidence">
        """, unsafe_allow_html=True)

        if result["evidence"]:
            for e in result["evidence"]:
                st.markdown(
                    f'<div>{e["snippet"]} <span class="arrow">→ {e["label"]}</span></div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<div>No matching evidence was extracted.</div>", unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with right:
        host = urlparse(result["final_url"]).netloc or urlparse(url).netloc
        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">📄 Website Analysis Summary</div>
            <div class="info-row"><span>Website</span><span>{host}</span></div>
            <div class="info-row"><span>Protocol</span><span>{urlparse(result["final_url"]).scheme.upper()}</span></div>
            <div class="info-row"><span>Title</span><span>{result["title"][:35] or "Not available"}</span></div>
            <div class="info-row"><span>Scan Time</span><span>{result["scan_time"]}</span></div>
            <div class="info-row"><span>Indicators</span><span>{len(patterns)}</span></div>
        </div>
        """, unsafe_allow_html=True)

        counts = {}
        for p in patterns:
            counts[p["name"]] = counts.get(p["name"], 0) + 1

        rows = "".join(
            f'<div class="info-row"><span>{k}</span><span>{v}</span></div>'
            for k, v in counts.items()
        ) or '<div class="info-row"><span>None</span><span>0</span></div>'

        color_cls = "high" if severity == "HIGH" else "medium" if severity == "MEDIUM" else "low"

        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">🎯 Detected Features</div>
            {rows}
        </div>

        <div class="info-card">
            <div class="info-title">⚠️ Risk Level</div>
            <div class="risk-big" style="color:{'#ff3d60' if severity=='HIGH' else '#f5bd21' if severity=='MEDIUM' else '#24c78a'}">
                {severity} RISK <span style="float:right;">{score}%</span>
            </div>
            <div class="progress"><div class="progress-fill" style="width:{score}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

        if severity == "HIGH":
            advice = "Verify the offer independently, check the final price, and avoid entering payment details until the warning signs are understood."
        elif severity == "MEDIUM":
            advice = "Review pricing, subscription terms, checkboxes, and urgency messages before continuing."
        else:
            advice = "Continue using normal safe-browsing practices and verify important transactions."

        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">🛡️ Stay Safe Online</div>
            <div class="safe-box">{advice}</div>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            "📄 Download Scan Report",
            data=result["report_text"],
            file_name="dark_pattern_scan_report.txt",
            mime="text/plain",
            use_container_width=True,
            key=f"dl_{result['scan_time'].replace(' ', '_')}_{host}",
        )

        st.markdown('<div class="small-note">Part 1 uses transparent rule-based detection. A matched rule is an indicator for investigation, not proof of fraud.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════════════════════════════════════════════

page = st.session_state["page"]

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div class="brand-title">Dark Pattern &<br>Online Fraud Detector</div>
        <div class="brand-sub">Detect deceptive website designs<br>and protect users from online fraud.</div>
    </div>
    """, unsafe_allow_html=True)

    for label, key, icon in [
        ("Home",         "home",   "⌂"),
        ("Scan Website", "scan",   "🔗"),
        ("Report",       "report", "▤"),
        ("About",        "about",  "ⓘ"),
    ]:
        active = page == key
        css_class = "nav-active-btn" if active else ""
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            go(key)
        st.markdown("</div>", unsafe_allow_html=True)

    history_count = len(st.session_state["scan_history"])
    st.markdown(f"""
    <div class="side-bottom">
        🛡️<br><br>Safer Browsing · Better Decisions<br>
        <span style="color:#4a7bb0;font-size:10px;">{history_count} scan(s) this session</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════

if page == "home":
    st.markdown("""
    <h1>Dark Pattern & Online Fraud Detector</h1>
    <div class="subtitle">Enter a website URL to analyze for dark patterns and potential online fraud.</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="url-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown('<div class="label">Website URL</div>', unsafe_allow_html=True)
        url = st.text_input(
            "Website URL",
            value="",
            placeholder="https://www.example.com",
            label_visibility="collapsed",
            key="home_url",
        )
        st.markdown(
            '<div class="example">🌐 Examples: https://www.amazon.com &nbsp; | &nbsp; '
            'https://www.flipkart.com &nbsp; | &nbsp; https://www.example.com</div>',
            unsafe_allow_html=True
        )
    with c2:
        st.write("")
        analyze = st.button("🔎 Analyze", use_container_width=True, key="home_analyze")
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze:
        if not url.strip():
            st.warning("Please enter a website URL.")
            st.stop()

        with st.spinner("Fetching and analyzing website HTML…"):
            result = analyze_url(url.strip())

        if not result["success"]:
            st.error(result["error"])
            st.stop()

        # Persist to history
        st.session_state["scan_history"].append({**result, "queried_url": url.strip()})
        render_result_block(result, url.strip())

    else:
        st.markdown("""
        <div class="section-card" style="margin-top:20px;">
            <div class="section-title">🚀 How it works</div>
            <div style="color:#a9c0dc;font-size:13px;line-height:1.8;">
            1. Enter a public website URL.<br>
            2. The application fetches the page HTML.<br>
            3. Rule-based checks search for urgency, fake countdowns,
               hidden/additional charges, subscription pressure, manipulative wording,
               and pre-ticked consent checkboxes.<br>
            4. The dashboard calculates a transparent risk score and shows the evidence.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="about-card" style="margin-top:12px;">
                <div class="about-title">⏱️ Fake Countdown Timers</div>
                <div class="about-body">Artificial urgency using timers or "only X minutes left" messages to pressure immediate decisions.</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="about-card" style="margin-top:12px;">
                <div class="about-title">💰 Hidden Charges</div>
                <div class="about-body">Service fees, handling fees, and convenience charges introduced late in the checkout process.</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="about-card" style="margin-top:12px;">
                <div class="about-title">☑️ Pre-ticked Subscriptions</div>
                <div class="about-body">Checkboxes already selected for recurring payments or newsletters without user intent.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SCAN WEBSITE
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "scan":
    st.markdown("""
    <h1>Scan Website</h1>
    <div class="subtitle">Run a full dark-pattern scan on any public website — or scan multiple URLs in batch mode.</div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔗 Single URL Scan", "📋 Batch URL Scan"])

    # ── Single URL ────────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="url-card">', unsafe_allow_html=True)
        sc1, sc2 = st.columns([5, 1])
        with sc1:
            st.markdown('<div class="label">Website URL</div>', unsafe_allow_html=True)
            scan_url = st.text_input(
                "scan_url",
                value="",
                placeholder="https://www.example.com",
                label_visibility="collapsed",
                key="scan_single_url",
            )
            st.markdown(
                '<div class="example">🌐 Paste any public URL — the app fetches live HTML and applies all detection rules.</div>',
                unsafe_allow_html=True
            )
        with sc2:
            st.write("")
            scan_btn = st.button("🔎 Scan", use_container_width=True, key="scan_single_btn")
        st.markdown('</div>', unsafe_allow_html=True)

        if scan_btn:
            if not scan_url.strip():
                st.warning("Please enter a website URL.")
            else:
                with st.spinner("Fetching and analyzing website HTML…"):
                    result = analyze_url(scan_url.strip())

                if not result["success"]:
                    st.error(result["error"])
                else:
                    st.session_state["scan_history"].append({**result, "queried_url": scan_url.strip()})
                    render_result_block(result, scan_url.strip())

    # ── Batch URL ─────────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="url-card">', unsafe_allow_html=True)
        st.markdown('<div class="label">URLs to Scan (one per line, max 10)</div>', unsafe_allow_html=True)
        batch_text = st.text_area(
            "batch_urls",
            value="",
            placeholder="https://www.amazon.com\nhttps://www.flipkart.com\nhttps://www.example.com",
            height=180,
            label_visibility="collapsed",
            key="scan_batch_urls",
        )
        batch_btn = st.button("🔎 Run Batch Scan", key="scan_batch_btn")
        st.markdown('</div>', unsafe_allow_html=True)

        if batch_btn:
            urls = [u.strip() for u in batch_text.strip().splitlines() if u.strip()]
            if not urls:
                st.warning("Please enter at least one URL.")
            else:
                urls = urls[:10]
                batch_results = []
                progress = st.progress(0, text="Starting batch scan…")

                for i, u in enumerate(urls):
                    progress.progress((i) / len(urls), text=f"Scanning {u[:60]}…")
                    r = analyze_url(u)
                    batch_results.append((u, r))
                    if r["success"]:
                        st.session_state["scan_history"].append({**r, "queried_url": u})

                progress.progress(1.0, text="Batch scan complete!")

                st.markdown('<div class="section-card"><div class="section-title">📊 Batch Scan Results</div>', unsafe_allow_html=True)

                for u, r in batch_results:
                    if r["success"]:
                        sev   = r["severity"]
                        score = r["risk_score"]
                        col   = "#ff3d60" if sev == "HIGH" else "#f5bd21" if sev == "MEDIUM" else "#24c78a"
                        cls   = sev.lower()
                        st.markdown(f"""
                        <div class="report-row">
                            <div class="report-url">🔗 {u}</div>
                            <div class="report-time">{r["scan_time"]}</div>
                            <span class="tag {cls}" style="float:none;min-width:60px;text-align:center;">{sev}</span>
                            <div class="report-score" style="color:{col};">{score}%</div>
                        </div>
                        """, unsafe_allow_html=True)

                        with st.expander(f"View details — {u[:70]}"):
                            render_result_block(r, u)
                    else:
                        st.markdown(f"""
                        <div class="report-row">
                            <div class="report-url">❌ {u}</div>
                            <div class="report-time" style="color:#ff6680;">Failed to fetch</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REPORT
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "report":
    st.markdown("""
    <h1>Scan History &amp; Reports</h1>
    <div class="subtitle">All scans performed during this session — view details, compare results, and download reports.</div>
    """, unsafe_allow_html=True)

    history = st.session_state["scan_history"]

    if not history:
        st.markdown("""
        <div class="section-card" style="margin-top:20px;text-align:center;padding:40px;">
            <div style="font-size:48px;margin-bottom:16px;">📭</div>
            <div class="section-title">No Scans Yet</div>
            <div style="color:#7e9abb;font-size:13px;">Run a scan from the Home or Scan Website page to see results here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary stats
        high_count   = sum(1 for r in history if r["severity"] == "HIGH")
        medium_count = sum(1 for r in history if r["severity"] == "MEDIUM")
        low_count    = sum(1 for r in history if r["severity"] in ("LOW", "NONE"))
        avg_score    = round(sum(r["risk_score"] for r in history) / len(history), 1)

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Scans</div>
                <div class="metric-value">{len(history)}</div>
                <div class="metric-caption">This Session</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">High Risk</div>
                <div class="metric-value" style="color:#ff3d60;">{high_count}</div>
                <div class="metric-caption">Sites</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Medium Risk</div>
                <div class="metric-value" style="color:#f5bd21;">{medium_count}</div>
                <div class="metric-caption">Sites</div>
            </div>
            """, unsafe_allow_html=True)
        with s4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Risk Score</div>
                <div class="metric-value">{avg_score}%</div>
                <div class="metric-caption">Across All Scans</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # Action bar
        ac1, ac2 = st.columns([1, 5])
        with ac1:
            if st.button("🗑️ Clear History", key="report_clear"):
                st.session_state["scan_history"] = []
                st.rerun()
        with ac2:
            all_text = "\n\n" + ("=" * 60) + "\n\n".join(r.get("report_text", "") for r in history)
            st.download_button(
                "📥 Download All Reports",
                data=all_text,
                file_name="all_scan_reports.txt",
                mime="text/plain",
                key="report_download_all",
            )

        st.markdown('<div class="section-card"><div class="section-title">🗂️ Scan Records</div>', unsafe_allow_html=True)

        for idx, r in enumerate(reversed(history)):
            sev   = r["severity"]
            score = r["risk_score"]
            col   = "#ff3d60" if sev == "HIGH" else "#f5bd21" if sev == "MEDIUM" else "#24c78a"
            cls   = sev.lower()
            u     = r.get("queried_url", r.get("final_url", "Unknown"))

            st.markdown(f"""
            <div class="report-row">
                <div class="report-url">🔗 {u}</div>
                <div class="report-time">🕒 {r["scan_time"]}</div>
                <span class="tag {cls}" style="float:none;min-width:60px;text-align:center;">{sev}</span>
                <div class="report-score" style="color:{col};">{score}%</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"#{len(history) - idx}  View full report — {u[:70]}"):
                render_result_block(r, u)

        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ═══════════════════════════════════════════════════════════════════════════════

elif page == "about":
    st.markdown("""
    <h1>About This Tool</h1>
    <div class="subtitle">Understand how the Dark Pattern & Online Fraud Detector works under the hood.</div>
    """, unsafe_allow_html=True)

    col_main, col_side = st.columns([1.8, 1])

    with col_main:
        st.markdown("""
        <div class="about-card">
            <div class="about-title">🛡️ What Is This?</div>
            <div class="about-body">
                The <strong style="color:#e8f4ff;">Dark Pattern & Online Fraud Detector</strong> is a
                rule-based web analysis tool built as Part 1 of a multi-phase project on detecting
                deceptive design practices (dark patterns) and online fraud indicators.<br><br>
                It fetches the live HTML of any public website and applies a set of expert-designed
                regular-expression rules to flag language and structural elements commonly associated
                with manipulative or deceptive user interface patterns.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <div class="about-title">⚙️ How Detection Works</div>
            <div class="about-body">
                <strong style="color:#e8f4ff;">Step 1 — Fetch</strong><br>
                The app sends an HTTP GET request (with a real browser User-Agent) to the target URL
                and follows redirects. The full HTML response is retrieved.<br><br>
                <strong style="color:#e8f4ff;">Step 2 — Parse</strong><br>
                BeautifulSoup extracts all visible text, stripping scripts, styles, and SVGs.
                The DOM is also inspected for pre-checked HTML checkboxes.<br><br>
                <strong style="color:#e8f4ff;">Step 3 — Match</strong><br>
                Each detection rule applies its regular-expression patterns (case-insensitive) to the
                cleaned text. At least one match triggers that rule.<br><br>
                <strong style="color:#e8f4ff;">Step 4 — Score</strong><br>
                Matched rules contribute their weight to a cumulative risk score (capped at 100%).
                The severity threshold determines the HIGH / MEDIUM / LOW / NONE classification.<br><br>
                <strong style="color:#e8f4ff;">Step 5 — Report</strong><br>
                Results are presented with evidence snippets, a risk gauge, and a downloadable
                plain-text report for documentation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Detection rules breakdown
        st.markdown("""
        <div class="about-card">
            <div class="about-title">📋 Detection Rules</div>
        """, unsafe_allow_html=True)

        rules_info = [
            ("⏱️", "Fake Countdown Timer",      "HIGH",   30, "Countdown timers, 'only X minutes left', and similar urgency phrases that manufacture false time pressure."),
            ("💰", "Hidden Charges",             "HIGH",   25, "Service fees, handling fees, convenience fees, and processing fees introduced late in the purchasing flow."),
            ("☑️", "Pre-ticked Subscription",   "HIGH",   30, "Auto-renew, recurring billing, newsletter, or membership language — especially in combination with pre-checked checkboxes."),
            ("⚡", "Urgency Language",           "MEDIUM", 15, "Scarcity or pressure phrases like 'limited time', 'only X left', 'act now', 'last chance', and 'hurry'."),
            ("⚠️", "Manipulative Wording",      "MEDIUM", 10, "Emotionally exploitative language such as 'you'll regret', 'missing out', 'exclusive deal', 'secret offer', 'claim before'."),
        ]

        for icon, name, sev, weight, desc in rules_info:
            cls = sev.lower()
            st.markdown(f"""
            <div class="rule-card">
                <div class="rule-header">
                    <span class="rule-icon">{icon}</span>
                    <span class="rule-name">{name}</span>
                    <span class="rule-weight"><span class="tag {cls}" style="float:none;">{sev} · {weight}pts</span></span>
                </div>
                <div class="rule-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <div class="about-title">📊 Risk Score Thresholds</div>
            <div class="about-body">
                <table style="width:100%;border-collapse:collapse;color:#9dbad8;">
                    <tr style="border-bottom:1px solid #1f4571;">
                        <th style="text-align:left;padding:8px 0;color:#e8f4ff;">Score Range</th>
                        <th style="text-align:left;padding:8px 0;color:#e8f4ff;">Severity</th>
                        <th style="text-align:left;padding:8px 0;color:#e8f4ff;">Meaning</th>
                    </tr>
                    <tr style="border-bottom:1px solid #1a3a5c;">
                        <td style="padding:8px 0;">70% – 100%</td>
                        <td style="padding:8px 0;"><span class="tag high" style="float:none;">HIGH</span></td>
                        <td style="padding:8px 0;">Multiple strong dark-pattern indicators. Investigate before transacting.</td>
                    </tr>
                    <tr style="border-bottom:1px solid #1a3a5c;">
                        <td style="padding:8px 0;">40% – 69%</td>
                        <td style="padding:8px 0;"><span class="tag medium" style="float:none;">MEDIUM</span></td>
                        <td style="padding:8px 0;">Some indicators present. Review terms and pricing carefully.</td>
                    </tr>
                    <tr style="border-bottom:1px solid #1a3a5c;">
                        <td style="padding:8px 0;">1% – 39%</td>
                        <td style="padding:8px 0;"><span class="tag low" style="float:none;">LOW</span></td>
                        <td style="padding:8px 0;">Minimal indicators found. Normal browsing caution advised.</td>
                    </tr>
                    <tr>
                        <td style="padding:8px 0;">0%</td>
                        <td style="padding:8px 0;"><span class="tag none" style="float:none;">NONE</span></td>
                        <td style="padding:8px 0;">No rule matched. No evidence of dark patterns detected.</td>
                    </tr>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_side:
        st.markdown("""
        <div class="about-card">
            <div class="about-title">🛠️ Tech Stack</div>
            <div style="margin-top:8px;">
                <span class="tech-badge">🐍 Python 3.10+</span>
                <span class="tech-badge">🎈 Streamlit</span>
                <span class="tech-badge">🌐 Requests</span>
                <span class="tech-badge">🍜 BeautifulSoup4</span>
                <span class="tech-badge">🔎 RegEx</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <div class="about-title">⚠️ Disclaimer</div>
            <div class="about-body">
                This tool is provided for <strong style="color:#e8f4ff;">educational and research purposes</strong> only.<br><br>
                A rule match is an <em>indicator for investigation</em> — not proof that a website is
                fraudulent or malicious. Many legitimate websites may use language that matches
                one or more rules (e.g., subscription services, auction sites).<br><br>
                Always verify findings independently and exercise your own judgement before
                making financial or personal-data decisions online.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <div class="about-title">🚀 Roadmap</div>
            <div class="about-body">
                <strong style="color:#e8f4ff;">Part 1 ✅</strong> — Rule-based detection<br>
                (Current version)<br><br>
                <strong style="color:#7e9abb;">Part 2 🔜</strong> — ML-based classifier<br>
                Trained model on labeled dark-pattern datasets.<br><br>
                <strong style="color:#7e9abb;">Part 3 🔜</strong> — Browser extension<br>
                Real-time detection while browsing.<br><br>
                <strong style="color:#7e9abb;">Part 4 🔜</strong> — Visual screenshot analysis<br>
                Computer-vision-based UI pattern detection.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <div class="about-title">📚 What Are Dark Patterns?</div>
            <div class="about-body">
                Dark patterns are user interface design choices that trick or manipulate users into
                doing things they didn't intend to — like signing up for a subscription, sharing
                more data than necessary, or spending more money.<br><br>
                The term was coined by UX designer <strong style="color:#e8f4ff;">Harry Brignull</strong> in 2010.
                Regulators worldwide (EU, FTC, CCI) are increasingly taking action against companies
                that deploy such practices.
            </div>
        </div>
        """, unsafe_allow_html=True)
