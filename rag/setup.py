from rag.loader import load_documents
from rag.splitter import split_documents
from rag.vector_store import build_vector_store


def setup_rag():
    print("Loading documents...")
    documents = load_documents()

    print("Splitting documents...")
    chunks = split_documents(documents)

    print("Building vector store...")
    build_vector_store(chunks)

    print("RAG setup complete.")

#Command
#python -c "from rag.setup import setup_rag; setup_rag()"
