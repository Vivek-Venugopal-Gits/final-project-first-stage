import chromadb
from rag.embeddings import embed_texts
from pathlib import Path

# Use relative path from the rag module
CHROMA_PATH = Path(__file__).parent.parent / "data" / "vector_db"


def retrieve_context(query, k=4):
    """
    Retrieve relevant context from the vector database.
    
    Args:
        query: User's query string
        k: Number of results to retrieve
    
    Returns:
        tuple: (combined_context_string, list_of_sources)
    """
    # Create persistent client
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    try:
        collection = client.get_collection("django_docs")
    except Exception as e:
        print(f"⚠️  Warning: Vector database not found. Run RAG setup first.")
        print(f"   Error: {e}")
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