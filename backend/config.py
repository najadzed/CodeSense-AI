import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# --- Load key ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY missing in .env")

genai.configure(api_key=GEMINI_API_KEY)

# --- Priority list ---
# put flash first since pro often has zero free quota
MODEL_PRIORITY = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.5-pro",
    "gemini-pro-latest"
]

def choose_model():
    """
    Pick the best available model that supports generate_content and still fits free-tier quota.
    """
    try:
        models = list(genai.list_models())
        supported = []
        for m in models:
            name = m.name
            methods = getattr(m, "supported_generation_methods", [])
            if "generateContent" in methods or "generate_content" in methods:
                supported.append(name)

        # check priority order
        for pref in MODEL_PRIORITY:
            for m in supported:
                if pref in m:
                    print(f"✅ Using Gemini model: {m}")
                    return m

        if supported:
            print(f"⚠️ Using fallback model: {supported[0]}")
            return supported[0]

    except Exception as e:
        print(f"⚠️ Model discovery failed, using default flash: {e}")

    # last resort
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

GEMINI_MODEL = choose_model()
