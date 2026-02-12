# Stop Hook
$ErrorActionPreference = "Stop"

try {
    $DebugLog = Join-Path $HOME ".gemini\extensions\pickle-rick\debug.log"

    function Log-Message([string]$msg) {
        try { Add-Content -Path $DebugLog -Value "[$((Get-Date).ToString('u'))] [StopHook] $msg" -ErrorAction SilentlyContinue } catch {}
    }

    try { 
        $InputStr = $input | Out-String 
        if ([string]::IsNullOrWhiteSpace($InputStr)) { Write-Output '{"decision": "allow"}'; exit 0 }
        $Json = $InputStr | ConvertFrom-Json 
    } 
    catch { Write-Output '{"decision": "allow"}'; exit 0 }

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

    if (-not $State.active -or $State.worker) { Write-Output '{"decision": "allow"}'; exit 0 }

    # Context Check
    if ($State.working_dir) {
        if ((Resolve-Path .).Path -ne (Resolve-Path $State.working_dir).Path) { Write-Output '{"decision": "allow"}'; exit 0 }
    }

    # Check Termination
    $Start = $State.start_time_epoch
    if (-not $Start) { $Start = [DateTimeOffset]::Now.ToUnixTimeSeconds() }
    
    $Elapsed = [DateTimeOffset]::Now.ToUnixTimeSeconds() - $Start
    $MaxTime = ($State.max_time_minutes -as [int]) * 60
    $MaxIter = $State.max_iterations -as [int]
    $Iter = $State.iteration -as [int]
    $Promise = $State.completion_promise

    $ShouldStop = $false

    if ($MaxTime -gt 0 -and $Elapsed -ge $MaxTime) { $ShouldStop = $true; Log-Message "Time Limit" }
    elseif ($MaxIter -gt 0 -and $Iter -ge $MaxIter) { $ShouldStop = $true; Log-Message "Iteration Limit" }
    elseif ($Promise -and $Promise -ne "null") {
        $Prompt = $Json.prompt_response
        $PromiseTag = "<promise>$Promise</promise>"
        if ($Prompt -and $Prompt.IndexOf($PromiseTag, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $ShouldStop = $true; Log-Message "Promise Fulfilled"
        }
    }

    if ($ShouldStop) {
        $State.active = $false
        try { $State | ConvertTo-Json -Depth 10 | Set-Content $StateFile -Encoding UTF8 } catch {}
        Write-Output '{"decision": "allow"}'
        exit 0
    }

    # Block Exit
    Log-Message "Blocking Exit (Iter $Iter)"
    $Feedback = "🥒 **Pickle Rick Loop Active** (Iteration $Iter)"
    if ($MaxIter -gt 0) { $Feedback += " of $MaxIter" }
    if ($Promise -and $Promise -ne "null") { $Feedback += "`n🎯 Target: <promise>$Promise</promise>" }

    Write-Output (@{
        decision = "block"
        systemMessage = $Feedback
        hookSpecificOutput = @{ hookEventName = "AfterAgent"; additionalContext = $State.original_prompt }
    } | ConvertTo-Json -Depth 10)

} catch {
    # Fail open on ANY error
    Write-Output '{"decision": "allow"}'
    exit 0
}