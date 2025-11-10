import google.generativeai as genai
from backend.config import GEMINI_MODEL

def build_context_text(context_docs, max_chars_per_doc=1500):
    """
    Build a single string context from retrieved docs, including file header.
    """
    context_text = ""
    for d in context_docs:
        source = d.metadata.get("source", d.metadata.get("path", "unknown"))
        snippet = d.page_content[:max_chars_per_doc]
        context_text += f"\n\n=== File: {source} ===\n{snippet}\n"
    return context_text

def query_gemini(context_docs, question):
    """
    Send context + question to Gemini and return (answer, context_docs).
    """
    context_text = build_context_text(context_docs, max_chars_per_doc=1500)
    prompt = f"""
You are CodeSense AI — a senior software engineer assistant.

Use the code context below to answer precisely.
If the question asks about endpoints, routes, auth, logging, etc.:
 - Mention which file it’s in (relative path)
 - Approximate line number (if visible)
 - The function/class name (if visible)
 - A short explanation of what the code does and where to look

Context:
{context_text}

Question:
{question}

Answer concisely as a developer. Reference files and line numbers where possible.
"""
    model = genai.GenerativeModel(GEMINI_MODEL)
    # use generate_content; handle API changes safely
    response = model.generate_content(prompt)
    # response may be a complex object; grab text
    text = ""
    if hasattr(response, "content"):
        # older/newer SDKs may differ
        try:
            text = response.content[0].text
        except Exception:
            text = str(response)
    else:
        text = getattr(response, "text", str(response))
    return text.strip(), context_docs
