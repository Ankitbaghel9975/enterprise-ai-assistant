
import chromadb
from chromadb.utils import embedding_functions

# Create persistent vector database
client = chromadb.PersistentClient(
    path="./data/chroma_db"
)

# Use ChromaDB's default embedding model
embedding_function = (
    embedding_functions.DefaultEmbeddingFunction()
)

# Create or access document collection
collection = client.get_or_create_collection(
    name="company_documents",
    embedding_function=embedding_function
)


def store_documents(chunks, document_name):

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(f"{document_name}_{index}")

        documents.append(chunk["text"])

        metadatas.append({
            "filename": document_name,
            "page": chunk["page"]
        })

    if documents:
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    return len(documents)

def search_documents(question, top_k=3):

    # Check whether any documents have been uploaded
    total_documents = collection.count()

    if total_documents == 0:
        return []

    # Search for the most relevant document chunks
    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, total_documents)
    )

    retrieved_chunks = []

    if results["documents"]:
        for text, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved_chunks.append({
                "text": text,
                "filename": metadata["filename"],
                "page": metadata["page"],
                "distance": distance
            })

    return retrieved_chunks


