---
id: r01
title: "PM2 Restart n8n-sovereign"
status: Done
priority: High
project: project
created: 2026-02-08
updated: 2026-02-08
links:
  - url: prd.md
    title: Restart PRD
labels: [infrastructure, devops]
assignee: Pickle Rick
---

# Description

## Problem to solve
We need to verify that n8n correctly restarts and initializes its triggers.

## Solution
Execute `pm2 restart n8n-sovereign` and monitor the logs.

# Discussion/Comments

- 2026-02-08 Pickle Rick: Restart complete. Fixed PM2 config to include WEBHOOK_URL. n8n is online and managed.
