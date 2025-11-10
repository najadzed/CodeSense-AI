import streamlit as st
import os, zipfile, tempfile, base64
import streamlit.components.v1 as components
from backend.utils import load_code_files
from backend.embeddings import build_vector_db
from backend.rag_pipeline import query_gemini
from backend.summarizer import summarize_code

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(page_title="CodeSense AI", page_icon="💻", layout="wide")

# ============================
# THEME TOGGLE (dark / light)
# ============================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

toggle_label = "🌙 Dark Mode" if st.session_state.theme == "dark" else "☀️ Light Mode"
if st.sidebar.button(toggle_label, key="toggle_theme"):
    toggle_theme()

# ============================
# SESSION VARIABLES
# ============================
if "history" not in st.session_state:
    st.session_state.history = []
if "db" not in st.session_state:
    st.session_state.db = None
if "docs" not in st.session_state:
    st.session_state.docs = None
if "summary" not in st.session_state:
    st.session_state.summary = None

# ============================
# THEME STYLES
# ============================
theme_color = "#0E1117" if st.session_state.theme == "dark" else "#FFFFFF"
text_color = "#FFFFFF" if st.session_state.theme == "dark" else "#000000"
sidebar_bg = "#1E1E1E" if st.session_state.theme == "dark" else "#F5F5F5"

st.markdown(f"""
<style>
body {{ background-color: {theme_color}; color: {text_color}; }}
div[data-testid="stSidebar"]{{ background-color:{sidebar_bg}; }}
.stButton > button {{ border-radius:10px; }}
.stFileUploader, .stTextInput > div > div > input {{ border-radius: 8px; }}
hr{{ border-top:1px solid {'#303030' if st.session_state.theme=='dark' else '#DDD'}; }}
</style>
""", unsafe_allow_html=True)

# ============================
# HEADER (Perfectly Centered)
# ============================
logo_path = "assets/codesense_logo.png"
logo_base64 = ""
if os.path.exists(logo_path):
    logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()

header_html = f"""
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 14px;
    margin-top: 0px;
    margin-bottom: 6px;
    line-height: 1.2;
">
    <img src="data:image/png;base64,{logo_base64}"
         style="
            width: 58px;
            height: 58px;
            border-radius: 14px;
            box-shadow: 0 0 12px rgba(0,0,0,0.25);
            object-fit: contain;
            vertical-align: middle;
            margin-top: -3px;
            transition: all 0.3s ease;
         "
         onmouseover="this.style.transform='scale(1.08)'; this.style.boxShadow='0 0 18px rgba(79,70,229,0.45)';"
         onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 0 12px rgba(0,0,0,0.25)';"
    >
    <h1 style="
        font-size: 2.7rem;
        font-weight: 700;
        letter-spacing: -0.6px;
        margin: 0;
        padding: 0;
        display: flex;
        align-items: center;
        background: linear-gradient(90deg, #7dd3fc, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">
        CodeSense&nbsp;AI
    </h1>
</div>
<p style="text-align:center; color:gray; font-size:1.05rem; margin-top:2px;">
    Understand your codebase instantly — powered by <b>Gemini</b>
</p>
<hr style="opacity:0.4; margin-top:10px; margin-bottom:25px;">
"""

components.html(header_html, height=160)

# ============================
# SIDEBAR SECTION
# ============================
with st.sidebar:
    st.image("assets/codesense_logo.png", width=100)
    st.header("⚙️ Settings")

    folder_path = st.text_input("📁 Local folder path (optional):", placeholder="C:/Users/ASUS/Desktop/project")
    st.caption("Upload ZIPs or single code files or use Demo Mode.")

    if st.button("🚀 Run Demo Mode", key="demo_mode"):
        demo_path = os.path.join("data", "sample_code")
        if os.path.exists(demo_path):
            with st.spinner("Loading demo project..."):
                docs = load_code_files(demo_path)
                st.session_state.db = build_vector_db(docs)
                st.session_state.docs = docs
                st.success("✅ Demo project loaded successfully!")
        else:
            st.error("Demo sample_code not found.")

    st.divider()
    st.subheader("🧭 Recent Questions")

    # Clear History Button
    if st.button("🗑️ Clear History", key="clear_history"):
        st.session_state.history.clear()
        st.success("History cleared.")

    # Recent question buttons
    if st.session_state.history:
        for idx, q in enumerate(reversed(st.session_state.history[-8:])):
            short_label = q[:40] + ("..." if len(q) > 40 else "")
            if st.button(short_label, key=f"history_{idx}", help=q):
                st.session_state.last_question = q
    else:
        st.caption("No recent questions yet.")

# ============================
# FILE UPLOAD + PROCESSING
# ============================
uploaded_files = st.file_uploader(
    "Upload your codebase or files",
    type=["zip", "py", "js", "ts", "java", "go", "html", "css", "json", "md", "txt", "jsx", "tsx", "rb", "php", "htm"],
    accept_multiple_files=True
)

