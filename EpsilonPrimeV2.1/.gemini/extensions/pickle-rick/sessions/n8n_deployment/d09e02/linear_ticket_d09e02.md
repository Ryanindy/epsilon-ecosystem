---
id: d09e02
title: "Configure n8n Persistence (Service/PM2)"
status: Done
priority: High
project: project
created: 2026-02-07
updated: 2026-02-07
links:
  - url: ../linear_ticket_parent.md
    title: Parent Ticket
  - url: plan_2026-02-07.md
    title: PM2 Persistence Plan
  - url: n8n.json
    title: PM2 Config File
labels: [infrastructure, devops]
assignee: Pickle Rick
---

# Description

## Problem to solve
If the machine reboots or the terminal closes, n8n might die. We need a "God Mode" persistence strategy.

## Solution
Formalize the n8n execution using a Windows Service (NSSM) or PM2. Ensure it starts on boot and logs correctly.

# Discussion/Comments

- 2026-02-07 Pickle Rick: Planning complete. Moving to PM2 management for process isolation and auto-restart. Will use `pm2 start` with the global n8n binary.
- 2026-02-07 Pickle Rick: Implementation complete. n8n is running via PM2 (n8n-sovereign). Configured pm2-windows-startup for boot persistence. Verified 200 OK on public Tailscale URL.
