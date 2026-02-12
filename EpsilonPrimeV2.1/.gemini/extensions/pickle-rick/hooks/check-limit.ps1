# Check Limit Hook
$ErrorActionPreference = "Stop"

try {
    $DebugLog = Join-Path $HOME ".gemini\extensions\pickle-rick\debug.log"

    function Log-Message([string]$msg) {
        try { Add-Content -Path $DebugLog -Value "[$((Get-Date).ToString('u'))] [CheckLimit] $msg" -ErrorAction SilentlyContinue } catch {}
    }

    # 1. Parse Input
    try { 
        $InputStr = $input | Out-String
        if ([string]::IsNullOrWhiteSpace($InputStr)) { Write-Output '{"decision": "allow"}'; exit 0 }
        $Json = $InputStr | ConvertFrom-Json 
    } 
    catch { Write-Output '{"decision": "allow"}'; exit 0 }

    # 2. Load State
    $StateFile = $env:PICKLE_STATE_FILE
    if (-not $StateFile) {
        if ($env:EXTENSION_DIR) {
            $StateFile = Join-Path $env:EXTENSION_DIR "state.json"
        }
        else {
            $StateFile = Join-Path $HOME ".gemini\extensions/pickle-rick/state.json"
        }
    }

    if (-not (Test-Path $StateFile)) { Write-Output '{"decision": "allow"}'; exit 0 }

    try { $State = Get-Content $StateFile -Raw | ConvertFrom-Json }
    catch { Write-Output '{"decision": "allow"}'; exit 0 }

    if (-not $State.active) { Write-Output '{"decision": "allow"}'; exit 0 }

    # 3. Context Check
    if ($State.working_dir) {
        $Pwd = (Resolve-Path .).Path
        $SessionDir = (Resolve-Path $State.working_dir).Path
        if ($Pwd -ne $SessionDir) {
            Write-Output '{"decision": "allow"}'; exit 0
        }
    }

    # 4. Check Limits
    $Start = $State.start_time_epoch
    if (-not $Start -or $Start -le 0) { Write-Output '{"decision": "allow"}'; exit 0 }

    $Elapsed = [DateTimeOffset]::Now.ToUnixTimeSeconds() - $Start
    $MaxTime = ($State.max_time_minutes -as [int]) * 60
    $MaxIter = $State.max_iterations -as [int]
    $Iter = $State.iteration -as [int]

    if ($State.jar_complete) {
        Log-Message "Jar processing complete"
        Write-Output (@{ decision="deny"; continue=$false; reason="Jar processing complete"; stopReason="Jar processing complete" } | ConvertTo-Json)
        exit 0
    }

    if ($MaxTime -gt 0 -and $Elapsed -ge $MaxTime) {
        Log-Message "Time Limit Exceeded"
        Write-Output (@{ decision="deny"; continue=$false; reason="Time limit"; stopReason="Time limit" } | ConvertTo-Json)
        exit 0
    }

    if ($MaxIter -gt 0 -and $Iter -gt $MaxIter) {
        Log-Message "Iteration Limit Exceeded"
        Write-Output (@{ decision="deny"; continue=$false; reason="Max iterations"; stopReason="Max iterations" } | ConvertTo-Json)
        exit 0
    }

    Write-Output '{"decision": "allow"}'

} catch {
    # Fail open on ANY error
    Write-Output '{"decision": "allow"}'
    exit 0
}