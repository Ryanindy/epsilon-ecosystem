import os
import shutil
import hashlib

def get_file_hash(path):
    """Simple hash for deduplication."""
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        # Just hash the first 1MB for speed
        buf = f.read(1024 * 1024)
        hasher.update(buf)
    return hasher.hexdigest()

source_dir = "I:\\"
dest_base = r"I:"

# Folders to IGNORE (The new structure + System)
ignore_dirs = {
    'LIBRARY', 'ARSENAL', 'GALLERY', 'GRAVEYARD', '_SOURCE_', 
    '$RECYCLE.BIN', 'System Volume Information', '.chromadb'
}

# Map extensions to destinations
ext_map = {
    # LIBRARY
    '.pdf': r'LIBRARY\Manuals',
    '.epub': r'LIBRARY\Philosophy',
    '.md': r'LIBRARY\Manuals',
    '.txt': r'LIBRARY\Manuals',
    # ARSENAL
    '.json': r'ARSENAL\Webhooks',
    '.py': r'ARSENAL\Coding',
    '.go': r'ARSENAL\Coding',
    '.js': r'ARSENAL\Coding',
    '.exe': r'ARSENAL\Windows_Tools',
    '.msi': r'ARSENAL\Windows_Tools',
    # GALLERY
    '.jpg': r'GALLERY\Images',
    '.jpeg': r'GALLERY\Images',
    '.png': r'GALLERY\Images',
    '.gif': r'GALLERY\Images',
    '.mp4': r'GALLERY\Video',
    '.mov': r'GALLERY\Video',
}

# Subfolder keyword map
keyword_map = {
    'legal': r'LIBRARY\Legal',
    'fcra': r'LIBRARY\Legal',
    'rcw': r'LIBRARY\Legal',
    'business': r'LIBRARY\Business',
    'tax': r'LIBRARY\Business',
    'epsilon': r'LIBRARY\Philosophy',
    'n8n': r'ARSENAL\Webhooks',
}

processed_hashes = set()

print(f"[*] Starting Reorg from {source_dir}...")

for root, dirs, files in os.walk(source_dir):
    # Modify dirs in-place to skip ignored folders
    dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
    
    for file in files:
        file_path = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        
        # Determine Target
        target_sub = None
        
        # Check keywords in path first (higher priority)
        path_lower = file_path.lower()
        for kw, folder in keyword_map.items():
            if kw in path_lower:
                target_sub = folder
                break
        
        # Fallback to extension map
        if not target_sub:
            target_sub = ext_map.get(ext)
            
        if target_sub:
            dest_dir = os.path.join(dest_base, target_sub)
            dest_path = os.path.join(dest_dir, file)
            
            # Simple Deduplication
            try:
                # If file is big, hash it
                if os.path.getsize(file_path) > 1024:
                    f_hash = f"{file}_{os.path.getsize(file_path)}" # Simple hash for speed
                    if f_hash in processed_hashes:
                        continue
                    processed_hashes.add(f_hash)
                
                # Copy if not exists
                if not os.path.exists(dest_path):
                    shutil.copy2(file_path, dest_path)
                    # print(f"[+] Copied: {file} -> {target_sub}")
            except Exception as e:
                print(f"[!] Error copying {file}: {e}")

print("[*] Reorg Complete. Everything is in its right place.")