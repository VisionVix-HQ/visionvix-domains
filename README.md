# VisionVix Domains — mass deploy

One GitHub repo. One folder per domain. One Vercel project per domain.
A single PowerShell script deploys them all and writes the DNS to GoDaddy.

```
visionvix-domains/
├── deploy.ps1              ← the deploy script
├── domains.txt            ← one domain per line (what to deploy)
├── secrets.example.ps1    ← copy to secrets.ps1, add your GoDaddy key
├── .gitignore             ← keeps secrets.ps1 + logs out of git
│
├── aiblogging.app/        ← folder name == domain name, exactly
│   ├── index.html
│   ├── og.jpg  hero.webp  site.webp  app.webp  stats.webp
│   ├── sitemap.xml
│   └── robots.txt
├── symptomchecker.app/
│   └── … (same 8 files)
└── … one folder per domain
```

## Setup (one time)

1. Install + log in to Vercel CLI:
   ```
   npm i -g vercel
   vercel login
   ```
2. Get a **Production** GoDaddy API key+secret: https://developer.godaddy.com/keys
3. Add your key WITHOUT putting it in the repo — pick one:
   - **Env vars (recommended):**
     ```powershell
     $env:GODADDY_KEY    = "your_key"
     $env:GODADDY_SECRET = "your_secret"
     ```
   - **Or a local file:** copy `secrets.example.ps1` → `secrets.ps1`, fill it in.
     (`secrets.ps1` is git-ignored, so it never gets pushed.)

## Deploy

Test ONE domain first:
```powershell
pwsh ./deploy.ps1 -Only aiblogging.app
```

Deploy everything in `domains.txt`:
```powershell
pwsh ./deploy.ps1
```

Deploy without touching DNS (e.g. DNS already set):
```powershell
pwsh ./deploy.ps1 -SkipDns
```

## Results

Every run appends to `deploy-results.csv` (domain, deployed, attached, dns_set,
timestamp, note). Filter that for `fail` to find any that need a re-run.

## Notes

- **Public repo is fine** — the landing pages are for sale, meant to be seen.
  Only the GoDaddy key must stay out (handled above).
- **Vercel plan limits:** 600+ projects may hit Hobby-plan caps or daily deploy
  limits. Check your plan; run in batches if needed (use a smaller domains.txt).
- **Confirm Vercel's DNS targets** in your dashboard match the values at the top
  of deploy.ps1 (A `216.150.1.1`, CNAME `cname.vercel-dns.com`).
