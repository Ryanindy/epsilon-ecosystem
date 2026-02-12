import shutil
import os
import datetime
import zipfile

# Configuration
SOURCE_DIRS = [
    r"C:\Users\Media Server\skills",
    r"C:\Users\Media Server\flows",
    r"H:\epsilon",
    r"H:\business",
    r"H:\decisions"
]
BACKUP_ROOT = r"C:\Users\Media Server\Desktop\SURVIVAL_VAULT"
TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')

def create_backup():
    if not os.path.exists(BACKUP_ROOT):
        os.makedirs(BACKUP_ROOT)
        
    zip_filename = os.path.join(BACKUP_ROOT, f"Epsilon_Backup_{TIMESTAMP}.zip")
    
    print(f"🔒 Starting Backup to {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in SOURCE_DIRS:
            if os.path.exists(folder):
                print(f"  - Archiving {os.path.basename(folder)}...")
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(folder))
                        try:
                            zipf.write(file_path, arcname)
                        except Exception as e:
                            print(f"    ! Failed to pack {file}: {e}")
            else:
                print(f"  ! Warning: {folder} not found.")
                
    print("✅ Backup Secure.")

if __name__ == "__main__":
    create_backup()
