import google.generativeai as genai
genai.configure(api_key="AIzaSyCNv8tIxzylhGincFxKbxHexsAtDwdWUgc")
for m in genai.list_models():
    print(m.name, " | supports generate_content:", "generateContent" in m.supported_generation_methods)
