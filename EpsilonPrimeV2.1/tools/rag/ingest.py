import os
import argparse
import json
import time

def generate_index(source_dir, output_file, collection_name, yolo_mode=False):
    print(f"[*] Indexing {source_dir} (Collection: {collection_name})...")
    
    files_data = []
    
    if not os.path.exists(source_dir):
        print(f"[!] Error: Source directory {source_dir} not found.")
        return

    count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # In YOLO mode, we ingest almost everything. Otherwise, filter system files.
            if not yolo_mode and (file.startswith('.') or file == "Thumbs.db"):
                continue
                
            file_path = os.path.join(root, file)
            try:
                # Basic metadata extraction
                file_info = {
                    "id": f"{collection_name}_{count}",
                    "name": file,
                    "path": os.path.abspath(file_path),
                    "collection": collection_name,
                    "size": os.path.getsize(file_path),
                    "extension": os.path.splitext(file)[1].lower(),
                    "last_modified": os.path.getmtime(file_path)
                }
                files_data.append(file_info)
                count += 1
            except Exception as e:
                print(f"[!] Error processing {file}: {e}")

    # Load existing if it exists (Append Mode)
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                # Filter out old entries from this collection to avoid duplicates
                existing_data = [x for x in existing_data if x.get('collection') != collection_name]
                files_data.extend(existing_data)
        except:
            pass # Start fresh if corrupt

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(files_data, f, indent=2)

    elapsed = time.time() - start_time
    print(f"[+] Index updated at {output_file}. Added {count} files in {elapsed:.2f}s.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest files into RAG Index.")
    parser.add_argument("--source", required=True, help="Directory to ingest")
    parser.add_argument("--collection", default="default", help="Collection name")
    parser.add_argument("--output", default="rag/RAG_METADATA.json", help="Output JSON index")
    parser.add_argument("--yolo", action="store_true", help="Ingest all files without strict filters")
    
    args = parser.parse_args()
    
    generate_index(args.source, args.output, args.collection, args.yolo)