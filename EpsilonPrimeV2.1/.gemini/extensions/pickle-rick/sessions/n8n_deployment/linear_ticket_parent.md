---
id: n8n_epic
title: "[Epic] n8n Tailscale Persistence & Verification"
status: Done
priority: High
project: project
created: 2026-02-07
updated: 2026-02-07
links:
  - url: prd.md
    title: n8n Deployment PRD
labels: [infrastructure, n8n, tailscale]
assignee: Pickle Rick
---

# Description

## Problem to solve
n8n is currently running and accessible, but the configuration is unmanaged, the persistence method (how it was started) is unknown, and the Tailscale Funnel reliability for webhooks hasn't been stress-tested.

## Solution
Audit the existing process, formalize the persistence (Windows Service or PM2), and verify end-to-end connectivity via the Tailscale public domain.

# Discussion/Comments

- 2026-02-07 Pickle Rick: Epic complete. n8n transitioned to PM2 management with boot persistence enabled. Public domain verified for webhook traffic. Infrastructure is stabilized.
