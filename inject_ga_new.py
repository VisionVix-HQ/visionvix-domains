import os

dest = r'C:\Users\visio\Projects\visionivx-domains'

ga_script = '<!-- Google Analytics -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-HT0138DLZF"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag("js", new Date());\n  gtag("config", "G-HT0138DLZF");\n</script>'

domains = [
    "adcopygenerator.app","agreementgenerator.app","aiadcopygenerator.app","aibotbuilder.app",
    "aicertificategenerator.app","aiinvoicegenerator.app","aijson.app","aijsongenerator.app",
    "ailifestyle.app","aimemegenerator.app","aimoney.app","aipapertrading.app",
    "aireceiptgenerator.app","airesumegenerator.app","allergytracker.app","apigenerator.app",
    "apisecurity.app","artscanner.app","barcodescanner.app","bonehealth.app",
    "botgenerator.app","butterflyidentifier.app","casinocalculator.app","certificategenerator.app",
    "chatbotcreator.app","chatbotgenerator.app","cholesteroltest.app","cronvalidator.app",
    "cryptoblackjack.app","csvvalidator.app","datacompliance.app","dataintelligence.app",
    "dentalscanner.app","dkimvalidator.app","domainevaluation.app","earthquakealert.app",
    "equationcalculator.app","eulagenerator.app","exifchecker.app","firewallchecker.app",
    "gasfinder.app","gastracker.app","gdprcompliance.app","glaucomatest.app",
    "glucosetest.app","hearttest.app","hormonetest.app","iotmonitor.app",
    "jackpotcalculator.app","jointhealth.app","jsonminifier.app","jwtvalidator.app",
    "kidneytest.app","legalautomation.app","legaltemplate.app","liveroulette.app",
    "livertest.app","lotterycalculator.app","lotteryodds.app","lotterystatistics.app",
    "lungtest.app","matchpredictor.app","medicalassistant.app","ndagenerator.app",
    "numberpatterns.app","ogchecker.app","onlinebaccarat.app","onlineblackjack.app",
    "onlinecraps.app","outlierchecker.app","outlinegenerator.app","passwordchecker.app",
    "payslipgenerator.app","pokemoncardmaker.app","pokeronline.app","policygenerator.app",
    "pricecomparison.app","proposalgenerator.app","redirectchecker.app","regexgenerator.app",
    "resolutionchecker.app","retinascan.app","robotschecker.app","roulettecalculator.app",
    "scanmymeal.app","schedulegenerator.app","scorepredictor.app","sitemapvalidator.app",
    "slogangenerator.app","softwarelicense.app","spamchecker.app","spfvalidator.app",
    "sportspredictor.app","sslchecker.app","surveygenerator.app","symptomchecker.app",
    "taglinegenerator.app","taxestimator.app","techagent.app","teethscanner.app",
    "teethwhitening.app","telehealthplatform.app","templategenerator.app","termsgenerator.app",
    "threatdetection.app","thyroidhealth.app","thyroidtest.app","tifftopdf.app",
    "titlegenerator.app","trademarkclassification.app","trademarkmonitoring.app",
    "trademarkvaluation.app","trademarkviolation.app","transactionmonitoring.app",
    "translateemail.app","travelassistant.app","trendtrading.app","tsunamialert.app",
    "turkishfood.app","tutoragent.app","txttocsv.app","txttodoc.app","txttohtml.app",
    "txttoimage.app","txttojson.app","txttosvg.app","txttoxml.app","typosquatting.app",
    "uianimation.app","urinetest.app","urlchecker.app","urldecode.app","urlparser.app",
    "uxroadmap.app","vehiclecheck.app","vfcpcalculator.app","virtualdoctor.app",
    "virusscanner.app","voicetesting.app","vpnchecker.app","webptopdf.app",
    "websiteaudit.app","wellnesscoaching.app","wildfiretracker.app","wincalculator.app",
    "wokflowscanning.app","workflowautomation.app","workflowbuilder.app","workflowgenerator.app",
    "writingagent.app","xlsxtopdf.app","xmlvalidator.app","zoningmap.app"
]

for d in domains:
    dst_file = os.path.join(dest, d, 'index.html')
    if not os.path.exists(dst_file):
        print('NOT FOUND: ' + d)
        continue
    content = None
    for enc in ['utf-8', 'cp1252', 'latin-1']:
        try:
            with open(dst_file, 'r', encoding=enc) as f:
                content = f.read()
            break
        except:
            continue
    if content is None:
        print('ENCODING ERROR: ' + d)
        continue
    if 'G-HT0138DLZF' in content:
        print('Already has GA: ' + d)
        continue
    content = content.replace('</head>', ga_script + '\n</head>', 1)
    with open(dst_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: ' + d)
