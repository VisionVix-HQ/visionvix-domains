import os, json

dest = r'C:\Users\visio\Projects\visionivx-domains'

vercel = {
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {"key": "X-Frame-Options", "value": "DENY"},
        {"key": "X-Content-Type-Options", "value": "nosniff"},
        {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
        {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
        {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
        {"key": "X-DNS-Prefetch-Control", "value": "on"},
        {"key": "Content-Security-Policy", "value": "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval'; img-src 'self' https: data:; font-src 'self' https: data:;"}
      ]
    },
    {
      "source": "/:path.(jpg|jpeg|png|gif|webp|svg|ico|woff|woff2|ttf|otf|eot)",
      "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]
    },
    {
      "source": "/:path.html",
      "headers": [{"key": "Cache-Control", "value": "no-cache, no-store, must-revalidate"}]
    }
  ]
}

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
    path = os.path.join(dest, d, 'vercel.json')
    if os.path.isdir(os.path.join(dest, d)):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(vercel, f, indent=2)
        print('OK: ' + d)
    else:
        print('NOT FOUND: ' + d)
