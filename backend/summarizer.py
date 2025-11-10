import google.generativeai as genai
from backend.config import GEMINI_MODEL

def summarize_code(content, filename="codebase"):
    """
    Summarize a snippet of the codebase (content). Keep under model context limits.
    """
    prompt = f"""
You are a senior software architect. Summarize the following codebase snippet in 3 concise bullet points:
- Describe the main purpose of the codebase
- Mention primary languages/frameworks used
- Note any key files, endpoints, or noteworthy architecture patterns

Codebase snippet ({filename}):
{content}
"""
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    if hasattr(response, "content"):
        try:
            return response.content[0].text.strip()
        except Exception:
            return str(response)
    return getattr(response, "text", str(response))
