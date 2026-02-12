import os
import chromadb
from chromadb.utils import embedding_functions
import argparse

# Configuration
CHROMA_PATH = "rag/.chromadb"

def query_rag(query_text, collection_filter=None, threshold=0.05, top_k=5):
    """
    Sovereign RAG Query Tool (Pickle Spec).
    """
    if not os.path.exists(CHROMA_PATH):
        return "ERROR: RAG Index not found."

    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        ef = embedding_functions.DefaultEmbeddingFunction()
    except Exception as e:
        return f"ERROR: Connection failure: {e}"

    # Determine which collections to scan
    if collection_filter:
        collections = [f"{collection_filter}_collection" if "_collection" not in collection_filter else collection_filter]
    else:
        collections = [c.name for c in client.list_collections()]

    all_results = []

    for coll_name in collections:
        try:
            collection = client.get_collection(name=coll_name, embedding_function=ef)
            results = collection.query(
                query_texts=[query_text],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            if not results['ids'] or not results['ids'][0]:
                continue

            for i in range(len(results['ids'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                dist = results['distances'][0][i]
                similarity = 1.0 / (1.0 + dist)

                if similarity >= threshold:
                    all_results.append({
                        "content": doc,
                        "metadata": meta,
                        "similarity": similarity,
                        "collection": coll_name
                    })
        except Exception:
            continue

    all_results.sort(key=lambda x: x['similarity'], reverse=True)
    final_results = all_results[:top_k]

    if not final_results:
        return f"ZERO_MATCHES: No matches above threshold {threshold} in {collections}."

    output = [f"## RAG RETRIEVAL: '{query_text}'\n"]
    for res in final_results:
        output.append(f"### Collection: {res['collection']} (Sim: {res['similarity']:.4f})")
        output.append(f"**Source**: {res['metadata'].get('source', 'Unknown')}")
        output.append(f"**Path**: {res['metadata'].get('path', 'Unknown')}")
        output.append(f"\n{res['content']}\n")
        output.append("---")

    return "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pickle Rick's Sovereign RAG Query")
    parser.add_argument("--query", required=True)
    parser.add_argument("--collection", help="Optional collection name")
    parser.add_argument("--threshold", type=float, default=0.05)
    
    args = parser.parse_args()
    print(query_rag(args.query, args.collection, args.threshold))