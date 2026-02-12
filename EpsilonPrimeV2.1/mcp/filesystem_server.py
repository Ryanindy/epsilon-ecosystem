import os
import shutil
import asyncio
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("epsilon-filesystem")

# Allowed root - default to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@mcp.tool()
def list_directory(path: str = ".") -> str:
    """
    Lists the contents of a directory.
    """
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    try:
        items = os.listdir(full_path)
        return "
".join(items)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def read_file(path: str) -> str:
    """
    Reads the content of a file.
    """
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file.
    """
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Written to {path}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def move_file(source: str, destination: str) -> str:
    """
    Moves or renames a file or directory.
    """
    src_path = os.path.abspath(os.path.join(BASE_DIR, source))
    dest_path = os.path.abspath(os.path.join(BASE_DIR, destination))
    try:
        shutil.move(src_path, dest_path)
        return f"Success: Moved {source} to {destination}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def get_file_info(path: str) -> str:
    """
    Gets metadata for a file or directory.
    """
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    try:
        stat = os.stat(full_path)
        return f"Size: {stat.st_size} bytes, Created: {stat.st_ctime}, Modified: {stat.st_mtime}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
