"""
CipherVault – Educational Encryption & Decryption Toolkit
Main Streamlit Application

⚠️  EDUCATIONAL DISCLAIMER: The Caesar and Vigenère ciphers implemented here
    are classical ciphers suitable ONLY for learning purposes. They provide
    NO security against modern cryptanalysis. Never use them to protect
    sensitive information.
"""

import streamlit as st
import datetime

# ── Algorithm imports ──────────────────────────────────────────────
from algorithms.caesar import caesar_encrypt, caesar_decrypt, caesar_brute_force
from algorithms.vigenere import vigenere_encrypt, vigenere_decrypt
from algorithms.analysis import character_frequency

# ── Utility imports ────────────────────────────────────────────────
from utils.validators import (
    validate_caesar_shift,
    validate_vigenere_keyword,
    validate_text_input,
    validate_uploaded_file,
)
from utils.history import add_history_entry, clear_history

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Page configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="CipherVault – Encryption Toolkit",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Custom CSS – Dark cybersecurity theme
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
/* ── Import Google Fonts ───────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ────────────────────────────────────── */
:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2035;
    --bg-card-hover: #1e2642;
    --accent-cyan: #06b6d4;
    --accent-blue: #3b82f6;
    --accent-purple: #8b5cf6;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border-color: #1e293b;
    --gradient-cyan: linear-gradient(135deg, #06b6d4, #3b82f6);
    --gradient-purple: linear-gradient(135deg, #8b5cf6, #06b6d4);
    --shadow-glow: 0 0 20px rgba(6, 182, 212, 0.15);
}

/* ── Global Styles ─────────────────────────────────────── */
.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0a0e1a !important;
}

/* ── Force dark background on ALL Streamlit containers ─── */
.stApp > header,
.stApp [data-testid="stHeader"] {
    background-color: #0a0e1a !important;
}

.stApp [data-testid="stToolbar"] {
    background-color: transparent !important;
}

.stMain,
.stApp [data-testid="stAppViewContainer"],
.stApp [data-testid="stMain"],
.stApp .main,
.stApp .block-container,
.stApp [data-testid="stAppViewBlockContainer"],
.stApp [data-testid="stVerticalBlock"],
.stApp [data-testid="stBottomBlockContainer"],
.stApp [data-testid="stMainBlockContainer"] {
    background-color: #0a0e1a !important;
    color: var(--text-primary) !important;
}

/* ── Expander dark background ──────────────────────────── */
.stApp [data-testid="stExpander"],
.stApp [data-testid="stExpander"] details,
.stApp [data-testid="stExpander"] summary,
.stApp [data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
    background-color: #111827 !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
}

/* ── DataFrame / Table dark background ─────────────────── */
.stApp [data-testid="stDataFrame"],
.stApp [data-testid="stTable"] {
    background-color: #111827 !important;
}

/* ── File uploader dark ────────────────────────────────── */
.stApp [data-testid="stFileUploader"],
.stApp [data-testid="stFileUploaderDropzone"] {
    background-color: #0d1321 !important;
    border-color: rgba(6, 182, 212, 0.2) !important;
}

/* ── Download button dark ──────────────────────────────── */
.stApp .stDownloadButton button {
    background-color: #111827 !important;
    color: var(--text-primary) !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
}

.stApp .stDownloadButton button:hover {
    background-color: #1a2035 !important;
    border-color: #06b6d4 !important;
}

/* ── Markdown text color ───────────────────────────────── */
.stApp .stMarkdown, .stApp .stMarkdown p,
.stApp .stMarkdown li, .stApp .stMarkdown td,
.stApp .stMarkdown th {
    color: var(--text-secondary) !important;
}

.stApp .stMarkdown h1, .stApp .stMarkdown h2,
.stApp .stMarkdown h3, .stApp .stMarkdown h4,
.stApp .stMarkdown h5 {
    color: var(--text-primary) !important;
}

/* ── Alert / info / error boxes ────────────────────────── */
.stApp [data-testid="stAlert"] {
    background-color: #111827 !important;
}

/* ── Code block dark ───────────────────────────────────── */
.stApp .stCode, .stApp code {
    background-color: #0d1321 !important;
    color: #06b6d4 !important;
}

