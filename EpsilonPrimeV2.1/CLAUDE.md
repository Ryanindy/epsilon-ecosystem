# EpsilonPrime V2.1 - Claude Code Project Instructions

## Quick Reference
- **Stack**: Python 3.13 + Flask, Google GenAI, ChromaDB RAG, LangGraph
- **Entry point**: `main_server.py` (Flask app, port configurable)
- **Architecture**: Tri-Mind system (Epsilon governance, Pickle engineering, Jack execution)
- **Auth**: Bearer token via `EPSILON_API_KEY` env var

## Commands
```bash
# Start the server
cd "C:/Users/Media Server/EpsilonPrimeV2.1"
python main_server.py

# Install dependencies
pip install -r requirements.txt

# Run with venv
./venv/Scripts/python main_server.py
```

## Architecture
```
EpsilonPrimeV2.1/
  main_server.py        # Flask entry point, API routes, auth
  persona_prompt.py     # AI persona/system prompt configuration
  sms_handler.py        # Twilio SMS handling + AI response generation
  tri_mind_graph.py     # LangGraph-based Tri-Mind cognitive loop
  memory.db             # Local SQLite memory store
  boot/                 # Boot sequence scripts
  commands/             # CLI command modules
  hive/                 # Multi-agent coordination
  mcp/                  # MCP server integrations
  rag/                  # RAG system
    .chromadb/          # Vector store (multiple collections)
    core_knowledge/     # Source documents for RAG ingestion
  skills/               # Skill definitions (.skill.md files)
  templates/            # Flask HTML templates (web UI)
  tools/                # Tool modules
    autonomy/           # Self-healing, autonomous operations
    boot/               # Boot validators
    browser_tools.py    # Playwright browser automation
    engineering/        # Code generation tools
    maintenance/        # Healer, git sync, skill sync
    n8n/                # n8n workflow integration
    osint/              # OSINT research tools
    rag/                # RAG retrieval + warmup
    sovereign_tools.py  # Core sovereign operation tools
    wholesale/          # Wholesale business tools
  logs/                 # Runtime logs
```

## Key Modules
- **tri_mind_graph.py**: LangGraph cognitive loop — Epsilon (strategy), Pickle Rick (engineering), Jack (execution)
- **sms_handler.py**: Processes incoming SMS via Twilio, generates AI responses with client context
- **tools/sovereign_tools.py**: Core tools for file ops, git, system management
- **tools/browser_tools.py**: Playwright-based web automation
- **rag/**: ChromaDB vector store with multiple collections, warmup on boot

## Conventions
- All API routes require Bearer token auth (check_auth middleware)
- Environment variables loaded from `.env` via python-dotenv
- Logging uses Python stdlib `logging` module
- RAG collections are in `rag/.chromadb/`, metadata in `rag/RAG_METADATA.json`
- Tools follow a modular pattern: each in its own file under `tools/`

## Common Pitfalls
- `EPSILON_API_KEY` must be set in `.env` or API auth will fail silently
- ChromaDB binary files are large — be careful with git operations on `rag/.chromadb/`
- Many temp/debug scripts in root (fix_*.py, gen_*.py, etc.) — these are one-off utilities, not part of core
- `__pycache__` directories are tracked in git — consider adding to .gitignore
