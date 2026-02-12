import os
import platform
import subprocess
import shutil

def get_drives():
    """
    Returns a list of available drives/mount points on the host system.
    Supports Windows and Linux.
    """
    drives = []
    system = platform.system()

    if system == "Windows":
        try:
            # Use wmic to get logical disks
            output = subprocess.check_output(['wmic', 'logicaldisk', 'get', 'name'], encoding='utf-8')
            drives = [line.strip() for line in output.split('
') if line.strip() and "Name" not in line]
        except Exception as e:
            # Fallback for Windows if wmic fails
            import string
            available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
            drives = available_drives

    elif system == "Linux":
        try:
            # Use df -h to get mount points
            output = subprocess.check_output(['df', '-h'], encoding='utf-8')
            lines = output.split('
')[1:] # Skip header
            for line in lines:
                parts = line.split()
                if parts:
                    mount_point = parts[-1]
                    drives.append(mount_point)
        except Exception:
            pass
    
    return drives

def scan_path(path):
    """
    Returns a list of files and folders in the specified path.
    """
    results = []
    try:
        if not os.path.exists(path):
            return f"Error: Path {path} does not exist."
        
        with os.scandir(path) as entries:
            for entry in entries:
                info = {
                    "name": entry.name,
                    "is_dir": entry.is_dir(),
                    "path": entry.path,
                    "size": entry.stat().st_size if not entry.is_dir() else 0
                }
                results.append(info)
    except Exception as e:
        return f"Error scanning path: {e}"
    
    return results

def read_host_file(path):
    """
    Reads the content of a file on the host.
    """
    try:
        if not os.path.exists(path):
            return f"Error: File {path} not found."
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_host_file(path, content):
    """
    Writes content to a file on the host.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Written to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def copy_to_host(source, destination):
    """
    Copies a file from the portable environment to the host.
    """
    try:
        shutil.copy2(source, destination)
        return f"Success: Copied {source} to {destination}"
    except Exception as e:
        return f"Error copying file: {e}"

if __name__ == "__main__":
    # Test execution
    print(f"Host System: {platform.system()}")
    print(f"Drives: {get_drives()}")
