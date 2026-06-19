# VEX SECURITY — Developer Documentation

**Complete Technical Guide for Implementation**
Version 2.1.0 · February 2026 · Status: Pre-Production (Dashboard Prototype Complete)

\---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Dashboard Pages (9 sections)](#3-dashboard-pages)
4. [VEX Manager (Script Builder, Features, Trust Badge)](#4-vex-manager)
5. [Security Modules (8 modules with per-module modes)](#5-security-modules)
6. [Scanner Engine (AI-powered, 13 external checks)](#6-scanner-engine)
7. [Per-Site Detail View (10 tabs)](#7-per-site-detail-view)
8. [Live Attack Monitoring](#8-live-attack-monitoring)
9. [Generated Script Tag (data attributes)](#9-generated-script-tag)
10. [Backend API (what to build)](#10-backend-api)
11. [Database Schema](#11-database-schema)
12. [CDN and Deployment](#12-cdn-and-deployment)
13. [Authentication](#13-authentication)
14. [File Structure](#14-file-structure)
15. [Color Theme and Brand](#15-color-theme-and-brand)
16. [What Is Built vs. What Needs Building](#16-what-is-built-vs-what-needs-building)

\---

## 1\. Project Overview

VEX Security is a **client-side website security platform**. It provides real-time protection against XSS, script injection, form hijacking, session theft, DOM mutation attacks, cryptomining, clickjacking, and CSRF attacks.

The product has **three main components**:

1. **Dashboard (React)** — Admin interface for scanning, monitoring, configuration, and reporting. This is what you have now as a working prototype (`vexbot-dashboard.jsx`).
2. **Runtime Script (`vex-security.min.js`)** — Client-side JavaScript that runs on protected websites. **Needs to be built.**
3. **Backend API** — Receives reports from the runtime script, stores scan results, serves dashboard data. **Needs to be built.**

> \*\*NOTE:\*\* The dashboard prototype is a fully functional React component that demonstrates all UI and UX. The scanner currently uses the Claude AI API to perform real web searches and return real scan data. In production, you will replace the AI scanner with direct API calls to security services.

\---

## 2\. Architecture Overview

### 2.1 How It Works in Production

1. Owner signs up on VEX dashboard, adds their site URL
2. Dashboard scans the site and generates a custom script tag
3. Owner pastes script tag into their site HTML `<head>`
4. `vex-security.min.js` loads from CDN and activates protection modules
5. Runtime script detects attacks and sends reports to backend API
6. Dashboard reads reports from database and shows them in Monitoring page

### 2.2 System Diagram

```
\[Website Visitor Browser]
       |
       v
\[vex-security.min.js]  <── loaded from CDN (cdn.vexbot.io)
    |         |
    | blocks   | reports
    | attacks  | events
    v         v
\[Visitor     \[Backend API]  <── Vercel / Node.js serverless
 protected]      |
                 v
            \[Database]  <── PostgreSQL / Supabase
                 |
                 v
            \[Dashboard]  <── React SPA (vexbot-dashboard.jsx)
             reads data
```

### 2.3 Technology Stack

|Layer|Technology|Notes|
|-|-|-|
|Dashboard|React (JSX)|Single file component, \~1830 lines|
|Runtime Script|Vanilla JS|Must be built. No dependencies. Target <8KB gzipped|
|Backend API|Node.js + Vercel Serverless|REST endpoints for reports, scans, auth|
|Database|PostgreSQL (Supabase)|Sites, scans, events, users tables|
|CDN|Vercel Edge / Cloudflare|Serves `vex-security.min.js` globally|
|Auth|JWT + API keys|Dashboard login + per-site API keys|
|Scanner (current)|Claude AI API|Uses web search to analyze sites. Replace in production|

\---

## 3\. Dashboard Pages

The dashboard has **9 main pages** accessible from the left sidebar. Each page is rendered conditionally based on the `page` state variable.

### 3.1 Dashboard (Home)

The main overview page showing aggregate statistics across all scanned sites.

* **Stats cards** — Total sites scanned, average security score, total findings count, critical+high findings count
* **Score distribution** — Visual breakdown of how many sites score 80+, 50-79, and below 50
* **Recent scans list** — Quick view of last scanned sites with their scores

> Stats are computed from the `allSites` state array using `useMemo`. No backend call needed for this page if sites are loaded on app init.

### 3.2 Scanner

Where users enter URLs to scan. Supports multiple URLs (one per line or comma-separated).

* **URL input** — Textarea accepting multiple URLs
* **Scan button** — Triggers `scanSite()` for each URL. Shows progress (current/total)
* **AI-powered scanning** — Currently calls Claude API with a crafted prompt (`SCAN\_PROMPT`) that instructs Claude to do 4 web searches

> \*\*⚠️ IMPORTANT:\*\* In production, replace the Claude API scanner with direct calls to real security APIs: SecurityHeaders.com, BuiltWith, crt.sh, VirusTotal, DMARC/SPF DNS lookups, etc. The Claude scanner is a prototype that demonstrates the data structure.

### 3.3 Sites

Lists all scanned sites with search, filter, and sort capabilities.

* **Search** — Filters sites by URL text match
* **Filter** — By score range: all, secure (80+), needs work (50-79), at risk (<50)
* **Sort** — By score ascending/descending, by name, by scan date
* **Tags** — Custom color-coded tags per site (production, staging, client, etc.)
* **Click a site** — Opens the `SiteDetail` component with 10 sub-tabs

### 3.4 Findings

Aggregated view of all security findings across all sites, sorted by severity.

* **Severity filter** — All, Critical, High, Medium, Low, Info
* **Site filter** — Filter findings to a specific site
* **Finding cards** — Each shows severity badge, title, description, which site, which category

Finding categories: `headers`, `ssl`, `scripts`, `email`, `dns`, `infrastructure`, `subdomains`, `reputation`, `techstack`, `compliance`, `breaches`

### 3.5 Monitoring

Live attack monitoring panel. Shows real-time security events from the runtime script.

* **Event feed** — Scrollable list of attack events with timestamp, type, source IP, action taken
* **Filter** — By attack type (XSS, injection, form hijack, etc.)
* **Live toggle** — Enables simulated real-time event generation for demo purposes
* **Alert rules** — Custom threshold alerts (e.g., alert if >10 XSS attacks in 5 minutes)

> The monitoring page currently uses \*\*simulated events\*\* generated client-side. In production, events come from the backend API which receives them from the runtime script on protected sites.

### 3.6 Reports

Export and reporting tools.

* **Export format** — CSV or JSON download of all site data
* **White-label** — Company name and logo URL fields for branded PDF reports (placeholder)
* **Email** — Send report to email address (placeholder)
* **Trust Badge** — Preview with link to full configuration in VEX Manager
* **Scheduled scans** — Enable/disable automatic recurring scans with frequency selector

### 3.7 Compare

Side-by-side comparison of 2+ sites. Uses the `ComparePage` component.

* **URL input** — Enter URLs to compare (comma-separated)
* **Comparison table** — Score, SSL, headers, email security, WAF, CDN for each site
* **Visual diff** — Color-coded cells showing which site is stronger in each category

### 3.8 VEX Manager

The most complex page. This is where site owners configure the VEX runtime script. Has **3 sub-tabs**: Builder, Features, Trust Badge. See [Section 4](#4-vex-manager) for complete details.

### 3.9 Settings

Global application settings.

* **Alert threshold** — Minimum severity to trigger notifications
* **Notifications toggle** — Enable/disable alert notifications
* **Scheduled scans** — Frequency and enable/disable
* **Export** — Same as Reports page export

\---

## 4\. VEX Manager

This is the core configuration interface. It generates the script tag that site owners paste into their HTML.

### 4.1 Builder Tab

#### Configuration Card

* **Site ID** — Unique identifier for the site. Maps to `data-id` attribute on the script tag
* **Whitelisted Domains** — Comma-separated list of trusted domains that security modules should not block
* **Report Endpoint** — URL where the runtime script sends attack reports
* **Script Placement** — `<head>` (recommended, earliest protection) or `</body>`

#### SRI (Subresource Integrity)

* **Version selector** — Choose which VEX version to use (2.1.0, 2.0.4, 2.0.0, 1.5.2)
* **Compute SRI** — Uses Web Crypto API to SHA-384 hash the script from CDN
* **Verify** — Re-fetches and compares hash to detect tampering
* **Custom URL** — Override CDN URL for self-hosted deployments

> SRI computation uses the real Web Crypto API (`crypto.subtle.digest`). It will fail in the prototype since the CDN URLs are not live yet. In production, it will work once the script is deployed to `cdn.vexbot.io`.

#### Pre-Install Deep Scan

* **URL input** — Enter the site URL to check before installing VEX
* **Deep scan** — Analyzes the site for existing infections, malicious scripts, compromised resources
* **Results** — Shows clean/infected status with detailed findings

#### Protection Mode (Presets)

|Preset|Behavior|
|-|-|
|**⚡ Smart (Recommended)**|Safe modules block, risky modules report. Default for new installs|
|**🛡 Block All**|All 8 modules actively block attacks|
|**📋 Report All**|All modules detect but do NOT block|
|**👁 All Off**|Disable everything. For debugging only|

Presets set all modules at once. Users can then override individual modules.

#### Security Modules (Per-Module Modes)

Each of the 8 modules has its own mode: **Block (B)**, **Report (R)**, or **Off (X)**. See [Section 5](#5-security-modules) for details.

#### VEX Chatbot Toggle

* **Enable/disable** — Adds VEX chatbot script to the generated code
* **API Key** — Required for chatbot functionality
* **Position** — Bottom-right or bottom-left
* **Theme** — Dark or light chatbot UI theme

When enabled, chatbot domains are **auto-whitelisted** so security modules don't block it.

#### Generated Install Code

Shows the complete script tag with all configured options. Copy button copies to clipboard. Also generates matching CSP header.

#### Install Checklist

Visual checklist tracking configuration completeness: infection check passed, SRI hash set, report endpoint configured, CSP generated, placement set, modules configured.

### 4.2 Features Tab

Educational page explaining how VEX works. Shows three pillars: Isolated Modules, Whitelist System, Single Load. Also shows each security module with its risk level, description, and false positive warnings.

### 4.3 Trust Badge

Generates embeddable "Secured by VEX AI Agent" badges for site owners to display.

* **Dark variant** — Navy background (`#0f1a2e`) with gold text. For dark-themed sites
* **Light variant** — Cream background (`#fdf8ee`) with dark gold text. For light-themed sites
* **Code preview** — Shows HTML embed code that updates when switching between dark/light
* **Copy button** — Copies the selected variant's embed code

\---

## 5\. Security Modules

VEX has **8 security modules**. Each can independently be set to Block, Report, or Off mode.

|Module|Key|Risk|What It Does|False Positive Risk|
|-|-|-|-|-|
|XSS Attack Blocking|`xss`|LOW|Detects and blocks cross-site scripting payloads|Rare. Safe to block immediately|
|Script Injection Detection|`scriptInject`|**HIGH**|Monitors for unauthorized `<script>` tags added to DOM|Blocks Google Analytics, Stripe, chat widgets, ad scripts, A/B tools|
|Form Hijack Prevention|`formHijack`|MEDIUM|Protects forms from action URL redirection|Payment gateways (Stripe, PayPal) modify form actions legitimately|
|Session Theft Protection|`sessionTheft`|LOW|Guards cookies and session tokens from exfiltration|Rare. Safe to block immediately|
|DOM Mutation Monitoring|`domMutation`|**HIGH**|Watches for suspicious page structure changes|React/Vue/Angular constantly mutate DOM. Sliders, modals, lazy-load all trigger this|
|Cryptominer Detection|`cryptominer`|SAFE|Blocks unauthorized cryptocurrency mining|Almost zero false positives|
|Clickjacking Shield|`clickjack`|LOW|Prevents UI redress via invisible iframe overlays|Rare. Safe to block immediately|
|CSRF Token Validation|`csrfProtect`|MEDIUM|Verifies CSRF tokens on form submissions|Sites without CSRF tokens have every form flagged|

### 5.1 Smart Preset (Default Configuration)

|Module|Mode|Reason|
|-|-|-|
|XSS Blocking|**BLOCK**|Low risk, safe immediately|
|Script Injection|REPORT|HIGH risk — test for false positives first|
|Form Hijack|REPORT|MEDIUM risk — test checkout flows first|
|Session Theft|**BLOCK**|Low risk, safe immediately|
|DOM Mutation|REPORT|HIGH risk — test on dynamic sites first|
|Cryptominer|**BLOCK**|SAFE — almost zero false positives|
|Clickjacking|**BLOCK**|Low risk, safe immediately|
|CSRF Protection|REPORT|MEDIUM risk — test form behavior first|

### 5.2 Per-Module Mode in Script Tag

The generated script tag encodes each module's mode in the `data-modules` attribute:

```html
<script
  src="https://cdn.vexbot.io/v2/vex-security.min.js"
  integrity="sha384-\[hash]"
  crossorigin="anonymous"
  data-id="example.com"
  data-modules="xss:block,scriptInject:report,formHijack:report,sessionTheft:block,domMutation:report,cryptominer:block,clickjack:block,csrfProtect:report"
  data-whitelist="cdn.vexbot.io,google-analytics.com"
  data-report="https://api.vexbot.io/v1/report"
></script>
```

> The runtime script (`vex-security.min.js`) must parse the `data-modules` attribute and initialize each module with its specified mode. Modules set to `off` should not be loaded at all to save bandwidth.

\---

## 6\. Scanner Engine

### 6.1 Current Implementation (Prototype)

The scanner currently uses the **Claude AI API** to perform real web searches and return structured security data. Flow:

1. `scanSite(url)` is called for each URL
2. A detailed prompt (`SCAN\_PROMPT`) instructs Claude to do 4 web searches
3. Claude returns a JSON object with all security data
4. Dashboard parses the JSON and adds it to `allSites` state
5. `SiteDetail` component renders the data across 10 tabs

### 6.2 Scan Data Structure

Each scanned site produces this JSON:

```json
{
  "url": "https://example.com",
  "status": "scanned",
  "score": 72,
  "platform": "WordPress",
  "platformVersion": "6.4",
  "ssl": {
    "status": "valid",
    "expiry": "2026-08-15",
    "issuer": "Let's Encrypt"
  },
  "headers": {
    "csp": { "present": true, "note": "default-src 'self'..." },
    "xframe": { "present": true, "note": "DENY" },
    "hsts": { "present": false, "note": "Missing" },
    "xcontent": { "present": true },
    "xxss": { "present": true },
    "referrer": { "present": false },
    "permissions": { "present": false }
  },
  "scripts": {
    "total": 12,
    "thirdParty": 5,
    "suspicious": 1,
    "list": \["..."]
  },
  "cookies": { "total": 8, "thirdParty": 3 },
  "emailSecurity": {
    "spf": { "present": true, "note": "v=spf1..." },
    "dkim": { "present": true },
    "dmarc": { "present": false, "note": "Missing" }
  },
  "dns": {
    "nameservers": "...",
    "dnssec": true,
    "registrar": "..."
  },
  "infrastructure": {
    "waf": "Cloudflare",
    "cdn": "Cloudflare",
    "server": "nginx"
  },
  "subdomains": {
    "found": 15,
    "notable": \["api.example.com", "admin.example.com"]
  },
  "reputation": {
    "blacklisted": false,
    "breachExposure": "none"
  },
  "techStack": {
    "frontend": "React",
    "analytics": "GA4",
    "payment": "Stripe"
  },
  "compliance": {
    "gdprBanner": true,
    "privacyPolicy": true
  },
  "findings": \[
    {
      "severity": "high",
      "title": "Missing HSTS",
      "description": "...",
      "category": "headers"
    }
  ],
  "summary": "Site has moderate security...",
  "scannedAt": "2026-02-18T14:30:00Z"
}
```

### 6.3 Production Scanner (What to Build)

Replace the Claude API calls with direct API integrations:

|Check|API / Service|What It Returns|
|-|-|-|
|HTTP Headers|securityheaders.com API or direct HEAD request|CSP, HSTS, X-Frame-Options, X-Content-Type, etc.|
|SSL Certificate|SSL Labs API or `openssl s\_client`|Cert validity, expiry date, issuer, chain|
|Tech Stack|BuiltWith / Wappalyzer API|Platform, framework, CDN, WAF, analytics|
|DNS Records|DNS over HTTPS or `dig`|SPF, DKIM, DMARC, nameservers, DNSSEC|
|Subdomains|crt.sh Certificate Transparency|All known subdomains from CT logs|
|Reputation|VirusTotal, Google Safe Browsing|Blacklist status, malware flags|
|Breaches|Have I Been Pwned API|Known data breaches for the domain|
|Vulnerabilities|CVE databases, Shodan|Known CVEs for detected software|
|Compliance|Direct page scan|Cookie banner, privacy policy link|
|Scripts|Direct page scan + VirusTotal|Third-party scripts, suspicious code|

\---

## 7\. Per-Site Detail View

When a user clicks a site in the Sites page, the `SiteDetail` component renders with **10 tabs**:

|Tab|Content|
|-|-|
|**Overview**|Score ring, SSL status, key stats summary, platform badge, quick findings count|
|**Headers**|All 7 HTTP security headers with present/missing dots, notes, and recommendations|
|**Email**|SPF, DKIM, DMARC status with detailed record values|
|**Infrastructure**|WAF, CDN, hosting provider, server software|
|**Subdomains**|Count of discovered subdomains, notable ones listed (admin, api, staging, etc.)|
|**Reputation**|Blacklist status, breach exposure|
|**Tech Stack**|Frontend framework, analytics, payment processor, CMS, detected technologies|
|**Compliance**|GDPR banner present, privacy policy found, cookie consent|
|**Findings**|All findings for this specific site, sorted by severity with category badges|
|**Install**|Per-site script tag generator with its own module config, placement, presets, CSP header, install checklist|

### 7.1 Install Tab (Per-Site)

Each site's Install tab is **independent** from the global VEX Manager. It generates a site-specific script tag with:

* Unique `data-id` based on the site's domain
* Its own per-module mode configuration (B/R/X toggles)
* Quick presets (Smart, Block All, Report All)
* Placement selector (head vs body)
* Chatbot toggle
* Auto-generated CSP header
* Step-by-step install guide

> The Install tab state (`instModules`, `instPlacement`, etc.) is local to each `SiteDetail` render. It does not affect the global VEX Manager configuration.

\---

## 8\. Live Attack Monitoring

### 8.1 Event Structure

```json
{
  "id": "evt\_1708281234567",
  "type": "xss",
  "site": "example.com",
  "ip": "203.0.113.42",
  "source": "Ukraine",
  "blocked": true,
  "timestamp": "2026-02-18T14:30:00Z",
  "details": "Reflected XSS via search parameter",
  "module": "xss"
}
```

### 8.2 Attack Types

|Type Key|Display Name|
|-|-|
|`xss`|XSS Attack|
|`injection`|Script Injection|
|`formHijack`|Form Hijack|
|`sessionTheft`|Session Theft|
|`domMutation`|DOM Mutation|
|`cryptominer`|Cryptominer|
|`clickjack`|Clickjacking|
|`csrf`|CSRF Attack|

### 8.3 Production Flow

1. Runtime script detects an attack on a visitor's browser
2. Script sends POST to the report endpoint (`data-report` attribute)
3. Backend API validates the event and stores it in database
4. Dashboard polls or uses WebSocket to show events in real-time
5. Alert rules trigger notifications when thresholds are exceeded

\---

## 9\. Generated Script Tag

The script tag uses HTML data attributes for configuration. The runtime script reads these on load.

|Attribute|Example Value|Purpose|
|-|-|-|
|`data-id`|`example.com`|Identifies which site this installation belongs to|
|`data-modules`|`xss:block,scriptInject:report,...`|Per-module mode string. Format: `key:mode` pairs comma-separated. Modes: `block`, `report`, `off`|
|`data-whitelist`|`cdn.vexbot.io,google.com`|Comma-separated trusted domains. Security modules skip these|
|`data-report`|`https://api.vexbot.io/v1/report`|URL where attack events are POSTed. If empty, events log to console only|
|`integrity`|`sha384-...`|SRI hash for tamper detection. Browser refuses to execute if mismatch|
|`crossorigin`|`anonymous`|Required when using `integrity` attribute|

### 9.1 CSP Header

The dashboard also generates a matching Content-Security-Policy header:

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://cdn.vexbot.io;
  style-src 'self' 'unsafe-inline';
  connect-src 'self';
  img-src 'self' data:;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
```

\---

## 10\. Backend API

### 10.1 Endpoints

|Method|Path|Purpose|
|-|-|-|
|`POST`|`/api/v1/report`|Receive attack events from runtime script. No auth (uses `data-id` to identify site)|
|`GET`|`/api/v1/events?site=X\&since=T`|Fetch attack events for dashboard Monitoring page. Requires auth|
|`POST`|`/api/v1/scan`|Trigger a server-side scan of a URL. Returns scan results JSON|
|`GET`|`/api/v1/sites`|List all sites for the authenticated user|
|`GET`|`/api/v1/sites/:id`|Get full scan data for one site|
|`PUT`|`/api/v1/sites/:id/config`|Update site configuration (modules, whitelist, etc.)|
|`POST`|`/api/v1/auth/login`|Authenticate user, return JWT|
|`POST`|`/api/v1/auth/register`|Create new user account|
|`GET`|`/api/v1/stats`|Aggregate stats for dashboard home page|

### 10.2 Report Endpoint Detail

The `/api/v1/report` endpoint is the most critical. It receives events from every visitor on every protected site. It must be:

* **Fast:** respond in <50ms, process asynchronously
* **Rate-limited:** prevent abuse from single IP
* **Validated:** check `data-id` exists in database, validate event schema
* **CORS enabled:** runtime script sends from any domain

```json
// Expected POST body from runtime script:
{
  "siteId": "example.com",
  "type": "xss",
  "blocked": true,
  "details": "Reflected XSS in search param",
  "ip": "203.0.113.42",
  "userAgent": "Mozilla/5.0...",
  "url": "https://example.com/search?q=<script>",
  "timestamp": "2026-02-18T14:30:00Z"
}
```

\---

## 11\. Database Schema

Recommended PostgreSQL tables:

### users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password\_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  plan VARCHAR(50) DEFAULT 'free',
  created\_at TIMESTAMPTZ DEFAULT NOW()
);
```

### sites

```sql
CREATE TABLE sites (
  id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
  user\_id UUID REFERENCES users(id),
  url VARCHAR(500) NOT NULL,
  domain VARCHAR(255) NOT NULL,
  config JSONB DEFAULT '{}',     -- modules, whitelist, report\_url, etc.
  last\_scan JSONB,                -- full scan result JSON
  score INTEGER DEFAULT 0,
  status VARCHAR(50) DEFAULT 'pending',
  tags TEXT\[] DEFAULT '{}',
  created\_at TIMESTAMPTZ DEFAULT NOW(),
  scanned\_at TIMESTAMPTZ
);
```

### events

```sql
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
  site\_id UUID REFERENCES sites(id),
  type VARCHAR(50) NOT NULL,     -- xss, injection, formHijack, etc.
  blocked BOOLEAN DEFAULT false,
  ip VARCHAR(45),
  source\_country VARCHAR(100),
  details TEXT,
  url TEXT,
  user\_agent TEXT,
  module VARCHAR(50),
  created\_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx\_events\_site ON events(site\_id, created\_at DESC);
CREATE INDEX idx\_events\_type ON events(type);
```

### scans

```sql
CREATE TABLE scans (
  id UUID PRIMARY KEY DEFAULT gen\_random\_uuid(),
  site\_id UUID REFERENCES sites(id),
  result JSONB NOT NULL,          -- full scan JSON
  score INTEGER,
  findings\_count INTEGER,
  created\_at TIMESTAMPTZ DEFAULT NOW()
);
```

\---

## 12\. CDN and Deployment

### 12.1 Files to Deploy

|File|CDN Path|Purpose|
|-|-|-|
|`vex-security.min.js`|`cdn.vexbot.io/v2/vex-security.min.js`|Runtime protection script. **Must be built**|
|`vex-logo.png`|`cdn.vexbot.io/badge/vex-logo.png`|Trust badge logo image|
|`vexchat.min.js`|`cdn.vexbot.io/chat/v1/vexchat.min.js`|Chatbot widget script (optional)|

### 12.2 Versioning

|Version|Path|Notes|
|-|-|-|
|2.1.0|`/v2/vex-security.min.js`|Latest — all 8 modules|
|2.0.4|`/v2/vex-security@2.0.4.min.js`|Hotfix — XSS bypass patch|
|2.0.0|`/v2/vex-security@2.0.0.min.js`|Added CSRF + clickjack|
|1.5.2|`/v1/vex-security.min.js`|Legacy — 6 modules|

### 12.3 Recommended Setup

* Deploy CDN files to Vercel Edge Network or Cloudflare Workers
* Set `Cache-Control: public, max-age=31536000, immutable` for versioned files
* Set `Access-Control-Allow-Origin: \*` on all CDN files
* Enable Brotli compression (target <8KB for runtime script)

\---

## 13\. Authentication

* **JWT tokens** for dashboard sessions (stored in httpOnly cookie)
* **API keys** for per-site runtime script identification (`data-id` attribute)
* **OAuth** (Google, GitHub) as optional login methods
* **Rate limiting** on all API endpoints
* **CORS** restricted to dashboard domain for authenticated endpoints
* **Report endpoint** (`/api/v1/report`) does NOT require auth but validates `data-id` exists

\---

## 14\. File Structure

### 14.1 Current (Prototype)

```
vexbot-dashboard.jsx     // Entire dashboard (\~1830 lines, single React component)
```

### 14.2 Recommended Production Structure

```
vex-security/
├── dashboard/                    # React app
│   └── src/
│       ├── components/
│       │   ├── Sidebar.jsx
│       │   ├── Dashboard.jsx     # Home page
│       │   ├── Scanner.jsx
│       │   ├── Sites.jsx
│       │   ├── SiteDetail.jsx    # With 10 sub-tabs
│       │   ├── Findings.jsx
│       │   ├── Monitoring.jsx
│       │   ├── Reports.jsx
│       │   ├── Compare.jsx
│       │   ├── VexManager.jsx    # Builder + Features + Trust Badge
│       │   ├── Settings.jsx
│       │   └── ui/               # Shared components
│       │       ├── Card.jsx
│       │       ├── Btn.jsx
│       │       ├── Badge.jsx
│       │       ├── Input.jsx
│       │       ├── ScoreRing.jsx
│       │       ├── Icon.jsx
│       │       └── EmptyState.jsx
│       ├── hooks/
│       │   ├── useScan.js        # Scanner logic
│       │   └── useEvents.js      # Real-time event subscription
│       ├── api/
│       │   └── client.js         # API client with auth
│       ├── theme.js              # Color vars, gold/cyan/brand
│       └── App.jsx
│
├── runtime/                      # vex-security.min.js source
│   ├── src/
│   │   ├── core.js              # Module loader, config parser
│   │   ├── modules/
│   │   │   ├── xss.js
│   │   │   ├── script-inject.js
│   │   │   ├── form-hijack.js
│   │   │   ├── session-theft.js
│   │   │   ├── dom-mutation.js
│   │   │   ├── cryptominer.js
│   │   │   ├── clickjack.js
│   │   │   └── csrf.js
│   │   ├── reporter.js          # Sends events to backend
│   │   └── whitelist.js         # Domain whitelist checker
│   └── rollup.config.js         # Bundle and minify
│
├── api/                          # Vercel serverless functions
│   ├── report.js
│   ├── events.js
│   ├── scan.js
│   ├── sites.js
│   └── auth.js
│
└── database/
    ├── schema.sql
    └── migrations/
```

\---

## 15\. Color Theme and Brand

VEX brand identity is built around **gold (`#d4a853`)** on dark backgrounds.

### 15.1 CSS Custom Properties

|Variable|Value|Usage|
|-|-|-|
|`--accent`|`#d4a853`|Primary gold. Buttons, headers, borders, nav active|
|`--cyan`|`#00fff9`|Data accent. Score rings, live indicators, scan progress|
|`--bg`|`#0f0f23`|Page background (dark navy)|
|`--card`|`rgba(26,26,46,0.85)`|Card backgrounds (semi-transparent for blur)|
|`--border`|`rgba(212,168,83,0.1)`|Card and section borders (gold tint)|
|`--text1`|`rgba(255,255,255,0.95)`|Primary text (almost white)|
|`--text2`|`rgba(255,255,255,0.75)`|Secondary text (slightly dimmed)|
|`--text3`|`rgba(255,255,255,0.4)`|Muted text (labels)|
|`--mono`|`JetBrains Mono, SF Mono, Fira Code`|Monospace font for code, badges, data|

### 15.2 Functional Colors (Do Not Change)

|Color|Hex|Usage|
|-|-|-|
|Green|`#00e676`|Secure, pass, block success, enabled|
|Red|`#ff1744`|Critical, danger, high risk|
|Orange|`#ff6d00` / `#ffab00`|Medium risk, warnings|
|Magenta|`#ff00ff`|Chatbot section exclusively|
|Blue|`#4fc3f7`|Low severity findings|

### 15.3 Brand Assets

* **Logo:** Gold V-shaped robot (embedded as base64 PNG in `VexBotLogo` component)
* **Brand name:** "VEX Bot" (sidebar) or "VEX Security" (formal)
* **Trust badge:** "Secured by VEX AI Agent" with robot logo — dark and light variants

\---

## 16\. What Is Built vs. What Needs Building

### ✅ DONE — Dashboard Prototype

* Complete React dashboard with 9 pages, all functional
* AI-powered scanner using Claude API (13 checks, returns real data)
* Per-site detail view with 10 tabs
* Script tag generator with per-module modes (B/R/X per module)
* SRI hash computation (Web Crypto API)
* CSP header auto-generation
* Pre-install deep infection scan
* Live attack monitoring with simulation
* Compare page for side-by-side analysis
* Export (CSV/JSON)
* Trust badge generator (dark/light variants with copy)
* Complete gold brand theme

### 🔨 NEEDS BUILDING

#### Priority 1: Runtime Script (`vex-security.min.js`)

* Core module loader that reads `data-modules` attribute
* 8 security modules implementing detection and blocking logic
* Whitelist checker for trusted domains
* Event reporter that POSTs to `data-report` URL
* **Must be <8KB gzipped, zero dependencies, vanilla JS**

#### Priority 2: Backend API

* Node.js / Vercel serverless functions for all endpoints listed in Section 10
* PostgreSQL database setup (schema in Section 11)
* Report ingestion endpoint (high-volume, low-latency)
* Scan endpoint that calls real security APIs
* Authentication system (JWT + API keys)

#### Priority 3: Production Scanner

* Replace Claude AI scanner with direct API calls
* SecurityHeaders.com integration
* SSL Labs or openssl checks
* BuiltWith / Wappalyzer for tech stack
* crt.sh for subdomain discovery
* VirusTotal for reputation
* DNS queries for SPF/DKIM/DMARC

#### Priority 4: Infrastructure

* Deploy CDN files (`vex-security.min.js`, badge assets)
* Set up database (Supabase recommended)
* Configure Vercel project for API and dashboard
* Domain setup: `cdn.vexbot.io`, `api.vexbot.io`, `app.vexbot.io`
* SSL certificates for all subdomains

#### Priority 5: Enhancements

* WebSocket for real-time monitoring (replace polling)
* PDF report generation (white-label)
* Email notifications for alerts
* Team / organization support
* Billing and plan management

\---

*Confidential — VEX Bot Security*

