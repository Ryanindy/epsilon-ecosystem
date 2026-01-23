import os
import chromadb
from chromadb.utils import embedding_functions
import uuid
from pypdf import PdfReader

# Configuration
CHROMA_PATH = "H:/.chromadb"
RAG_ROOT = "H:/"

# Primary Domains (High Confidence)
DOMAIN_MAP = {
    "epsilon": "epsilon_collection",
    "legal": "legal_collection",
    "business": "business_collection",
    "decisions": "decisions_collection"
}

# External Sources (Library / Archive)
# We will scan these recursively
LIBRARY_ROOTS = [
    "H:/EricAI_RAG",
    "H:/Legal Legal"
]

def safe_read_text(file_path):
    for encoding in ['utf-8', 'cp1252', 'latin-1']:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, PermissionError):
            continue
    return None

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return None

def build_index():
    print(f"Connecting to ChromaDB at {CHROMA_PATH}...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = embedding_functions.DefaultEmbeddingFunction()
    total_docs = 0

    # 1. Process Core Domains
    for domain, collection_name in DOMAIN_MAP.items():
        dir_path = os.path.join(RAG_ROOT, domain)
        if not os.path.exists(dir_path):
            continue

        print(f"Processing domain: {domain} -> {collection_name}")
        try:
            collection = client.get_or_create_collection(name=collection_name, embedding_function=ef)
        except Exception as e:
            print(f"Error creating collection {collection_name}: {e}")
            continue

        files = [f for f in os.listdir(dir_path) if f.endswith(".md") and f != "README.md"]
        
        ids, documents, metadatas = [], [], []

        for filename in files:
            content = safe_read_text(os.path.join(dir_path, filename))
            if not content: continue
            
            ids.append(filename.replace(".md", ""))
            documents.append(content)
            metadatas.append({"source": filename, "domain": domain})

        if ids:
            collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            count = collection.count()
            print(f"  -> Collection count: {count}")
            total_docs += count

    # 2. Process Library (Bulk Ingest)
    print("Processing Library (Bulk Ingest)...")
    try:
        library_col = client.get_or_create_collection(name="library_collection", embedding_function=ef)
    except Exception as e:
        print(f"Error creating library_collection: {e}")
        return

    library_ids, library_docs, library_metadatas = [], [], []
    
    for root_dir in LIBRARY_ROOTS:
        if not os.path.exists(root_dir):
            print(f"Skipping {root_dir} (not found)")
            continue
            
        print(f"Scanning: {root_dir}")
        for root, _, files in os.walk(root_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                content = None
                
                # Check extension
                if filename.lower().endswith((".md", ".txt")):
                    content = safe_read_text(file_path)
                elif filename.lower().endswith(".pdf"):
                    content = read_pdf(file_path)
                
                if not content or len(content) < 100: continue # Skip empty/short files

                # Create unique ID
                doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, file_path))
                
                library_ids.append(doc_id)
                library_docs.append(content)
                library_metadatas.append({
                    "source": filename,
                    "path": file_path,
                    "domain": "library"
                })
                
                # Batch upsert (50 at a time to be safe with memory)
                if len(library_ids) >= 50:
                    try:
                        library_col.upsert(ids=library_ids, documents=library_docs, metadatas=library_metadatas)
                        total_docs += len(library_ids)
                        print(f"  -> Indexed {len(library_ids)} documents from {root}...")
                    except Exception as e:
                        print(f"Error upserting batch: {e}")
                    library_ids, library_docs, library_metadatas = [], [], []

    # Final batch
    if library_ids:
        library_col.upsert(ids=library_ids, documents=library_docs, metadatas=library_metadatas)
        total_docs += len(library_ids)

    print("\n==========================================")
    print(f"INDEXING COMPLETE. Total Documents: {total_docs}")
    print("==========================================")

if __name__ == "__main__":
    build_index()
