<#
=====================================================================
 VisionVix - Mass Deploy: Vercel + GoDaddy DNS  (PowerShell 5.1 safe)
 ---------------------------------------------------------------------
 PROVEN PATTERN (tested on aiscriptgenerator.app + airpg.app):
   1. vercel deploy .\<folder> --prod --yes      (from repo root)
   2. vercel domains add <domain> <domain>       (+ www)
   3. PUT A record 76.76.21.21 to GoDaddy
   4. verify

 KEY LESSONS BAKED IN:
   - Apex A record = 76.76.21.21  (NOT 216.150.1.1)
   - Deploy by pointing at the folder from repo root (avoids "no files")
   - NO vercel.json (a BOM-encoded one corrupts the project to "services")
   - www auto-configures once apex A is set (no separate CNAME needed)

 RUN FROM THE REPO ROOT (C:\Users\visio\Projects\visionivx-domains):
   # set key once per session:
   $env:GODADDY_KEY    = "your_key"
   $env:GODADDY_SECRET = "your_secret"

   pwsh ./deploy.ps1 -Limit 10            # first run: just 10 to prove the script
   pwsh ./deploy.ps1 -Limit 100           # then bigger batches
   pwsh ./deploy.ps1                       # no limit = all remaining
   pwsh ./deploy.ps1 -Only airpg.app       # one specific domain
   pwsh ./deploy.ps1 -SkipDns              # deploy only, skip GoDaddy

 AUTO-SKIP: domains already marked OK in deploy-results.csv are skipped,
 so you can re-run safely and it picks up where it left off.
=====================================================================
#>

param(
  [int]$Limit = 0,
  [string]$Only = "",
  [switch]$SkipDns,
  [switch]$Redo,
  [string]$DomainsFile = "domains.txt",
  [int]$DelaySeconds = 2
)

$ErrorActionPreference = "Stop"
$VERCEL_A = "76.76.21.21"

$GODADDY_KEY    = $env:GODADDY_KEY
$GODADDY_SECRET = $env:GODADDY_SECRET

if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
  Write-Host "STOP: Vercel CLI not found. npm i -g vercel ; vercel login" -ForegroundColor Red; exit 1
}
if ((-not $GODADDY_KEY -or -not $GODADDY_SECRET) -and -not $SkipDns) {
  Write-Host "STOP: set `$env:GODADDY_KEY and `$env:GODADDY_SECRET first (or use -SkipDns)." -ForegroundColor Red; exit 1
}
if (-not (Test-Path $DomainsFile)) {
  Write-Host "STOP: $DomainsFile not found in this folder." -ForegroundColor Red; exit 1
}

$domains = Get-Content $DomainsFile |
  ForEach-Object { $_.Trim() } |
  Where-Object { $_ -ne "" -and -not $_.StartsWith("#") }

if ($Only -ne "") { $domains = $domains | Where-Object { $_ -eq $Only } }

$logFile = "deploy-results.csv"
$done = @{}
if ((Test-Path $logFile) -and -not $Redo) {
  Import-Csv $logFile | Where-Object { $_.result -eq "ok" } | ForEach-Object { $done[$_.domain] = $true }
}
if (-not (Test-Path $logFile)) {
  "domain,result,timestamp,note" | Out-File $logFile -Encoding ascii
}

$todo = $domains | Where-Object { -not $done.ContainsKey($_) }
if ($Limit -gt 0) { $todo = $todo | Select-Object -First $Limit }

if (-not $todo -or $todo.Count -eq 0) {
  Write-Host "Nothing to do (all done, or list empty)." -ForegroundColor Yellow; exit 0
}

Write-Host "This run: $($todo.Count) domain(s).  Already done: $($done.Count).  A-record: $VERCEL_A" -ForegroundColor Cyan

$headers = @{
  "Authorization" = "sso-key $($GODADDY_KEY):$($GODADDY_SECRET)"
  "Content-Type"  = "application/json"
}
$aBody = '[{"data":"' + $VERCEL_A + '","ttl":600}]'

$ok = 0; $fail = 0

foreach ($domain in $todo) {
  Write-Host "`n=== $domain ===" -ForegroundColor White
  $note = ""

  $folder = ".\$domain"
  if (-not (Test-Path $folder)) {
    Write-Host "  ! folder not found, skipping" -ForegroundColor Yellow
    "$domain,fail,$(Get-Date -f s),folder missing" | Out-File $logFile -Append -Encoding ascii
    $fail++; continue
  }

  # readiness check: must have a non-empty index.html, or skip (NOT logged as ok)
  $indexPath = Join-Path $folder "index.html"
  if (-not (Test-Path $indexPath) -or (Get-Item $indexPath).Length -lt 100) {
    Write-Host "  - not ready (no/empty index.html), skipping" -ForegroundColor Yellow
    "$domain,skipped,$(Get-Date -f s),not ready - no index.html" | Out-File $logFile -Append -Encoding ascii
    continue
  }

  $vj = Join-Path $folder "vercel.json"
  if (Test-Path $vj) { Remove-Item $vj -Force }

  try {
    Write-Host "  deploying..." -ForegroundColor Gray
    vercel deploy $folder --prod --yes 2>&1 | Out-Null

    Write-Host "  attaching domain + www..." -ForegroundColor Gray
    vercel domains add $domain $domain 2>&1 | Out-Null
    vercel domains add "www.$domain" $domain 2>&1 | Out-Null

    if (-not $SkipDns) {
      Write-Host "  writing GoDaddy A @ -> $VERCEL_A ..." -ForegroundColor Gray
      Invoke-RestMethod -Method Put `
        -Uri "https://api.godaddy.com/v1/domains/$domain/records/A/@" `
        -Headers $headers -Body $aBody | Out-Null
    } else { $note = "dns skipped" }

    Write-Host "  OK" -ForegroundColor Green
    "$domain,ok,$(Get-Date -f s),$note" | Out-File $logFile -Append -Encoding ascii
    $ok++
  }
  catch {
    $note = ($_.Exception.Message -replace ',', ';')
    Write-Host "  FAIL: $note" -ForegroundColor Red
    "$domain,fail,$(Get-Date -f s),$note" | Out-File $logFile -Append -Encoding ascii
    $fail++
  }

  Start-Sleep -Seconds $DelaySeconds
}

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host " Done this run.  OK: $ok   FAIL: $fail" -ForegroundColor Cyan
Write-Host " Log: $logFile  (re-run to retry fails; OK ones auto-skip)" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
