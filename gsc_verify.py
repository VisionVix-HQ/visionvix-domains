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

NEW_DOMAINS = [
    "airpg.app", "airunning.app", "aiscriptgenerator.app", "aisinger.app",
    "aismartcalendar.app", "aisneakers.app", "aisocialmedia.app", "aispamblocker.app",
    "aistatistics.app", "aistockanalysis.app", "aistocknews.app", "aistocktrading.app",
    "aistoryteller.app", "aitalking.app", "aitaskmanager.app", "aitemplategenerator.app",
    "aithermometer.app", "aitrivia.app", "aitrucker.app", "aiuidesign.app",
    "aiunblocked.app", "aivalidation.app", "aivirusscanner.app", "aiworkflowbuilder.app",
    "aiworkflowgenerator.app", "amlmonitoring.app", "analyzedata.app", "analyzemarket.app",
    "anchortool.app", "antiquevaluation.app", "aimathsolver.app", "apitesting.app",
    "artagent.app", "asoagent.app", "assetvaluation.app", "auditsite.app",
    "autonomousagents.app", "babyfeeding.app", "backendroadmap.app", "blockchainstock.app",
    "bloggenerator.app", "blogoptimizer.app", "blogtemplate.app", "blogwriter.app",
    "booktracking.app", "bookvaluation.app", "bookwriting.app", "boundarysurvey.app",
    "brandabuse.app", "brandmonitoring.app", "budgetanalysis.app", "bugbiteidentifier.app",
    "businessroadmap.app", "cadastralsurvey.app", "carbcalculator.app", "cardiagnostic.app",
    "careeragent.app", "carvaluation.app", "chanonicalurlchecker.app",
    "checklistgenerator.app", "checklistui.app", "aicryptoportofolio.app",
    "aisimulation.app", "aismarthome.app", "brandidentity.app", "brandvaluation.app",
    "budgetagent.app"
]

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

    success = 0
    failed = []

    for i, d in enumerate(NEW_DOMAINS):
        url = f"https://{d}/"
        print(f"[{i+1}/{len(NEW_DOMAINS)}] {d}...")
        try:
            result = service.sites().get(siteUrl=url).execute()
            level = result.get("permissionLevel", "unknown")
            if level in ["siteOwner", "siteFullUser"]:
                print(f"  Verified ✓ ({level})")
            else:
                print(f"  Not verified yet — ({level})")
            success += 1
        except HttpError as e:
            print(f"  Failed: {e}")
            failed.append(d)
        time.sleep(2)

    print(f"\n✓ Checked: {success}")
    print(f"✗ Failed: {len(failed)}")
    if failed:
        print("Failed domains:", ", ".join(failed))

if __name__ == "__main__":
    main()
