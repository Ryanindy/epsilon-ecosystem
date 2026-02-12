import os
import argparse
import chromadb
from chromadb.utils import embedding_functions

# Configuration
CHROMA_PATH = "rag/.chromadb"
DEFAULT_DIR = "skills"

def surgical_sync(target_dir):
    print(f"[*] Initializing Surgical Sync (God Mode) on {target_dir}...")
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(name="epsilon_collection", embedding_function=ef)

    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"[*] Embedding: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Use path as ID to ensure uniqueness and prevent overwrites
                    collection.upsert(
                        ids=[file_path],
                        documents=[content],
                        metadatas=[{
                            "source": file,
                            "path": file_path,
                            "type": "external_knowledge"
                        }]
                    )
                    count += 1
                except Exception as e:
                    print(f"[!] Error: {e}")

    print(f"[+] Surgical Sync Complete. {count} documents are now searchable.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=DEFAULT_DIR, help="Directory to sync")
    args = parser.parse_args()
    surgical_sync(args.dir)
