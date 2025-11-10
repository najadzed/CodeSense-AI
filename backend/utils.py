import os
from langchain_core.documents import Document

SUPPORTED_EXTENSIONS = [
    ".py", ".js", ".ts", ".go", ".java", ".html", ".htm",
    ".css", ".json", ".md", ".txt", ".jsx", ".tsx", ".rb", ".php"
]

def load_code_files(folder_path):
    """
    Recursively load supported files from a folder, return list of Document objects
    with line-numbered content and metadata.source = relative path.
    """
    docs = []
    root_abs = os.path.abspath(folder_path)
    for root, _, files in os.walk(root_abs):
        for file in sorted(files):
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        # add line numbers (4 digits)
                        numbered = "".join([f"{i+1:04d}: {line}" for i, line in enumerate(lines)])
                        # store relative path as source
                        rel = os.path.relpath(full_path, root_abs)
                        docs.append(Document(page_content=numbered, metadata={"source": rel, "path": full_path}))
                except Exception as e:
                    print(f"⚠️ Could not read {full_path}: {e}")
    return docs
