import chromadb
from chromadb.config import Settings
from rag.embeddings import embed_texts

CHROMA_PATH = "data/vector_db"


def build_vector_store(chunks):
    client = chromadb.Client(
        Settings(persist_directory=CHROMA_PATH)
    )

    collection = client.get_or_create_collection(
        name="django_docs"
    )

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    embeddings = embed_texts(texts)

    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(texts))]
    )

    
