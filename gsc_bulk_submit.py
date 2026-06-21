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
    print("Authenticating...")
    creds = authenticate()
    service = build("searchconsole", "v1", credentials=creds)

    existing = []
    try:
        result = service.sites().list().execute()
        existing = [s['siteUrl'].rstrip('/').replace('https://','') for s in result.get('siteEntry', [])]
        print(f"Already in GSC: {len(existing)}")
    except Exception as e:
        print(f"Could not fetch existing: {e}")

    domains = sorted([d for d in os.listdir('.') if os.path.isdir(d) and d.endswith('.app')])
    print(f"Total domains: {len(domains)}")

    to_add = [d for d in domains if d not in existing]
    print(f"Need to add: {len(to_add)}\n")

    success = []
    failed = []

    for i, d in enumerate(to_add):
        url = f"https://{d}/"
        print(f"[{i+1}/{len(to_add)}] {d}")

        try:
            service.sites().add(siteUrl=url).execute()
            print(f"  ✓ Added")
            success.append(d)
        except HttpError as e:
            if "already exists" in str(e):
                print(f"  ℹ Already exists")
                success.append(d)
            elif "429" in str(e):
                print(f"  ⚠ Rate limited — waiting 30 seconds...")
                time.sleep(30)
                try:
                    service.sites().add(siteUrl=url).execute()
                    print(f"  ✓ Added after retry")
                    success.append(d)
                except:
                    print(f"  ✗ Failed after retry")
                    failed.append(d)
            else:
                print(f"  ✗ Failed: {e}")
                failed.append(d)

        time.sleep(3)

    print(f"\n{'='*40}")
    print(f"✓ Success: {len(success)}")
    print(f"✗ Failed: {len(failed)}")

if __name__ == "__main__":
    main()
