# n8n Restart and Workflow Execution PRD

## HR Eng

| n8n Restart and Workflow Execution PRD |  | Cycle n8n process and trigger a production workflow. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: Eric **Intended audience**: Engineering | **Status**: Draft **Created**: 2026-02-08 | **Context**: PM2 + n8n + Tailscale Funnel |

## Introduction
The user wants to verify the stability of the n8n PM2 deployment by performing a full restart and then triggering an active workflow via the public domain.

## Problem Statement
**Current Process:** n8n is running under PM2. We need to verify that it correctly handles a forced restart and remains reachable via Tailscale for functional execution.
**Primary Users:** Eric Frederick.
**Pain Points:** Risk of process hung state or tunnel disconnection during restart.
**Importance:** Critical for ensuring the Daily Briefing and other automations can be triggered on-demand after maintenance.

## Objective & Scope
**Objective:** Perform a clean restart and verify functional execution.
**Ideal Outcome:** n8n restarts, reconnects to the network, and successfully responds to a webhook trigger on the public domain.

### In-scope or Goals
- Shutdown n8n via `pm2 stop`.
- Restart n8n via `pm2 restart` or `pm2 start`.
- Trigger the "Daily Briefing Dispatcher" (Pmi7eP1S8HxJPvZD) via its public webhook endpoint.

### Not-in-scope or Non-Goals
- Modifying the workflow logic.
- Changing Tailscale configuration.

## Product Requirements

### Critical User Journeys (CUJs)
1. **The Cycle**: The operator issues a restart command; the process dies and is reborn.
2. **The Execution**: The operator hits the webhook at `https://mediaserver.taild49f5e.ts.net/webhook/daily-briefing` and receives a success response.

### Functional Requirements
| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | PM2 Management | As a user, I want PM2 to handle the restart sequence safely. |
| P0 | Webhook Accessibility | As a user, I want the webhook to be reachable immediately after restart. |

## Success Metrics:
- **Restart Time**: < 30 seconds.
- **Trigger Success**: HTTP 200/201 from the public endpoint.
