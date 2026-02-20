import os
import sys
import chromadb
from chromadb.utils import embedding_functions

# Get Project Root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_PATH = os.path.join(PROJECT_ROOT, "rag", ".chromadb")

def warmup():
    print("[RAG] Warming up Vector Engine...")
    if not os.path.exists(CHROMA_PATH):
        print("[RAG] Error: ChromaDB path not found. Skipping warmup.")
        return

    try:
        # Initialize Client
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Get all collections
        collections = client.list_collections()
        print(f"[RAG] Found {len(collections)} collections to warm up.")
        
        for coll_meta in collections:
            coll_name = coll_meta.name
            print(f"  -> Paging: {coll_name}")
            collection = client.get_collection(name=coll_name, embedding_function=ef)
            # Dummy query to force disk-to-memory paging
            collection.query(query_texts=["warmup"], n_results=1)
            
        print("[RAG] Warmup complete. Indices are now in OS cache.")
    except Exception as e:
        print(f"[RAG] Warmup failed: {e}")

if __name__ == "__main__":
    warmup()
