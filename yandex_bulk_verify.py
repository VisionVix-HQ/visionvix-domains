import os
import time
import requests

YANDEX_TOKEN = "y0__wgBEPiEufUIGNuERCD6o8CBGGoUWrOaEH1nuizdWPB6SrA5FSWB"
USER_ID = "2393784952"
GODADDY_KEY = os.environ.get("GODADDY_KEY")
GODADDY_SECRET = os.environ.get("GODADDY_SECRET")

YANDEX_HEADERS = {"Authorization": f"OAuth {YANDEX_TOKEN}"}
GODADDY_HEADERS = {
    "Authorization": f"sso-key {GODADDY_KEY}:{GODADDY_SECRET}",
    "Content-Type": "application/json"
}

def get_domains():
    return sorted([d for d in os.listdir('.') if os.path.isdir(d) and d.endswith('.app')])

def add_domain(domain):
    url = f"https://api.webmaster.yandex.net/v4/user/{USER_ID}/hosts"
    data = {"host_url": f"https://{domain}/"}
    r = requests.post(url, headers=YANDEX_HEADERS, json=data)
    return r.status_code, r.json()

def get_verification_token(host_id):
    url = f"https://api.webmaster.yandex.net/v4/user/{USER_ID}/hosts/{host_id}/verification"
    r = requests.get(url, headers=YANDEX_HEADERS)
    if r.status_code == 200:
        data = r.json()
        for v in data.get("verification_variants", []):
            if v.get("verification_type") == "DNS_RECORD":
                return v.get("dns_record", {}).get("value")
    return None

def write_godaddy_txt(domain, token):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/TXT/@"
    r = requests.get(url, headers=GODADDY_HEADERS)
    existing = r.json() if r.status_code == 200 else []
    yandex_record = {"data": f"yandex-verification: {token}", "ttl": 600}
    if not any(rec.get("data", "").startswith("yandex-verification") for rec in existing):
        existing.append(yandex_record)
    r = requests.put(url, headers=GODADDY_HEADERS, json=existing)
    return r.status_code

def main():
    domains = get_domains()
    print(f"Total domains: {len(domains)}\n")
    success = []
    failed = []
    for i, domain in enumerate(domains):
        print(f"[{i+1}/{len(domains)}] {domain}")
        host_id = f"https:{domain}:443"
        status, result = add_domain(domain)
        if status in [200, 201]:
            print(f"  Added to Yandex")
        elif status == 409:
            print(f"  Already exists")
        else:
            print(f"  Failed to add: {result}")
            failed.append(domain)
            time.sleep(2)
            continue
        time.sleep(1)
        token = get_verification_token(host_id)
        if not token:
            print(f"  Could not get token")
            failed.append(domain)
            time.sleep(2)
            continue
        print(f"  Token: {token}")
        dns_status = write_godaddy_txt(domain, token)
        if dns_status == 200:
            print(f"  TXT written to GoDaddy")
            success.append(domain)
        else:
            print(f"  GoDaddy failed: {dns_status}")
            failed.append(domain)
        time.sleep(2)
    print(f"\nSuccess: {len(success)}")
    print(f"Failed: {len(failed)}")

if __name__ == "__main__":
    main()
