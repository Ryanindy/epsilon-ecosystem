import os
import chromadb
from chromadb.utils import embedding_functions
import json

# Configuration
CHROMA_PATH = "rag/.chromadb"
METADATA_PATH = "rag/RAG_METADATA.json"

def sync_vectors():
    print("[*] Initializing Vector Sync (God Mode)...")
    
    if not os.path.exists(METADATA_PATH):
        print("[!] Error: Metadata index not found.")
        return

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = embedding_functions.DefaultEmbeddingFunction()

    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        files = json.load(f)

    print(f"[*] Processing {len(files)} files...")

    for file_info in files:
        coll_name = f"{file_info['collection']}_collection"
        file_path = file_info['path']
        
        if not os.path.exists(file_path):
            print(f"[!] Warning: File not found {file_path}")
            continue

        print(f"[*] Indexing: {file_info['name']} -> {coll_name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            collection = client.get_or_create_collection(name=coll_name, embedding_function=ef)
            
            # Simple chunking for now (by paragraph or fixed length)
            # Jack Protocol: Keep it fast.
            collection.upsert(
                ids=[file_info['id']],
                documents=[content],
                metadatas=[{
                    "source": file_info['name'],
                    "path": file_path,
                    "collection": file_info['collection']
                }]
            )
        except Exception as e:
            print(f"[!] Error indexing {file_info['name']}: {e}")

    print("[+] Vector Sync Complete. RAG is now Intelligent.")

if __name__ == "__main__":
    sync_vectors()
