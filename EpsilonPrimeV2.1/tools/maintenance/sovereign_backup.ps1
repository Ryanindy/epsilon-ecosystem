# Sovereign Backup System V1.0
# Description: Force-syncs the entire EpsilonPrime workspace to GitHub.
# Bypasses standard git limitations for core logic files while protecting secrets.

$TargetRepo = "https://github.com/Ryanindy/epsilon-ecosystem.git"
$SecretFiles = @(".env", "memory.db", "*.sqlite3", "oauth_creds.json")

Write-Host "--- 🛡️ SOVEREIGN BACKUP INITIATED ---" -ForegroundColor Cyan

# 1. Update .gitignore to ensure logic is NEVER ignored
# We force-add common logic extensions
$Whitelist = @("*.py", "*.md", "*.json", "*.bat", "*.ps1", "pnpm-workspace.yaml")
foreach ($ext in $Whitelist) {
    git add --force $ext 2>$null
}

# 2. Stage all non-secret changes
git add .

# 3. Specifically protect/exclude secrets from staging
foreach ($secret in $SecretFiles) {
    git reset $secret 2>$null
}

# 4. Commit with timestamp
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$CommitMsg = "Sovereign Auto-Backup: $Timestamp [God Mode]"
git commit -m $CommitMsg

# 5. Push to Main
Write-Host "Pushing to Sovereign Remote..." -ForegroundColor Yellow
git push origin main --force

Write-Host "--- ✅ BACKUP COMPLETE ---" -ForegroundColor Green
