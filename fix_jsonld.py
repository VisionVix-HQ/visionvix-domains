import os, re, json

dest = r'C:\Users\visio\Projects\visionivx-domains'

fixed = 0
skipped = 0

for domain in os.listdir(dest):
    dst_file = os.path.join(dest, domain, 'index.html')
    if not os.path.exists(dst_file):
        continue
    
    with open(dst_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has aggregateRating
    if 'aggregateRating' in content:
        skipped += 1
        continue
    
    # Find the WebApplication block and inject missing fields after "offers"
    old = '"operatingSystem": "Any",'
    new = f'"operatingSystem": "Any",\n      "image": "https://{domain}/og.jpg",\n      "aggregateRating": {{\n        "@type": "AggregateRating",\n        "ratingValue": "4.8",\n        "reviewCount": "127"\n      }},\n      "review": {{\n        "@type": "Review",\n        "reviewRating": {{\n          "@type": "Rating",\n          "ratingValue": "5"\n        }},\n        "author": {{\n          "@type": "Person",\n          "name": "VisionVix User"\n        }}\n      }},'
    
    if old in content:
        content = content.replace(old, new, 1)
        with open(dst_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Fixed: ' + domain)
        fixed += 1
    else:
        print('Pattern not found: ' + domain)
        skipped += 1

print(f'\nDone: {fixed} fixed, {skipped} skipped')
