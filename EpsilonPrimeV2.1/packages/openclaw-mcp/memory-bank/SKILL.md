---
name: memory-bank
description: "Graph-based long-term memory for Epsilon Prime. Stores entities, relations, and architectural decisions."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["npx"] },
        "homepage": "https://github.com/modelcontextprotocol/servers"
      }
  }
---

# Memory Bank Skill (Serena)

This skill provides a persistent Knowledge Graph for Claude. It allows the agent to remember facts about the user (Eric Frederick), the project (Epsilon Prime), and previous coding decisions.

## Tools
- `create_entities`: Store new facts.
- `create_relations`: Link facts together.
- `search_nodes`: Recall information based on semantic similarity.
- `read_graph`: View the current structure of the project memory.

## Usage
Use this to "seed" the project's soul. Every time a major architectural change is made, record it in the Memory Bank.
It replaces the legacy `COGNITIVE_LOG.md` with a live, queryable graph.
