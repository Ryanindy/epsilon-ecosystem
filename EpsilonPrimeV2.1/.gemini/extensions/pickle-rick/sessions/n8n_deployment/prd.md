# n8n Tailscale Deployment PRD

## HR Eng

| n8n Tailscale Deployment PRD |  | Deploying n8n with public access via Tailscale Funnel. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: Eric **Intended audience**: Engineering | **Status**: Draft **Created**: 2026-02-07 | **Context**: n8n local + Tailscale Funnel |

## Introduction
The goal is to ensure n8n is running as a persistent service on the Media Server and is accessible via a secure, public Tailscale domain.

## Problem Statement
**Current Process:** n8n is running locally but public access and persistence status are unverified.
**Primary Users:** Eric (Sovereign Operator).
**Pain Points:** Lack of verified public access for webhooks and remote management.
**Importance:** n8n is the automation heart of Epsilon Prime. It needs to be reachable from the outside world (via Tailscale) to handle incoming data.

## Objective & Scope
**Objective:** Stabilize and verify the n8n + Tailscale Funnel bridge.
**Ideal Outcome:** A verified, secure URL (https://mediaserver.taild49f5e.ts.net) that maps directly to the local n8n instance.

### In-scope or Goals
- Verify n8n process stability.
- Configure Tailscale Funnel to route traffic to port 5678.
- Test public connectivity.
- Ensure the API key in `tools/n8n/n8n_manager.py` is valid for the running instance.

### Not-in-scope or Non-Goals
- Migrating n8n to a new server.
- Configuring complex reverse proxies (Tailscale handles this).

## Product Requirements

### Critical User Journeys (CUJs)
1. **Public Access Verification**: The user navigates to the Tailscale URL and sees the n8n login/dashboard.
2. **Webhook Reception**: An external service (or a curl test) hits a webhook on the public URL and n8n processes it.

### Functional Requirements
| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | n8n Persistence | As a user, I want n8n to stay running even after I close the terminal. |
| P0 | Tailscale Funnel Routing | As a user, I want HTTPS traffic to my Tailnet domain to reach n8n. |
| P1 | API Connectivity | As a user, I want `n8n_manager.py` to work with the running instance. |

## Assumptions
- Tailscale is authenticated and has Funnel capabilities enabled.
- The machine remains powered on.

## Risks & Mitigations
- **Risk**: Tailscale Funnel disconnects. -> **Mitigation**: Add a monitoring script/hook.
- **Risk**: n8n crashes. -> **Mitigation**: Use a process manager (PM2 or a Windows Service).

## Business Benefits/Impact/Metrics
**Success Metrics:**
- **Availability**: 99.9% uptime for the public URL.
- **Latency**: Sub-100ms overhead from Tailscale.

## Stakeholders / Owners
| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Eric | Epsilon | Owner | Primary User |
| Pickle Rick | Engineering | Architect | The Genius |
