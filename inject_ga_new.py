import os

dest = r'C:\Users\visio\Projects\visionivx-domains'

ga_script = '<!-- Google Analytics -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-HT0138DLZF"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag("js", new Date());\n  gtag("config", "G-HT0138DLZF");\n</script>'

domains = [
    "chefagent.app", "chefassistant.app", "christianmeditation.app", "cloudroadmap.app",
    "codeanalysis.app", "codeoptimizer.app", "coderefactor.app", "codereplicator.app",
    "codesecurity.app", "coinidentifier.app", "comparestock.app", "comparisonchart.app",
    "comparisongenerator.app", "compatibilitytest.app", "compliancematrix.app",
    "compliancereporting.app", "confidencecoaching.app", "contentaccuracy.app",
    "contentautomation.app", "contentroadmap.app", "contractbuilder.app",
    "conversiontracker.app", "cookingagent.app", "cryptonft.app", "cryptoportofolio.app",
    "cssgenerator.app", "datapolicy.app", "debtanalysis.app", "designagent.app",
    "designlayout.app", "developerroadmap.app", "deviceagent.app", "devopsroadmap.app",
    "devopstools.app", "diamondtester.app", "diyagent.app", "djvutopdf.app",
    "documentvalidation.app", "docxtopdf.app", "domainranking.app", "driverbehavior.app",
    "ecommerceautomation.app", "editimage.app", "eercalculator.app", "emailwriter.app",
    "endpointprotection.app", "equitycalculator.app", "equityvaluation.app", "euaiact.app",
    "euailaw.app", "eventagent.app", "faceaging.app", "facerecognition.app",
    "fakenumber.app", "fashionagent.app", "fbacalculator.app", "filipinofood.app",
    "financeautomation.app", "financialcoaching.app", "fitnessagent.app", "fixseo.app",
    "fleetanalytics.app", "fleettracker.app", "focusmusic.app", "foodreviewer.app",
    "foodwaste.app", "forensicaudit.app", "forexbot.app", "fraudalerts.app",
    "frauddetection.app", "frontendroadmap.app", "funnyjokes.app", "gameagent.app",
    "gardeningagent.app", "geofencealerts.app", "giff.app", "goldtrade.app",
    "gpsmapping.app", "greekfood.app", "healthcoaching.app", "homefinancing.app",
    "homeworkagent.app", "hragent.app", "hrautomation.app", "htmlcoding.app",
    "htmlgames.app", "htmlgenerator.app", "htmltoimage.app", "htmltopng.app",
    "improveux.app", "incometracker.app", "industrialautomation.app", "integercalculator.app",
    "inventoryagent.app", "investingagent.app", "iotanalytics.app", "iotautomation.app",
    "iotdeployment.app", "iotgateway.app", "iotintegration.app", "iotmonitoring.app",
    "japanesefood.app", "javascriptgenerator.app", "jobhuntagent.app", "jokesforkids.app",
    "keyloggerdetector.app", "koreanfood.app", "koreanlearning.app", "kycverification.app",
    "languageagent.app", "learnanimation.app", "learnautomation.app", "learnbengali.app",
    "learnblockchain.app", "learnblogging.app", "learncms.app", "learncopywriting.app",
    "learncybersecurity.app", "learnczech.app", "learndanish.app", "learndropshipping.app",
    "learndutch.app", "learnecommerce.app", "learnesperanto.app", "learnfigma.app",
    "learnfilipino.app", "learnfinnish.app", "learngreek.app", "learnhindi.app",
    "learnhungarian.app", "learnicelandic.app", "learnindonesian.app", "learnlatin.app",
    "learnmalay.app", "learnnorwegian.app", "learnpersian.app", "learnpolish.app",
    "learnrobotics.app", "learnromanian.app", "learnsaas.app", "learnseo.app",
    "learnsql.app", "learnswahili.app", "learnswedish.app", "learntamil.app",
    "learntaxes.app", "learnturkish.app", "learnurdu.app", "learnux.app",
    "learnvietnamese.app", "lebanesefood.app", "legalsoftware.app", "linkbuilder.app",
    "linkdecoder.app", "livetranslation.app", "logisticsplanner.app", "lootlocator.app",
    "lotteryscanner.app", "mcpconfig.app", "mcpendpoint.app", "mcphandler.app",
    "mcpinterface.app", "mcpnode.app", "measurment.app", "mentoragent.app",
    "micromechanic.app", "mindsetcoaching.app", "mocklocation.app", "modularai.app",
    "moneyagent.app", "moroccanfood.app", "motivationalcoaching.app", "movieagent.app",
    "musclebooster.app", "musicagent.app", "musicvideo.app", "mvpai.app", "mvptesting.app",
    "nftvaluation.app", "nlpcoaching.app", "onlinereputation.app", "optimizeads.app",
    "optimizecontent.app", "parentingcoaching.app", "payrollcalculator.app",
    "paystubgenerator.app", "pcagent.app", "pdfagent.app", "persianfood.app",
    "personalcoaching.app", "phishingprevention.app", "phoneverification.app", "phpseo.app",
    "planbudget.app", "plantdiagnosis.app", "plantrip.app", "pokeragent.app",
    "ppttopdf.app", "precalculuscalculator.app", "pricingoptimizer.app", "productcard.app",
    "productresearch.app", "promptanalyzer.app", "prompttocode.app", "propertysurvey.app",
    "proteincalculator.app", "pythonroadmap.app", "quitdrinking.app", "rankfaster.app",
    "rapai.app", "recipeagent.app", "reconscanner.app", "redirecttrace.app",
    "relationshipcoaching.app", "renovationagent.app", "researchagent.app",
    "revenueaudit.app", "rewardsagent.app", "riskanalysis.app", "roboticautomation.app",
    "roianalysis.app", "rootkitscanner.app", "rtftopdf.app", "safetymonitoring.app",
    "satelliteimagery.app", "savingstracker.app", "schemamapping.app", "semanticai.app",
    "semantichtml.app", "seoaiagent.app", "seometric.app", "seometrics.app",
    "seoranking.app", "seotaskagent.app", "servertools.app", "simplecalculator.app",
    "snippetgenerator.app", "sodiumcalculator.app", "softwareaudit.app", "songagent.app",
    "spamblocker.app", "spanishtranslation.app", "spiritualcoaching.app",
    "startupvaluation.app", "statisticscalculator.app", "stickyheader.app",
    "studydesign.app", "studygeography.app", "studyhistory.app", "studylaw.app",
    "summarizepaper.app"
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