question = st.text_input("💬 Ask about your codebase:", placeholder="e.g. Where are API endpoints defined?")

if uploaded_files or (folder_path and os.path.isdir(folder_path)):
    temp_dir = tempfile.mkdtemp()

    # Extract files
    for file in uploaded_files:
        if file.name.endswith(".zip"):
            with zipfile.ZipFile(file, "r") as z:
                z.extractall(temp_dir)
        else:
            path = os.path.join(temp_dir, file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())

    if folder_path and os.path.isdir(folder_path):
        temp_dir = folder_path

    with st.spinner("🔍 Indexing your codebase..."):
        docs = load_code_files(temp_dir)
        if not docs:
            st.warning("⚠️ No supported code files found.")
        else:
            st.session_state.db = build_vector_db(docs)
            st.session_state.docs = docs
            st.success(f"📚 Indexed {len(docs)} files successfully!")

# ============================
# SUMMARIZE BUTTON
# ============================
if st.session_state.docs:
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🧠 Summarize Codebase", key="summarize"):
            with st.spinner("📝 Summarizing with Gemini..."):
                all_text = "\n\n".join([d.page_content[:2000] for d in st.session_state.docs[:30]])
                st.session_state.summary = summarize_code(all_text, "uploaded codebase")
    with col2:
        if st.session_state.summary:
            with st.expander("📘 Gemini Summary", expanded=True):
                st.markdown(st.session_state.summary)

# ============================
# RAG (QUESTION HANDLER)
# ============================
def run_query_and_display(q):
    retriever = st.session_state.db.as_retriever()
    try:
        retrieved = retriever.get_relevant_documents(q)
    except AttributeError:
        retrieved = retriever.invoke(q)
    if not retrieved:
        st.warning("⚠️ No relevant code found for that question.")
        return

    with st.spinner("🤖 Thinking with Gemini..."):
        answer, docs_used = query_gemini(retrieved[:4], q)

    st.session_state.history.append(q)
    if len(st.session_state.history) > 30:
        st.session_state.history = st.session_state.history[-30:]

    st.markdown("### 💬 Gemini’s Developer Insight")
    st.write(answer)
    st.markdown("### 🔎 Referenced Code Snippets")

    for d in docs_used[:6]:
        source = d.metadata.get("source", d.metadata.get("path", "unknown"))
        ext = os.path.splitext(source)[1].lower().lstrip(".")
        lang_map = {
            "py":"python","js":"javascript","ts":"typescript","go":"go","java":"java",
            "html":"html","css":"css","json":"json","md":"markdown","rb":"ruby","php":"php"
        }
        lang = lang_map.get(ext, "")
        snippet = d.page_content[:1200]
        st.markdown(f"**📄 {source}**")
        st.code(snippet, language=lang)

# Handle clicked history question
if "last_question" in st.session_state and st.session_state.last_question:
    question = st.session_state.last_question
    st.session_state.last_question = None

if question and st.session_state.db:
    run_query_and_display(question)

# ============================
# FOOTER
# ============================
st.markdown("""
<style>
@keyframes glowPulse {
  0% { box-shadow: 0 0 5px #6366f1; opacity: 0.7; }
  50% { box-shadow: 0 0 15px #7c3aed; opacity: 1; }
  100% { box-shadow: 0 0 5px #6366f1; opacity: 0.7; }
}
.footer-glow {
  width: 100%;
  height: 3px;
  margin: 30px 0 18px 0;
  background: linear-gradient(90deg,#6366f1,#7c3aed,#6366f1);
  animation: glowPulse 3s infinite ease-in-out;
  border-radius: 6px;
}
.footer-icons img {
  width: 26px;
  height: 26px;
  margin: 0 6px;
  opacity: 0.8;
  transition: all 0.3s ease-in-out;
}
.footer-icons img:hover {
  opacity: 1;
  transform: scale(1.15);
}
</style>

<div class="footer-glow"></div>

<div style="text-align:center; font-size:1rem; color:#aaa;">
  💻 Built with precision by 
  <a href="https://github.com/najadzed" target="_blank" style="text-decoration:none; color:#7c3aed; font-weight:600;">Najad</a>
  • Powered by <b>CodeSense AI</b> × 
  <span style="color:#a78bfa; font-weight:600;">Gemini</span> ⚡
</div>

<div class="footer-icons" style="text-align:center; margin-top:10px;">
  <a href="https://github.com/najadzed" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/p-najad/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">
  </a>
</div>

<p style="text-align:center; font-size:0.9rem; color:#777; margin-top:6px;">
  © 2025 CodeSense AI. All rights reserved.
</p>
""", unsafe_allow_html=True)
