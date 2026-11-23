from pathlib import Path
import streamlit as st
from parser import parse_email_content
from detector import analyze_phishing_indicators

st.set_page_config(page_title="PhishGuard SOC", page_icon="🛡️", layout="wide")

css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ PhishGuard SOC - Threat Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7dd3fc;'>Created by Moussa Hassan — Automated Email Triage, Heuristic Analysis & Social Engineering Defense System</p>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Email Analysis Triage",
    "📚 Phishing Threat Guide",
    "👨‍💻 About Project",
    "🎯 AMIT Proposal & Compliance"
])

with tab1:
    col_input1, col_input2 = st.columns([2, 1])
    with col_input1:
        st.subheader("📥 Raw Email Input")
        default_email = st.session_state.get("sample_text", "From: security-alert@domain.com\nSubject: Urgent Action Required...\n\nDear user...")
        email_input = st.text_area("Paste Raw Email Content / Headers Here:", value=default_email, height=240)
        analyze_btn = st.button("🚀 Run Phishing Analysis", type="primary", use_container_width=True)

    with col_input2:
        st.subheader("💡 Quick Sample Loader")
        if st.button("Load Phishing Sample 🔴", use_container_width=True):
            st.session_state["sample_text"] = "From: security-alert@paypa1-update.com\nSubject: Urgent: Verify your account immediately!\n\nDear customer,\nWe detected unusual login attempts on your account. Please click the link below immediately:\nhttps://login.paypa1-update.com/auth/login?token=xyz123"
            st.rerun()
        if st.button("Load Clean Sample 🟢", use_container_width=True):
            st.session_state["sample_text"] = "From: newsletter@github.com\nSubject: Your weekly GitHub summary\n\nHi Moussa, here is your summary.\nhttps://github.com/settings/profile"
            st.rerun()

    if analyze_btn:
        if email_input.strip() == "":
            st.warning("Please paste an email content first!")
        else:
            with st.spinner("Analyzing email headers and heuristic indicators..."):
                parsed_data = parse_email_content(email_input)
                analysis_result = analyze_phishing_indicators(parsed_data)
            st.success("Analysis Complete Successfully!")
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader("📧 Metadata")
                st.write(f"**Sender:** `{parsed_data['sender']}`")
                st.write(f"**Subject:** `{parsed_data['subject']}`")
            with res_col2:
                st.subheader("⚠️ Verdict")
                score = analysis_result["risk_score"]
                verdict = analysis_result["verdict"]
                if score >= 60:
                    st.error(f"**{verdict}** (Score: {score}/100)")
                elif score >= 30:
                    st.warning(f"**{verdict}** (Score: {score}/100)")
                else:
                    st.success(f"**{verdict}** (Score: {score}/100)")

with tab2:
    st.markdown("""
    <div class="pg-info-center">
        <h3>📚 Email Phishing Threat Intelligence Guide</h3>
        <p>Phishing is a form of social engineering where attackers impersonate legitimate organizations to steal sensitive credentials.</p>
        <ul>
            <li><strong>Typosquatting:</strong> Using lookalike domains (e.g., paypa1.com).</li>
            <li><strong>Urgency &amp; Coercion:</strong> Inducing psychological panic.</li>
            <li><strong>Deceptive Links:</strong> Hiding malicious destinations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="pg-info-center">
        <h3>👨‍💻 Project Overview &amp; Architecture</h3>
        <p>PhishGuard SOC Engine developed by Moussa Hassan as a Graduation Project &amp; SOC Specialization.</p>
        <p>Stack: Python 3.12, Streamlit, Regex, Custom CSS Glassmorphism.</p>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="pg-info-center">
        <h3>🎯 AMIT Graduation Project Proposal Compliance</h3>
        <p>This project strictly implements the core modules outlined in the AMIT proposal:</p>
        <ol>
            <li>Automated Email Triage &amp; Ingestion</li>
            <li>URL &amp; Domain Analysis / Typosquatting</li>
            <li>Detection Engine &amp; Risk Scoring</li>
            <li>Enterprise Web Dashboard</li>
            <li>MITRE ATT&amp;CK T1566 Framework Mapping</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="amit-footer">
    <span>🛡️ PhishGuard SOC Project | Moussa Hassan | AMIT Graduation Standards | </span>
    <a href="https://amit-learning.com" target="_blank">Visit AMIT Website</a>
</div>
""", unsafe_allow_html=True)