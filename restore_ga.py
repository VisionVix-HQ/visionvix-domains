import os

source = r'C:\Users\visio\Desktop\Ready Landing Pages Domains\TO DEPLOY\deployed 19.6'
dest = r'C:\Users\visio\Projects\visionivx-domains'
ga_script = '<!-- Google Analytics -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-HT0138DLZF"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag("js", new Date());\n  gtag("config", "G-HT0138DLZF");\n</script>'

for domain in os.listdir(source):
    src_file = os.path.join(source, domain, 'index.html')
    dst_file = os.path.join(dest, domain, 'index.html')
    if os.path.exists(src_file) and os.path.exists(os.path.join(dest, domain)):
        # Try cp1252 first, then utf-8
        for enc in ['cp1252', 'utf-8', 'latin-1']:
            try:
                with open(src_file, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except:
                continue
        if 'G-HT0138DLZF' not in content:
            content = content.replace('</head>', ga_script + '\n</head>')
        with open(dst_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('OK: ' + domain)
