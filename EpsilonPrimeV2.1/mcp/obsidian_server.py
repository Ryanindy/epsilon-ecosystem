import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("epsilon-obsidian")

# Get vault path from env or use default
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", os.path.join(os.getcwd(), "Vault"))

@mcp.tool()
def search_vault(query: str) -> str:
    """
    Searches for notes in the Obsidian vault containing the query string.
    """
    if not os.path.exists(VAULT_PATH):
        return f"Error: Vault path {VAULT_PATH} not found."
    
    matches = []
    for root, dirs, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        if query.lower() in f.read().lower():
                            rel_path = os.path.relpath(full_path, VAULT_PATH)
                            matches.append(rel_path)
                except Exception:
                    continue
    
    return "
".join(matches) if matches else "No matches found."

@mcp.tool()
def read_note(name: str) -> str:
    """
    Reads a note from the vault. Provide the name or relative path (e.g. 'Work/Project.md').
    """
    if not name.endswith(".md"):
        name += ".md"
    
    full_path = os.path.join(VAULT_PATH, name)
    if not os.path.exists(full_path):
        return f"Error: Note {name} not found."
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def create_note(name: str, content: str) -> str:
    """
    Creates a new note in the vault.
    """
    if not name.endswith(".md"):
        name += ".md"
    
    full_path = os.path.join(VAULT_PATH, name)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Created note {name}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
