import os, re

source = r'C:\Users\visio\Desktop\Ready Landing Pages Domains\TO DEPLOY\deployed 19.6'
dest = r'C:\Users\visio\Projects\visionivx-domains'

ga_script = '<!-- Google Analytics -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-HT0138DLZF"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag("js", new Date());\n  gtag("config", "G-HT0138DLZF");\n</script>'

fix = '''<script>
window.addEventListener("DOMContentLoaded", function() {
  function animateCounter(el) {
    var target = parseFloat(el.dataset.target);
    var prefix = el.dataset.prefix || "";
    var suffix = el.dataset.suffix || "";
    var decimal = parseInt(el.dataset.decimal || "0", 10);
    var duration = 1400;
    var start = performance.now();
    function step(now) {
      var p = Math.min((now - start) / duration, 1);
      var ease = 1 - Math.pow(1 - p, 3);
      var val = target * ease;
      el.textContent = prefix + (decimal ? val.toFixed(decimal) : Math.round(val).toLocaleString("en-US")) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  document.querySelectorAll(".ks-val[data-target]").forEach(function(el) { animateCounter(el); });
  setTimeout(function() {
    var lineEl = document.getElementById("chartLine");
    if (lineEl) {
      lineEl.style.strokeDashoffset = "0";
      lineEl.style.transition = "none";
    }
  }, 500);
});
</script>'''

for domain in os.listdir(source):
    src_file = os.path.join(source, domain, 'index.html')
    dst_file = os.path.join(dest, domain, 'index.html')
    if os.path.exists(src_file) and os.path.exists(os.path.join(dest, domain)):
        for enc in ['cp1252', 'utf-8', 'latin-1']:
            try:
                with open(src_file, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except:
                continue
        # Inject GA before </head> only if not already there
        if 'G-HT0138DLZF' not in content:
            content = content.replace('</head>', ga_script + '\n</head>', 1)
        # Remove any previous fix attempts
        content = re.sub(r'<script>\s*window\.addEventListener\("DOMContentLoaded".*?</script>\s*', '', content, flags=re.DOTALL)
        # Replace LAST occurrence of </body>
        idx = content.rfind('</body>')
        if idx != -1:
            content = content[:idx] + fix + '\n</body>' + content[idx+7:]
        with open(dst_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('OK: ' + domain)
