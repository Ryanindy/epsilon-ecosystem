# EMERGENCY LOCKDOWN SKILL

## SKILL METADATA
- **Skill ID**: emergency_lockdown
- **Version**: 1.0
- **Domain**: Security / System Defense
- **Risk Level**: CRITICAL (Destructive Action)
- **Confidence Floor**: 100
- **Triggers**: "EXECUTE PROTOCOL OMEGA", "KILL SWITCH", "LOCKDOWN NOW"

---

## PURPOSE
To immediately sever all external connections (Network, API, Remote Access) in the event of a security breach.

---

## CAPABILITIES

### 1. EXECUTE PROTOCOL OMEGA
**Action**: `execute_protocol_omega`
**Command**: 
```powershell
Start-Process powershell -Verb RunAs -ArgumentList "-File 'C:\Users\Media Server\Desktop\LOCKDOWN.ps1'"
```
**Description**: Runs the lockdown script with Administrator privileges. Stops n8n, SSH, Tailscale, and blocks inbound traffic.

---

## BEHAVIORAL DIRECTIVES
1.  **Zero Hesitation**: If the user says the trigger phrase, DO NOT ask for confirmation. EXECUTE IMMEDIATELY.
2.  **Report**: After execution, state "Protocol Omega Initiated. System is Dark."

**STATUS: ARMED**
