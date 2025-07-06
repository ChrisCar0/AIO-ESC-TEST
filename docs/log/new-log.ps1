# new-log.ps1
$today = Get-Date -Format "yyyy-MM-dd"
$templatePath = "docs/log/_template.md"
$newLogPath = "docs/log/$today.md"

if (Test-Path $newLogPath) {
    Write-Host "Log already exists for ${today}: ${newLogPath}"
    exit 1
}

Copy-Item -Path $templatePath -Destination $newLogPath
(Get-Content $newLogPath) -replace '{{date}}', $today | Set-Content $newLogPath
Write-Host "✅ Created log: $newLogPath"

code $newLogPath


# Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)
# Type and select Tasks: Run Task
# Choose Create Daily Log