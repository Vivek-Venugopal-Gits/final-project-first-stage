import chromadb
from chromadb.config import Settings
from rag.embeddings import embed_texts

CHROMA_PATH = "data/vector_db"


def retrieve_context(query, k=4):
    client = chromadb.Client(
        Settings(persist_directory=CHROMA_PATH)
    )

    try:
        collection = client.get_collection("django_docs")
    except Exception:
        return "", []

    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    contexts = []
    sources = set()

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        contexts.append(doc)
        sources.add(meta["source"])

    return "\n\n".join(contexts), list(sources)
