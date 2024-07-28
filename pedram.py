# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from time import sleep
from random import choice

def check_internet():
    while True:
        try:
            urls=["https://www.kite.com",
                  "https://www.digikala.com/",
                  "https://www.aparat.com/",
                  "https://www.speedtest.net/",
                  "https://10fastfingers.com/",
                  "https://ibis.org.ir/",
                  "https://tms.iins.ir/login.pc?ReturnUrl=/dashboard.pc",
                  "https://www.sums.ac.ir/",
                  "https://pharmacy.sums.ac.ir/",
                  "https://libgen.is/",
                  "https://faradars.org/",
                  "https://www.aiva.ai/",
                  "https://www.qr-code-generator.com/",
                  "https://exchangeratesapi.io/",
                  "https://fixer.io/",
                  "https://soft98.ir/",
                  "https://www.downloadha.com/",
                  "https://www.isna.ir/",
                  "https://www.p30world.com/",
                  "https://www.softgozar.com/"
                  "https://virgool.io/",
                  "https://www.calculator.net/",
                  "https://reqbin.com/",
                  "https://www.amazon.com/",
                  "http://www.sanjesh.org/",
                  "https://upmusics.com/",
                  "https://www.filimo.com/",
                  "https://telewebion.com/",
                  "https://www.varzesh3.com/",
                  "https://www.namasha.com/",
                  "https://donya-e-eqtesad.com/",
                  "https://divar.ir/",
                  "https://iau.ir/fa",
                  "https://www.emofid.com/",
                  "https://www.dalfak.com/",
                  "https://www.khabaronline.ir/",
                  "https://www.tarafdari.com/",
                  "https://www.wikipedia.org/",
                  "https://sumsnavid.vums.ac.ir/",
                  
                  ]
            url=choice(urls)
            #url="https://www.kite.com"
            request=requests.get(url, timeout=5)
            #print("Connected to the Internet:",url)
            break
        except (requests.ConnectionError, requests.Timeout):
            now=datetime.now()
            print("No internet connection.",now.strftime("%H:%M:%S") ,url)
            sleep(10)

def jsonPath(onlinePath):
    """
    input json path from https://jsonpathfinder.com/
    
    example:
    x.Record.Section[2].Section[1].Section[3].Information[0].Value.StringWithMarkup[0].String"
    >>> x']['Record']['Section'][2]['Section'][1]['Section'][3]['Information'][0]['Value']['StringWithMarkup'][0]['String
    
    ***Consider start and end of the Result!!!**
    """
    
    p=onlinePath
    p=p.replace('[','.[')
    p=re.sub(r"\.\["   , "']["   ,p)
    p=re.sub(r"\]\."   , "]['"   ,p)
    p=p.replace('.',"']['")
    return p
