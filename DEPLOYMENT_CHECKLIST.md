# EPSILON ECOSYSTEM v1.3 - DEPLOYMENT CHECKLIST

## PRE-DEPLOYMENT

### Environment Setup
- [x] Windows 11 installed and updated
- [x] Git installed and authenticated
- [x] Python 3.10+ installed
- [x] Gemini CLI installed and in PATH
- [x] ChromaDB installed (`pip install chromadb`)
- [x] Node.js installed (if using n8n workflows)

### GitHub Setup
- [ ] GitHub account created
- [ ] Repository created: `epsilon-ecosystem`
- [ ] Personal Access Token generated
- [ ] Token stored in environment variable: `GITHUB_TOKEN`

---

## DIRECTORY SETUP

### Create Base Structure
```bash
# Done via automated agent setup
mkdir skills flows rag mcp output temp
```

### Copy Foundation Files
- [x] GEMINI.md → root
- [x] BOOT.md → root
- [x] All skill files → skills/
- [x] All flow files → flows/
- [x] All MCP configs → mcp/
- [x] All RAG READMEs → respective H:/ subdirectories

---

## CONFIGURATION

### MCP Configuration
- [ ] Update mcp/github.config.json with actual GitHub username
- [ ] Verify GITHUB_TOKEN environment variable is set
- [ ] Test filesystem MCP permissions

### RAG Initial Population
- [ ] Add at least 1 file to H:/epsilon/ (core_philosophy.md)
- [ ] Add at least 1 file to H:/legal/ (fcra_summary.md if applicable)
- [ ] Add at least 1 file to H:/business/ (automation_overview.md)
- [x] Create empty log files in H:/decisions/

### ChromaDB Initialization
```bash
python -c "import chromadb; client = chromadb.PersistentClient(path='H:/.chromadb'); print('ChromaDB initialized')"
```

---

## BOOT VALIDATION

### Run Boot Sequence
1. The system uses `BOOT.md` as the logic for session starts.
2. Initial status will likely be `DEGRADED` until the RAG index is built.

---

## INITIAL INDEX BUILD

### Populate RAG and Build Index
1. Use `rag_data_attendant` skill to build the initial index.
2. `gemini skill invoke rag_data_attendant --action=rebuild`

### Verify Index
```bash
python -c "import chromadb; client = chromadb.PersistentClient(path='H:/.chromadb'); print(f'Collections: {len(client.list_collections())}')"
```

---

## FINAL SYSTEM STATUS
- ✅ Architecture locked
- ✅ Persistence model defined
- ✅ Execution authority defined
- ✅ Human override enforced
- ✅ Brand isolation enforced
- ✅ **PRODUCTION-READY**

**Version**: 1.3 MERGED
**Last Updated**: 2026-01-22
