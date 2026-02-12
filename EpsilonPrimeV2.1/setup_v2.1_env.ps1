# EPSILON PRIME V2.1 ENVIRONMENT SETUP
# Run this to unify your CLI experience.

$ProfilePath = $PROFILE.CurrentUserCurrentHost
$ProjectRoot = "C:\Users\Media Server\EpsilonPrimeV2.1"

$AliasFunction = @"

function epsilon {
    Set-Location "$ProjectRoot"
    & "$ProjectRoot\epsilon.bat" `$args
}

Set-Alias -Name ep -Value epsilon
"@

if (Test-Path $ProfilePath) {
    $Content = Get-Content $ProfilePath
    if ($Content -match "function epsilon") {
        Write-Host "[!] Epsilon function already exists. Updating..." -ForegroundColor Yellow
        # Simple replacement logic for this specific setup
        $NewContent = $Content -replace 'function epsilon \{[\s\S]*?\}', $AliasFunction
        $NewContent | Set-Content $ProfilePath
    } else {
        Write-Host "[+] Adding Epsilon function to profile..." -ForegroundColor Green
        Add-Content $ProfilePath "`n$AliasFunction"
    }
} else {
    Write-Host "[+] Creating new PowerShell profile..." -ForegroundColor Green
    New-Item -Path $ProfilePath -Type File -Force
    Set-Content $ProfilePath $AliasFunction
}

Write-Host "[!] RESTART POWERSHELL TO APPLY CHANGES." -ForegroundColor Cyan
