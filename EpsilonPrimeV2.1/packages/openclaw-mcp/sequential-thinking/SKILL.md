---
name: sequential-thinking
description: "Forces the model to think in a structured, sequential manner before acting. Essential for complex architecture."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["npx"] },
        "homepage": "https://github.com/modelcontextprotocol/servers"
      }
  }
---

# Sequential Thinking Skill

Use this skill to enable the `thought` tool. When faced with a complex task (e.g., refactoring `tri_mind_graph.py`), you MUST use the `thought` tool to map out your logic steps before writing any code.

## Tools
- `thought`: Enables a reasoning buffer. Parameters: `thought` (string), `step` (int), `total_steps` (int).

## Usage
Trigger this automatically for any task marked as MEDIUM or HIGH risk.
It prevents model hallucinations and ensures tactical consistency.
