# 💻 CodeSense AI — Powered by Gemini  
### _Understand your codebase instantly • Built for developers, by developers._

![CodeSense AI Preview](./assets/screenshots/dbcc026f-8b3b-4432-a5aa-d77479b38372.png)  
*(Above: CodeSense AI in action — dark mode with Gemini-powered code summarization)*

---

<p align="center">
  <a href="https://streamlit.io" target="_blank"><img src="https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"></a>
  <a href="https://ai.google.dev/gemini-api" target="_blank"><img src="https://img.shields.io/badge/Powered%20by-Gemini-4285F4?logo=google&logoColor=white" alt="Gemini"></a>
  <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/ZedroDev/CodeSense-AI/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/License-MIT-success" alt="MIT License"></a>
</p>

---

## 🚀 Overview
**CodeSense AI** is an intelligent developer assistant that lets you **upload, explore, and query codebases** using natural language.  
Powered by **Google Gemini**, it performs context-aware reasoning — summarizing, locating endpoints, explaining architecture, and answering deep technical questions.

It’s your personal **AI code analyst**, designed for speed, clarity, and developer insight.

---

## ✨ Key Features — Already Implemented

```diff
+ 🧠 RAG-Powered Q&A — Retrieves exact code context and line references  
+ 💬 Gemini Summarizer — Generates detailed project-level summaries  
+ 🎨 Dark / Light Theme Toggle — Smooth transitions with custom CSS  
+ ⚙️ Demo Mode — Instantly load sample projects for testing  
+ 📂 Multi-file Upload — Supports ZIPs or individual code files  
+ 🧭 Recent Questions History — Sidebar recall with clear option  
+ 💡 Smart Header + Logo — Animated gradient and brand identity  
+ ⚡ Glowing Footer — Signature with social icons and gradient animation  

🧠 Example Insights

Query: “Where is the API authentication handled?”

Gemini’s Developer Insight
Found in auth/routes.py, lines 22–58 — defines the verify_user_token() function that validates JWTs before accessing protected endpoints.

Query: “Summarize this frontend structure.”

Gemini Summary
React-based dashboard app using modular context providers, dynamic routing, and API abstraction hooks for clean scalability.

🖼️ Interface Showcase
Mode	Preview
🏠 Main Dashboard	

🧠 Code Summarization	

💬 Developer Insights	

⚙️ Sidebar Controls	
🧩 Tech Stack
Layer	Technology
Frontend	Streamlit (custom CSS, components, theme toggle)
AI Model	Gemini 2.5 Pro via Google Generative AI SDK
RAG / Embeddings	LangChain + HuggingFace + FAISS
Backend Logic	Python (LangChain RAG pipeline, summarization, retriever)
File Parsing	Recursive directory + TextSplitter for all major languages
⚙️ Setup Instructions
1️⃣ Clone Repo
git clone https://github.com/ZedroDev/CodeSense-AI.git
cd CodeSense-AI

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Create .env File
GEMINI_API_KEY=your_gemini_api_key_here

4️⃣ Run the App
streamlit run app.py

🔮 Future Enhancements (v2.0)
+ 🎥 Interactive Demo Mode with curated sample projects  
+ 🧠 Full Repo Summarization with progress visualization  
+ 📄 Export to PDF (AI-generated summary reports)  
+ 🧩 Syntax-highlighted inline code viewer  
+ 🧭 Persistent Memory (SQLite) for question history  

🧾 Repository Info

Repository: CodeSense-AI

Description:
💻 AI-powered tool to analyze, summarize, and query entire codebases using Gemini and LangChain — with a modern Streamlit interface, dark mode, and RAG reasoning.

Topics:
ai • gemini • streamlit • langchain • rag • code-analyzer • python • developer-tools • codebase-search

🖋️ Credits & Footer

💻 Crafted with precision by Najad

Powered by CodeSense AI × Gemini
 ⚡
```