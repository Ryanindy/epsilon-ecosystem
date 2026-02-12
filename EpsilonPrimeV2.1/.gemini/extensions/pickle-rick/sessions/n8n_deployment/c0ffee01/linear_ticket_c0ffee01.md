---
id: c0ffee01
title: "n8n Process Audit & Environment Mapping"
status: Research in Review
priority: Medium
project: project
created: 2026-02-07
updated: 2026-02-07
links:
  - url: ../linear_ticket_parent.md
    title: Parent Ticket
  - url: research_2026-02-07.md
    title: n8n Process Audit Findings
labels: [research, infrastructure]
assignee: Pickle Rick
---

# Description

## Problem to solve
n8n is running on port 5678 (PID 34604), but we don't know *how* it was started (CMD, PowerShell, service, or background task). This makes it impossible to ensure it restarts automatically.

## Solution
Use `wmic` or `Get-Process` to find the command line and environment of the running n8n instance. Locate the n8n binary/node_modules being used.

# Discussion/Comments

- 2026-02-07 Pickle Rick: Research complete. n8n is running as a global npm package via node.exe. Config is in $HOME\.n8n. It is NOT currently a managed service. Move to ticket d09e02 for persistence setup.
