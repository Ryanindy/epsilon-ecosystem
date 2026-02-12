---
id: x02
title: "Trigger Daily Briefing Webhook"
status: Done
priority: High
project: project
created: 2026-02-08
updated: 2026-02-08
links:
  - url: prd.md
    title: Restart PRD
labels: [verification, workflow]
assignee: Pickle Rick
---

# Description

## Problem to solve
Verify the public endpoint is reachable after restart.

## Solution
`curl.exe -X POST https://mediaserver.taild49f5e.ts.net/webhook/daily-briefing` and verify response.

# Discussion/Comments

- 2026-02-08 Pickle Rick: Verified E2E connectivity using a sentinel webhook. n8n accepted the public request correctly after the PM2 restart.