/* ── Radio / selectbox label color ─────────────────────── */
.stApp label, .stApp .stRadio label span,
.stApp [data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
}

/* ── Sidebar Styling ───────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #0a0e1a 100%) !important;
    border-right: 1px solid var(--border-color) !important;
}

section[data-testid="stSidebar"] .stRadio label {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Card Component ────────────────────────────────────── */
.cv-card {
    background: linear-gradient(145deg, #1a2035 0%, #151d30 100%);
    border: 1px solid rgba(6, 182, 212, 0.12);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
}

.cv-card:hover {
    border-color: rgba(6, 182, 212, 0.25);
    box-shadow: var(--shadow-glow);
    transform: translateY(-2px);
}

/* ── Hero Title ────────────────────────────────────────── */
.cv-hero {
    text-align: center;
    padding: 40px 20px 20px;
}

.cv-hero h1 {
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

.cv-hero p {
    color: var(--text-secondary);
    font-size: 1.15rem;
    font-weight: 300;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Section Headers ───────────────────────────────────── */
.cv-section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(6, 182, 212, 0.15);
}

.cv-section-header h2 {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.cv-section-header .icon {
    font-size: 1.6rem;
}

/* ── Metric Cards ──────────────────────────────────────── */
.cv-metric {
    background: linear-gradient(145deg, #1a2035 0%, #151d30 100%);
    border: 1px solid rgba(6, 182, 212, 0.1);
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
}

.cv-metric:hover {
    border-color: rgba(6, 182, 212, 0.3);
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.1);
}

.cv-metric .value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    background: var(--gradient-cyan);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.cv-metric .label {
    color: var(--text-secondary);
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 6px;
}

/* ── Status Badges ─────────────────────────────────────── */
.cv-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

.cv-badge-success {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.cv-badge-error {
    background: rgba(244, 63, 94, 0.12);
    color: #f43f5e;
    border: 1px solid rgba(244, 63, 94, 0.25);
}

.cv-badge-info {
    background: rgba(6, 182, 212, 0.12);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.25);
}

.cv-badge-warning {
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.25);
}

/* ── Output Box ────────────────────────────────────────── */
.cv-output {
    background: #0d1321;
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    color: #06b6d4;
    word-wrap: break-word;
    white-space: pre-wrap;
    line-height: 1.7;
    min-height: 60px;
}

/* ── Dashboard Feature Cards ───────────────────────────── */
.cv-feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-top: 16px;
}

.cv-feature {
    background: linear-gradient(145deg, #1a2035 0%, #151d30 100%);
    border: 1px solid rgba(6, 182, 212, 0.08);
    border-radius: 14px;
    padding: 22px 20px;
    text-align: center;
    transition: all 0.3s ease;
}

.cv-feature:hover {
    border-color: rgba(6, 182, 212, 0.25);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.cv-feature .icon {
    font-size: 2rem;
    margin-bottom: 10px;
}

.cv-feature h4 {
    color: var(--text-primary);
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0 0 6px 0;
}

.cv-feature p {
    color: var(--text-muted);
    font-size: 0.8rem;
    margin: 0;
    line-height: 1.5;
}

/* ── Educational Callout ───────────────────────────────── */
.cv-callout {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(6, 182, 212, 0.08) 100%);
    border-left: 4px solid #8b5cf6;
    border-radius: 0 12px 12px 0;
    padding: 18px 24px;
    margin: 16px 0;
    color: var(--text-secondary);
    font-size: 0.92rem;
    line-height: 1.7;
}

.cv-callout strong {
    color: #8b5cf6;
}

/* ── Disclaimer Banner ─────────────────────────────────── */
.cv-disclaimer {
    background: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 10px;
    padding: 14px 20px;
    color: #f59e0b;
    font-size: 0.82rem;
    text-align: center;
    margin-top: 12px;
}

/* ── History Table ─────────────────────────────────────── */
.cv-history-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(30, 41, 59, 0.6);
    transition: background 0.2s ease;
}

.cv-history-item:hover {
    background: rgba(6, 182, 212, 0.04);
}

/* ── Streamlit Widget Overrides ────────────────────────── */
.stTextArea textarea, .stTextInput input, .stNumberInput input {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: #0d1321 !important;
    border: 1px solid rgba(6, 182, 212, 0.2) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

.stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus {
    border-color: #06b6d4 !important;
    box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.15) !important;
}

div.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.25) !important;
}

