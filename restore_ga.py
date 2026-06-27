import os, re

source = r'C:\Users\visio\Desktop\Ready Landing Pages Domains\TO DEPLOY\deployed 19.6'
dest = r'C:\Users\visio\Projects\visionivx-domains'

ga_script = '<!-- Google Analytics -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-HT0138DLZF"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag("js", new Date());\n  gtag("config", "G-HT0138DLZF");\n</script>'

fix = '''<script>
(function(){
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
  function runFix() {
    document.querySelectorAll(".ks-val[data-target]").forEach(function(el) { animateCounter(el); });
    setTimeout(function() {
      var lineEl = document.getElementById("chartLine");
      if (lineEl) {
        lineEl.style.opacity = "1";
      }
      var areaEl = document.getElementById("chartArea");
      if (areaEl) areaEl.style.opacity = "1";
      var dotEl = document.getElementById("chartDot");
      if (dotEl) dotEl.style.opacity = "1";
    }, 1000);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", runFix);
  } else {
    runFix();
  }
})();
</script>'''

for domain in os.listdir(dest):
    dst_file = os.path.join(dest, domain, 'index.html')
    if not os.path.exists(dst_file):
        continue
    with open(dst_file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'<script>\s*\(function\(\)\{.*?runVexCounterChartFix.*?\}\)\(\);\s*</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*window\.addEventListener\("DOMContentLoaded".*?</script>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*\(function\(\)\s*\{[\s\S]*?animateCounter[\s\S]*?\}\)\(\);\s*</script>', '', content, flags=re.DOTALL)
    if 'G-HT0138DLZF' not in content:
        content = content.replace('</head>', ga_script + '\n</head>', 1)
    idx = content.rfind('</body>')
    if idx != -1:
        content = content[:idx] + fix + '\n</body>' + content[idx+7:]
    with open(dst_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: ' + domain)
