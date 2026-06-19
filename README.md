
VisionVix Domains

600+ premium .app domains. All live. All deployed from this repo.

Every folder is a domain. Every domain is a live landing page. One PowerShell script deploys them all — Vercel + GoDaddy API, no manual steps.

→ Browse & buy domains at visionvix.app


Scale

StatValueDomains600+ premium .appStackStatic HTML · Vercel · GoDaddy APIDeploy time~6s per domainScriptOne PowerShell loop, fully automatedDNSWritten via GoDaddy API, no manual config


How it works

visionvix-domains/
├── deploy.ps1                ← one script deploys everything
├── domains.txt               ← one domain per line
│
├── accessibilityaudit.app/   ← folder name == domain, exactly
│   ├── index.html
│   ├── og.jpg
│   ├── hero.webp
│   ├── site.webp
│   ├── app.webp
│   ├── stats.webp
│   ├── sitemap.xml
│   ├── robots.txt
│   ├── manifest.json
│   ├── favicon.png
│   └── apple-touch-icon.png
│
├── accountingassistant.app/
│   └── … same structure
│
└── … one folder per domain

Each domain gets:


Its own Vercel project (auto-named from folder)
A production deploy in ~6 seconds
Domain + www attached via Vercel CLI
A record 76.76.21.21 written to GoDaddy via API
Live and resolving within 30 minutes



Deploy pipeline

Prerequisites


Vercel CLI installed and logged in
GoDaddy Production API key from developer.godaddy.com/keys


Set your GoDaddy keys (never commit these)

powershell# Permanent — set once, works every session
[System.Environment]::SetEnvironmentVariable("GODADDY_KEY", "your_key", "User")
[System.Environment]::SetEnvironmentVariable("GODADDY_SECRET", "your_secret", "User")

Deploy a batch

powershell# Edit $domains array in deploy.ps1, then:
cd C:\path\to\visionvix-domains
.\deploy.ps1

What the script does per domain

powershell# 1. Deploy to Vercel
vercel deploy .\domain.app --prod --yes --name domain-app

# 2. Attach domain + www
vercel domains add domain.app domain-app
vercel domains add www.domain.app domain-app

# 3. Write A record to GoDaddy
Invoke-RestMethod -Method Put `
  -Uri "https://api.godaddy.com/v1/domains/domain.app/records/A/@" `
  -Headers $headers -Body '[{"data":"76.76.21.21","ttl":600}]'

Verify all domains are live

powershellforeach ($d in $domains) {
  $status = try {
    (Invoke-WebRequest -Uri "https://$d" -UseBasicParsing -TimeoutSec 10).StatusCode
  } catch { "unreachable" }
  Write-Host "$d → $status"
}


Security


GoDaddy API keys live in Windows environment variables only — never in code
.gitignore blocks .env, *.key, *.secret, .vercel/, and any secrets file
Landing pages are pure static HTML — no server, no backend, no secrets in files
Public repo is intentional — the domains are for sale, meant to be discovered



Built by

VisionVix — premium domain marketplace and AI tools platform.

All domains in this repo are available for acquisition. Visit the marketplace or open an issue to enquire about a specific domain.