.stSelectbox > div > div {
    background-color: #0d1321 !important;
    border: 1px solid rgba(6, 182, 212, 0.2) !important;
    border-radius: 10px !important;
}

/* ── Tabs Styling ──────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border-color);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    letter-spacing: 0.01em;
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
}

/* ── Expander Styling ──────────────────────────────────── */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* ── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #334155; }

/* ── Divider ───────────────────────────────────────────── */
.cv-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.3), transparent);
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Session state initialization
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "history" not in st.session_state:
    st.session_state.history = []
if "last_plaintext" not in st.session_state:
    st.session_state.last_plaintext = ""
if "last_result" not in st.session_state:
    st.session_state.last_result = ""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Sidebar Navigation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px;">
        <span style="font-size:2.5rem;">🔐</span>
        <h2 style="font-family:'Inter',sans-serif; font-weight:700;
                    background: linear-gradient(135deg, #06b6d4, #8b5cf6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text; margin: 8px 0 4px;">CipherVault</h2>
        <p style="color:#64748b; font-size:0.78rem; font-weight:500;
                  letter-spacing:0.08em; text-transform:uppercase;">
            Educational Crypto Toolkit</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cv-divider"></div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Dashboard",
            "🔒  Encrypt / Decrypt",
            "🔓  Brute Force Lab",
            "📊  Frequency Analysis",
            "📁  File Encryption",
            "📜  History",
            "📖  Learn Cryptography",
        ],
        label_visibility="collapsed",
    )

    st.markdown('<div class="cv-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cv-disclaimer">
        ⚠️ Classical ciphers are for <strong>educational use only</strong>.<br>
        They offer no real-world security.
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Dashboard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if page == "🏠  Dashboard":
    st.markdown("""
    <div class="cv-hero">
        <h1>🔐 CipherVault</h1>
        <p>An educational encryption &amp; decryption toolkit exploring classical
           cryptographic algorithms. Learn, experiment, and understand the
           foundations of information security.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cv-divider"></div>', unsafe_allow_html=True)

    # ── Quick stats ────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="cv-metric">
            <div class="value">2</div>
            <div class="label">Algorithms</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="cv-metric">
            <div class="value">7</div>
            <div class="label">Tools</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="cv-metric">
            <div class="value">{len(st.session_state.history)}</div>
            <div class="label">Operations</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="cv-metric">
            <div class="value">∞</div>
            <div class="label">Learning</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # ── Available algorithms ───────────────────────────────────
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">🧩</span>
        <h2>Available Algorithms</h2>
    </div>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
        <div class="cv-card">
            <h3 style="color:#06b6d4; margin-top:0;">🔑 Caesar Cipher</h3>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.7;">
                A substitution cipher that shifts each letter by a fixed number
                of positions. One of the oldest known ciphers, used by Julius Caesar.
            </p>
            <div style="margin-top:12px;">
                <span class="cv-badge cv-badge-info">Shift-based</span>
                <span class="cv-badge cv-badge-warning" style="margin-left:6px;">Brute-forceable</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class="cv-card">
            <h3 style="color:#8b5cf6; margin-top:0;">🗝️ Vigenère Cipher</h3>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.7;">
                A polyalphabetic cipher using a keyword to determine variable
                shifts. Once considered "le chiffre indéchiffrable" (the unbreakable cipher).
            </p>
            <div style="margin-top:12px;">
                <span class="cv-badge cv-badge-info">Keyword-based</span>
                <span class="cv-badge cv-badge-success" style="margin-left:6px;">Polyalphabetic</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Feature grid ───────────────────────────────────────────
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">⚡</span>
        <h2>Toolkit Features</h2>
    </div>
    <div class="cv-feature-grid">
        <div class="cv-feature">
            <div class="icon">🔒</div>
            <h4>Encrypt / Decrypt</h4>
            <p>Encode and decode messages with Caesar or Vigenère ciphers</p>
        </div>
        <div class="cv-feature">
            <div class="icon">🔓</div>
            <h4>Brute Force Lab</h4>
            <p>Crack Caesar ciphertexts by trying all 25 possible shifts</p>
        </div>
        <div class="cv-feature">
            <div class="icon">📊</div>
            <h4>Frequency Analysis</h4>
            <p>Analyze character distributions to identify patterns</p>
        </div>
        <div class="cv-feature">
            <div class="icon">📁</div>
            <h4>File Encryption</h4>
            <p>Encrypt and decrypt .txt files with download support</p>
        </div>
        <div class="cv-feature">
            <div class="icon">📜</div>
            <h4>Operation History</h4>
            <p>Track all encryption and decryption operations</p>
        </div>
        <div class="cv-feature">
            <div class="icon">📖</div>
            <h4>Learn Cryptography</h4>
            <p>Interactive lessons on classical cipher fundamentals</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("""
    <div class="cv-callout">
        <strong>🎓 Educational Purpose</strong><br>
        CipherVault is designed for learning. Classical ciphers like Caesar and
        Vigenère are historically important but trivially breakable by modern
        standards. Explore them to build foundational understanding of
        cryptographic concepts.
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Encrypt / Decrypt
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "🔒  Encrypt / Decrypt":
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">🔒</span>
        <h2>Encryption &amp; Decryption Workspace</h2>
    </div>
    """, unsafe_allow_html=True)

    # ── Algorithm selector ─────────────────────────────────────
    algorithm = st.selectbox(
        "Select Algorithm",
        ["Caesar Cipher", "Vigenère Cipher"],
        key="enc_algo",
    )

    # ── Key input ──────────────────────────────────────────────
    if algorithm == "Caesar Cipher":
        shift_input = st.number_input(
            "Shift Value (integer, positive or negative)",
            value=3, step=1, key="caesar_shift",
        )
    else:
        keyword_input = st.text_input(
            "Keyword (letters only)",
            value="KEY", key="vig_keyword",
        )

    # ── Text I/O ───────────────────────────────────────────────
    col_in, col_out = st.columns(2)

    with col_in:
        st.markdown("##### 📝 Input Text")
        input_text = st.text_area(
            "Enter text to encrypt or ciphertext to decrypt",
            height=200, key="enc_input",
            label_visibility="collapsed",
            placeholder="Type or paste your message here…",
        )

    with col_out:
        st.markdown("##### 📤 Output")
        output_placeholder = st.empty()

    # ── Action buttons ─────────────────────────────────────────
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        encrypt_btn = st.button("🔒 Encrypt", use_container_width=True, type="primary")
    with b2:
        decrypt_btn = st.button("🔓 Decrypt", use_container_width=True)
    with b3:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    with b4:
        verify_btn = st.button("✅ Verify Round-trip", use_container_width=True)

    # ── Processing ─────────────────────────────────────────────
    result_text = ""
    error_msg = ""

    if encrypt_btn:
        try:
            validate_text_input(input_text, "Plaintext")
            if algorithm == "Caesar Cipher":
                result_text = caesar_encrypt(input_text, int(shift_input))
                st.session_state.last_plaintext = input_text
                st.session_state.last_result = result_text
                st.session_state.history = add_history_entry(
                    st.session_state.history, "Caesar", "Encrypt",
                    f"Shift = {int(shift_input)}"
                )
            else:
                kw = validate_vigenere_keyword(keyword_input)
                result_text = vigenere_encrypt(input_text, kw)
                st.session_state.last_plaintext = input_text
                st.session_state.last_result = result_text
                st.session_state.history = add_history_entry(
                    st.session_state.history, "Vigenère", "Encrypt",
                    f"Keyword length = {len(kw)}"
                )
        except ValueError as e:
            error_msg = str(e)

    elif decrypt_btn:
        try:
            validate_text_input(input_text, "Ciphertext")
            if algorithm == "Caesar Cipher":
                result_text = caesar_decrypt(input_text, int(shift_input))
                st.session_state.last_result = result_text
                st.session_state.history = add_history_entry(
                    st.session_state.history, "Caesar", "Decrypt",
                    f"Shift = {int(shift_input)}"
                )
            else:
                kw = validate_vigenere_keyword(keyword_input)
                result_text = vigenere_decrypt(input_text, kw)
                st.session_state.last_result = result_text
                st.session_state.history = add_history_entry(
                    st.session_state.history, "Vigenère", "Decrypt",
                    f"Keyword length = {len(kw)}"
                )
        except ValueError as e:
            error_msg = str(e)

    elif clear_btn:
        st.session_state.last_plaintext = ""
        st.session_state.last_result = ""
        st.rerun()

    elif verify_btn:
        try:
            validate_text_input(input_text, "Plaintext")
            if algorithm == "Caesar Cipher":
                encrypted = caesar_encrypt(input_text, int(shift_input))
                decrypted = caesar_decrypt(encrypted, int(shift_input))
            else:
                kw = validate_vigenere_keyword(keyword_input)
                encrypted = vigenere_encrypt(input_text, kw)
                decrypted = vigenere_decrypt(encrypted, kw)

            if decrypted == input_text:
                st.markdown("""
                <div class="cv-badge cv-badge-success" style="font-size:1rem; padding:12px 24px;">
                    ✅ Verification Passed — Decrypted text matches original plaintext!
                </div>
                """, unsafe_allow_html=True)
                result_text = f"Encrypted: {encrypted}\nDecrypted: {decrypted}"
            else:
                st.markdown("""
                <div class="cv-badge cv-badge-error" style="font-size:1rem; padding:12px 24px;">
                    ❌ Verification Failed — Decrypted text does not match!
                </div>
                """, unsafe_allow_html=True)
                result_text = f"Encrypted: {encrypted}\nDecrypted: {decrypted}\n\n⚠ MISMATCH"
        except ValueError as e:
            error_msg = str(e)

    # ── Display result ─────────────────────────────────────────
    if error_msg:
        with col_out:
            output_placeholder.error(f"⚠️ {error_msg}")
    elif result_text:
        with col_out:
            output_placeholder.markdown(
                f'<div class="cv-output">{result_text}</div>',
                unsafe_allow_html=True,
            )
        # Copy-to-clipboard via st.code (Streamlit has built-in copy)
        with col_out:
            st.code(result_text, language=None)

    st.markdown("""
    <div class="cv-disclaimer">
        ⚠️ These classical ciphers are for <strong>educational purposes only</strong>.
        Do not use them to secure sensitive information.
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Brute Force Lab
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "🔓  Brute Force Lab":
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">🔓</span>
        <h2>Caesar Brute Force Lab</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cv-callout">
        <strong>🎓 Educational Demonstration</strong><br>
        A brute-force attack tries <em>every possible key</em> until the correct
        one is found. The Caesar cipher has only 25 possible keys, making it
        trivially breakable. This tool shows why key space matters!
    </div>
    """, unsafe_allow_html=True)

    bf_input = st.text_area(
        "Enter Caesar ciphertext to crack",
        height=120,
        placeholder="Paste your Caesar-encrypted message here…",
        key="bf_input",
    )

    if st.button("🔓 Run Brute Force Attack", type="primary", use_container_width=True):
        if bf_input.strip():
            results = caesar_brute_force(bf_input)

            st.session_state.history = add_history_entry(
                st.session_state.history, "Caesar", "Brute Force",
                "All 25 shifts tested"
            )

            st.markdown(f"""
            <div class="cv-badge cv-badge-success" style="padding:10px 20px;">
                ✅ Generated all 25 possible decryptions
            </div>
            """, unsafe_allow_html=True)

            st.markdown("")

            # Display as a table
            import pandas as pd
            df = pd.DataFrame(results)
            df.columns = ["Shift (Key)", "Decrypted Text"]
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=600,
            )
        else:
            st.error("⚠️ Please enter ciphertext to analyze.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Frequency Analysis
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📊  Frequency Analysis":
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">📊</span>
        <h2>Character Frequency Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cv-callout">
        <strong>🎓 Why Frequency Analysis Matters</strong><br>
        In English, the letter <strong>E</strong> appears ~13% of the time. By
        analyzing letter frequencies in ciphertext, analysts can identify patterns
        and potentially crack substitution ciphers.
    </div>
    """, unsafe_allow_html=True)

    freq_text = st.text_area(
        "Enter text to analyze",
        height=150,
        placeholder="Paste any text — plaintext or ciphertext — to see its character distribution…",
        key="freq_input",
    )

    if st.button("📊 Analyze Frequencies", type="primary", use_container_width=True):
        if freq_text.strip():
            stats = character_frequency(freq_text)

            # ── Metric cards ───────────────────────────────────
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="cv-metric">
                    <div class="value">{stats['total_chars']}</div>
                    <div class="label">Total Characters</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="cv-metric">
                    <div class="value">{stats['alpha_chars']}</div>
                    <div class="label">Alphabetic</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="cv-metric">
                    <div class="value">{stats['unique_chars']}</div>
                    <div class="label">Unique Letters</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("")

            # ── Bar chart ──────────────────────────────────────
            if stats["frequency"]:
                import pandas as pd
                freq_df = pd.DataFrame(
                    list(stats["frequency"].items()),
                    columns=["Letter", "Count"],
                )
                freq_df = freq_df.sort_values("Letter").reset_index(drop=True)

                st.markdown("##### 📊 Character Distribution")
                st.bar_chart(freq_df.set_index("Letter"), height=350)

                st.markdown("##### 📋 Frequency Table")
                st.dataframe(
                    freq_df.sort_values("Count", ascending=False).reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )

            st.session_state.history = add_history_entry(
                st.session_state.history, "Analysis", "Frequency",
                f"{stats['total_chars']} chars analyzed"
            )
        else:
            st.error("⚠️ Please enter text to analyze.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: File Encryption
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📁  File Encryption":
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">📁</span>
        <h2>File Encryption &amp; Decryption</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cv-callout">
        Upload a <strong>.txt</strong> file (max 1 MB) to encrypt or decrypt its
        contents. The original file is never modified — you download a new file
        with the result.
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload a .txt file",
        type=["txt"],
        key="file_upload",
    )

    if uploaded is not None:
        try:
            file_content = validate_uploaded_file(uploaded)
            st.markdown("##### 📄 File Content Preview")
            preview = file_content[:2000] + ("…" if len(file_content) > 2000 else "")
            st.text_area("File content", preview, height=150, disabled=True, key="file_preview")

            # ── Algorithm / key config ─────────────────────────
            file_algo = st.selectbox(
                "Algorithm", ["Caesar Cipher", "Vigenère Cipher"], key="file_algo"
            )

            if file_algo == "Caesar Cipher":
                file_shift = st.number_input("Shift", value=3, step=1, key="file_shift")
            else:
                file_kw = st.text_input("Keyword", value="KEY", key="file_kw")

            fc1, fc2 = st.columns(2)
            with fc1:
                file_enc = st.button("🔒 Encrypt File", use_container_width=True, type="primary")
            with fc2:
                file_dec = st.button("🔓 Decrypt File", use_container_width=True)

            if file_enc or file_dec:
                try:
                    if file_algo == "Caesar Cipher":
                        if file_enc:
                            output = caesar_encrypt(file_content, int(file_shift))
                            op = "Encrypt"
                        else:
                            output = caesar_decrypt(file_content, int(file_shift))
                            op = "Decrypt"
                        detail = f"Shift = {int(file_shift)}"
                        algo_name = "Caesar"
                    else:
                        kw = validate_vigenere_keyword(file_kw)
                        if file_enc:
                            output = vigenere_encrypt(file_content, kw)
                            op = "Encrypt"
                        else:
                            output = vigenere_decrypt(file_content, kw)
                            op = "Decrypt"
                        detail = f"Keyword length = {len(kw)}"
                        algo_name = "Vigenère"

                    st.session_state.history = add_history_entry(
                        st.session_state.history, algo_name, f"File {op}", detail
                    )

                    st.markdown("##### 📤 Result")
                    out_preview = output[:2000] + ("…" if len(output) > 2000 else "")
                    st.text_area("Output", out_preview, height=150, disabled=True, key="file_output")

                    suffix = "encrypted" if file_enc else "decrypted"
                    base = uploaded.name.rsplit(".", 1)[0]
                    dl_name = f"{base}_{suffix}.txt"
                    st.download_button(
                        f"⬇️ Download {suffix} file",
                        data=output,
                        file_name=dl_name,
                        mime="text/plain",
                        use_container_width=True,
                    )

                    st.markdown(f"""
                    <div class="cv-badge cv-badge-success" style="padding:10px 20px;">
                        ✅ File {op.lower()}ed successfully — download your result above.
                    </div>
                    """, unsafe_allow_html=True)

                except ValueError as e:
                    st.error(f"⚠️ {e}")

        except ValueError as e:
            st.error(f"⚠️ {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: History
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📜  History":
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">📜</span>
        <h2>Operation History</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cv-callout">
        Recent encryption and decryption operations are logged here for reference.
        <strong>No plaintext or keys are stored</strong> — only metadata.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = clear_history(st.session_state.history)
            st.rerun()

        import pandas as pd
        hist_df = pd.DataFrame(st.session_state.history)
        hist_df.columns = ["Timestamp", "Algorithm", "Operation", "Details"]
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#64748b;">
            <span style="font-size:3rem;">📭</span>
            <p style="font-size:1.1rem; margin-top:12px;">No operations recorded yet.</p>
            <p style="font-size:0.85rem;">Head over to <strong>Encrypt / Decrypt</strong> to get started!</p>
        </div>
        """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Learn Cryptography
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📖  Learn Cryptography":
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">📖</span>
        <h2>Learn Cryptography</h2>
    </div>
    """, unsafe_allow_html=True)

    # ── Fundamental Concepts ───────────────────────────────────
    with st.expander("🔑 What is Encryption?", expanded=True):
        st.markdown("""
        **Encryption** is the process of converting readable information
        (*plaintext*) into an unreadable form (*ciphertext*) using a specific
        algorithm and a **key**.

        The goal is to ensure that only authorized parties who possess the
        correct key can read the original information.

        ```
        Plaintext  +  Key  →  [ Encryption Algorithm ]  →  Ciphertext
        "HELLO"    +  3    →  [ Caesar Cipher ]         →  "KHOOR"
        ```
        """)

    with st.expander("🔓 What is Decryption?"):
        st.markdown("""
        **Decryption** is the reverse process — converting ciphertext back into
        its original plaintext form using the correct key and the reverse of the
        encryption algorithm.

        ```
        Ciphertext  +  Key  →  [ Decryption Algorithm ]  →  Plaintext
        "KHOOR"     +  3    →  [ Caesar Decrypt ]         →  "HELLO"
        ```

        Without the correct key, the ciphertext should remain unreadable
        (though with classical ciphers, this protection is easily broken).
        """)

    with st.expander("📄 Plaintext vs. Ciphertext"):
        st.markdown("""
        | Term | Meaning | Example |
        |------|---------|---------|
        | **Plaintext** | The original, readable message | `HELLO WORLD` |
        | **Ciphertext** | The encrypted, unreadable output | `KHOOR ZRUOG` |

        In modern cryptography, plaintext can be any data — text, images,
        files — not just human-readable text.
        """)

    st.markdown('<div class="cv-divider"></div>', unsafe_allow_html=True)

    # ── Caesar Cipher ──────────────────────────────────────────
    with st.expander("🏛️ How Does the Caesar Cipher Work?"):
        st.markdown("""
        The **Caesar cipher** is one of the simplest encryption techniques. It
        works by **shifting** each letter in the alphabet by a fixed number of
        positions.

        **Example with Shift = 3:**
        ```
        Plain:    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
        Cipher:   D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
        ```

        **Encrypting "HELLO" with Shift 3:**
        - H → K  (H + 3)
        - E → H  (E + 3)
        - L → O  (L + 3)
        - L → O  (L + 3)
        - O → R  (O + 3)
        - Result: **KHOOR**

        **Strengths:** Simple to understand and implement.

        **Weaknesses:**
        - Only 25 possible keys (shifts 1–25)
        - Trivially cracked via brute force
        - Vulnerable to frequency analysis
        - Provides no real security
        """)

    with st.expander("📜 How Does the Vigenère Cipher Work?"):
        st.markdown("""
        The **Vigenère cipher** extends the Caesar cipher by using a
        **keyword** instead of a single shift value. Each letter of the keyword
        determines the shift for the corresponding letter of the plaintext.

        **Example with Keyword = "KEY":**
        ```
        Plaintext:  H  E  L  L  O
        Keyword:    K  E  Y  K  E
        Shifts:    10  4 24 10  4
        Ciphertext: R  I  J  V  S
        ```

        The keyword repeats as needed to cover the entire plaintext.

        **Strengths:**
        - Harder to crack than Caesar (polyalphabetic)
        - Resistant to simple frequency analysis
        - More keys = larger key space

        **Weaknesses:**
        - Can be broken with the Kasiski method or index of coincidence
        - Short keywords are especially vulnerable
        - Still insecure by modern standards
        """)

    st.markdown('<div class="cv-divider"></div>', unsafe_allow_html=True)

    with st.expander("🔑 Why Do Encryption Keys Matter?"):
        st.markdown("""
        The **key** is what makes encryption secure (or insecure).

        - **Caesar cipher** has only 25 possible keys → trivially breakable
        - **Vigenère cipher** has more keys (depending on keyword length) but
          is still limited
        - **Modern algorithms** (AES-256) have 2²⁵⁶ possible keys — more than
          the atoms in the observable universe

        **Key principles:**
        1. A larger key space makes brute-force attacks impractical
        2. The key must be kept secret — the algorithm can be public
        3. Key management is often the hardest part of real cryptography
        """)

    with st.expander("⚠️ Why Classical Ciphers Are NOT Secure"):
        st.markdown("""
        Classical ciphers like Caesar and Vigenère are **not suitable for
        modern security** because:

        1. **Tiny key space**: Can be brute-forced in microseconds
        2. **Pattern preservation**: Letter frequencies leak information
        3. **No diffusion**: Changing one plaintext letter changes only one
           ciphertext letter
        4. **Known attacks**: Frequency analysis, Kasiski examination, and
           other techniques break them easily

        **Modern encryption** (AES, RSA, ChaCha20) addresses all of these
        weaknesses through:
        - Massive key spaces
        - Complex mathematical operations
        - Avalanche effect (small input changes → large output changes)
        - Resistance to all known cryptanalytic attacks

        > *CipherVault uses classical ciphers purely as educational tools to
        > teach the fundamental concepts that underpin modern cryptography.*
        """)

    # ── Interactive mini-demo ──────────────────────────────────
    st.markdown('<div class="cv-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cv-section-header">
        <span class="icon">🧪</span>
        <h2>Interactive Mini-Demo</h2>
    </div>
    """, unsafe_allow_html=True)

    demo_text = st.text_input("Try it — enter a word:", value="CRYPTOGRAPHY", key="demo_input")
    demo_shift = st.slider("Caesar shift:", 0, 25, 3, key="demo_shift")

    if demo_text:
        encrypted = caesar_encrypt(demo_text, demo_shift)
        decrypted = caesar_decrypt(encrypted, demo_shift)

        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown(f"""
            <div class="cv-metric">
                <div class="value" style="font-size:1.2rem; word-break:break-all;">{demo_text}</div>
                <div class="label">Plaintext</div>
            </div>""", unsafe_allow_html=True)
        with d2:
            st.markdown(f"""
            <div class="cv-metric">
                <div class="value" style="font-size:1.2rem; word-break:break-all;">{encrypted}</div>
                <div class="label">Ciphertext (shift {demo_shift})</div>
            </div>""", unsafe_allow_html=True)
        with d3:
            st.markdown(f"""
            <div class="cv-metric">
                <div class="value" style="font-size:1.2rem; word-break:break-all;">{decrypted}</div>
                <div class="label">Decrypted ✅</div>
            </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Footer
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="cv-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:16px 0 30px; color:#475569; font-size:0.78rem;">
    <strong>CipherVault</strong> · DecodeLabs Cybersecurity Internship · Project 2<br>
    Built for educational purposes only · Classical ciphers provide no real-world security
</div>
""", unsafe_allow_html=True)
