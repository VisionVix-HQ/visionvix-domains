import os
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_FILE = "gsc_credentials.json"
TOKEN_FILE = "gsc_token.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters"]

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def main():
    # Test domains
    test_domains = {
        "accountingassistant.app": "google4ab88aa673a745c1.html",
        "addressvalidation.app": "google4ab88aa673a745c1.html"
    }

    print("Step 1 — Creating verification files...")
    for domain, filename in test_domains.items():
        filepath = os.path.join(domain, filename)
        content = f"google-site-verification: {filename}"
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  ✓ Created {filepath}")

    print("\nStep 2 — Push to GitHub now:")
    print("  git add .")
    print('  git commit -m "add: google verification files"')
    print("  git push")
    print("\nWait for Vercel to deploy (about 30 seconds), then press Enter to verify...")
    input()

    print("\nStep 3 — Verifying with Google...")
    creds = authenticate()
    service = build("searchconsole", "v1", credentials=creds)

    for domain in test_domains:
        url = f"https://{domain}/"
        print(f"\n=== {domain} ===")
        try:
            result = service.sites().get(siteUrl=url).execute()
            print(f"  Verification status: {result.get('permissionLevel', 'unknown')}")
        except HttpError as e:
            print(f"  ✗ Error: {e}")
        time.sleep(2)

if __name__ == "__main__":
    main()
