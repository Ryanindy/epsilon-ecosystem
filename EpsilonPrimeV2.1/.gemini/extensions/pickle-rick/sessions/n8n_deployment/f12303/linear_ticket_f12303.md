---
id: f12303
title: "Tailscale Funnel E2E Webhook Test"
status: Done
priority: Medium
project: project
created: 2026-02-07
updated: 2026-02-07
links:
  - url: ../linear_ticket_parent.md
    title: Parent Ticket
labels: [verification, network]
assignee: Pickle Rick
---

# Description

## Problem to solve
We see a 200 OK on the public URL, but we haven't verified that a full JSON payload can traverse the funnel and be processed by n8n.

## Solution
Create a test workflow in n8n with a webhook trigger. Send a complex JSON payload via `curl` to the public domain and verify receipt in n8n.

# Discussion/Comments

- 2026-02-07 Pickle Rick: E2E Verification complete. Created sentinel workflow, activated via API, and triggered via public Tailscale URL. Received "Workflow was started" confirmation. Tunnel is rock solid.
