import os

dest = r'C:\Users\visio\Projects\visionivx-domains'

old = 'We may use privacy-friendly, first-party analytics to understand which pages are viewed and which options interest visitors. This data is aggregated, does not identify you personally, and is not shared with advertising networks. We do not use Google Analytics or third-party advertising trackers.'

new = 'We use Google Analytics (GA4) to understand which pages are viewed and how visitors interact with the site. This data is aggregated and does not identify you personally. No advertising trackers or cross-site tracking cookies are used.'

fixed = 0
skipped = 0

for domain in os.listdir(dest):
    dst_file = os.path.join(dest, domain, 'index.html')
    if os.path.exists(dst_file):
        with open(dst_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if old in content:
            content = content.replace(old, new)
            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print('Fixed: ' + domain)
            fixed += 1
        else:
            skipped += 1

print(f'\nDone: {fixed} fixed, {skipped} skipped')
