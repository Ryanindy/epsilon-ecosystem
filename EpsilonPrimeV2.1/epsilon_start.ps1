# EPSILON PRIME V3.0.1 - SOVEREIGN STARTUP SCRIPT
# This script is the single point of entry for launching the entire ecosystem.
# It ensures all services start in the correct order and are managed.

$args_str = $args -join " "
Write-Host "--- LAUNCHING EPSILON PRIME V3.0 ---"
if ($args_str) { Write-Host "[DEBUG] Arguments: $args_str" -ForegroundColor Cyan }

# Step 0: Check Python Availability
$python_cmd = "python.exe"
if (!(Get-Command $python_cmd -ErrorAction SilentlyContinue)) {
    $python_cmd = "python"
    if (!(Get-Command $python_cmd -ErrorAction SilentlyContinue)) {
        Write-Host "[FATAL] Python not found in PATH. Aborting." -ForegroundColor Red
        exit 1
    }
}

# Step 1: Run the Hardened Bootloader
Write-Host "[1/6] Running Hardened Boot Sequence..."
& $python_cmd -u "boot/BOOT.py" $args
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FATAL] Boot sequence failed. Aborting startup." -ForegroundColor Red
    exit 1
}
Write-Host "[SUCCESS] Core services ignited." -ForegroundColor Green

# Step 2: Launch Healer Daemon
Write-Host "[2/6] Launching Self-Healing Daemon..."
Start-Process -FilePath "run_healer.bat" -WindowStyle Hidden
Write-Host "[SUCCESS] Healer active in background." -ForegroundColor Green

# Step 3: Launch Cognitive Loop
Write-Host "[3/6] Igniting Cognitive Loop..."
Start-Process -FilePath $python_cmd -ArgumentList "tools/autonomy/cognitive_loop.py" -WindowStyle Hidden
Write-Host "[SUCCESS] Autonomy Engine Online." -ForegroundColor Green

# Step 4: Verify Key Services are LIVE
Write-Host "[4/6] Verifying Service Ports..."
$services = @{
    "API Bridge" = 5000;
    "n8n"        = 5678;
    "OpenClaw"   = 18789;
}
foreach ($name in $services.Keys) {
    $port = $services[$name]
    try {
        $connection = Test-NetConnection -ComputerName localhost -Port $port -ErrorAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            Write-Host "  - $name (Port $port): LIVE" -ForegroundColor Green
        } else {
            Write-Host "  - $name (Port $port): FAILED TO BIND" -ForegroundColor Red
        }
    } catch {
        Write-Host "  - $name (Port $port): ERROR CHECKING" -ForegroundColor Yellow
    }
}

# Step 5: Run Global Skill Sync (if --sync is passed)
if ($args_str -match "--sync") {
    Write-Host "[5/6] Triggering Global Skill Sync..."
    & $python_cmd "tools/maintenance/skill_sync.py"
} else {
    Write-Host "[5/6] Skipping Skill Sync (No --sync flag)." -ForegroundColor Gray
}

# Step 6: Engage Final Diagnostic
Write-Host "[6/6] Running Final System Diagnostic..."
& $python_cmd -u "tools/sanity_check_v3.py"

Write-Host "--- SOVEREIGN ECOSYSTEM IS OPERATIONAL ---"
