from pathlib import Path

DOCS_PATH = Path("data/django_docs")

def load_documents():
    documents = []

    for file in DOCS_PATH.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "text": text,
            "metadata": {
                "source": file.name
            }
        })

    return documents
