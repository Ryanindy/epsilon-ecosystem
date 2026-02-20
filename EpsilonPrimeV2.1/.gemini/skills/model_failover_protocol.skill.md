# SKILL: Model Failover Protocol (Tier 1)
**ID:** T1_MODEL_FAILOVER
**AUTHORITY:** EPSILON_CORE
**VERSION:** 1.0.0

## 1. PURPOSE
To prevent system stagnation, infinite loops, and crash cycles caused by Gemini API `RESOURCE_EXHAUSTED` (429) errors. This protocol enforces an immediate, automatic downgrade to the next available model in the Epsilon Model Stack.

## 2. TRIGGER CONDITIONS
The system MUST trigger this protocol if any of the following strings appear in an API error response:
- `quotaId: GenerateRequestsPerMinutePerProjectPerModel-FreeTier`
- `quotaId: GenerateContentInputTokensPerModelPerMinute-FreeTier`
- `quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier`
- `status: RESOURCE_EXHAUSTED`
- `429 Too Many Requests`

## 3. FAILOVER HIERARCHY
The system shall attempt to resolve requests in the following order:
1. **Gemini 2.5 Flash** (Primary for Swarm Workers/Retrieval)
2. **Gemini 2.5 Pro** (Primary for Governance/Audit)
3. **Gemini 2.0 Flash** (Universal Fallback)
4. **Gemini 1.5 Flash** (Emergency/Stability Fallback)

## 4. EXECUTION RULES
1. **Immediate Halt**: On 429 detection, the current model invocation must be aborted immediately.
2. **Back-off Suppression**: Standard exponential back-off for 429 errors is FORBIDDEN if an alternative model in the stack remains untried for the current request.
3. **Model Blacklisting**: The exhausted model MUST be blacklisted for the remainder of the session or until a successful heartbeat check, whichever comes first.
4. **State Preservation**: The prompt and shared state must be preserved and passed to the next model in the hierarchy without modification.

## 5. LOGGING REQUIREMENTS
Every failover event must be logged to `logs/maintenance/failover.log` with:
- Timestamp
- Exhausted Model ID
- Triggering Error Snippet
- Target Model ID

## 6. COMPLIANCE
Failure to implement automatic failover is classified as "System Slop" and violates the Epsilon Prime Constitution v2.1.
