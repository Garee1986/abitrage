import urllib.request
import json


def bitbank():

    url = 'https://public.bitbank.cc/btc_jpy/depth'


    try:
        with urllib.request.urlopen(url) as response:
            body = json.loads(response.read())
            # headers = response.getheaders()
            # status = response.getcode()            
            # print(body)

    except urllib.error.URLError as e:
        print(e.reason)
        body = ""


    if body != "":
        dict = { "Corp":"bitbank",
                 "Symbol":"BTCJPY",
                 "Data":{
                     "ASKS":
                        {"Price":body['data']['asks'][0][0],
                         "Size":body['data']['asks'][0][1]},
                     "BIDS":
                        {"Price":body['data']['bids'][0][0],
                         "Size":body['data']['bids'][0][1]}
                        }
                }

    return dict



def bitflyer():

    url = 'https://api.bitflyer.com/v1/board'


    try:
        with urllib.request.urlopen(url) as response:
            body = json.loads(response.read())

    except urllib.error.URLError as e:
        print(e.reason)
        body = ""


    if body != "":
        dict = { "Corp":"bitflyer",
                 "Symbol":"BTCJPY",
                 "Data":{
                     "ASKS":
                        {"Price":body['asks'][0]['price'],
                         "Size":body['asks'][0]['size']},
                     "BIDS":
                        {"Price":body['bids'][0]['price'],
                         "Size":body['bids'][0]['size']}
                     }
                 }

    return dict



def bitflyerFX():

    url = 'https://api.bitflyer.com/v1/board?product_code=FX_BTC_JPY'


    try:
        with urllib.request.urlopen(url) as response:
            body = json.loads(response.read())

    except urllib.error.URLError as e:
        print(e.reason)
        body = ""


    if body != "":
        dict = { "Corp":"bitflyerFX",
                 "Symbol":"BTCJPY",
                 "Data":{
                     "ASKS":
                        {"Price":body['asks'][0]['price'],
                         "Size":body['asks'][0]['size']},
                     "BIDS":
                        {"Price":body['bids'][0]['price'],
                         "Size":body['bids'][0]['size']}
                     }
                }

    return dict



def coincheck():

    url = 'https://coincheck.com/api/order_books'


    try:
        with urllib.request.urlopen(url) as response:
            body = json.loads(response.read())

    except urllib.error.URLError as e:
        print(e.reason)
        body = ""


    if body != "":
        dict = { "Corp":"coincheck",
                 "Symbol":"BTCJPY",
                 "Data":{
                     "ASKS":
                        {"Price":body['asks'][0][0],
                         "Size":body['asks'][0][1]},
                  "BIDS":
                        {"Price":body['bids'][0][0],
                         "Size":body['bids'][0][1]}
                     }
                 }

    return dict



def zaif():

    url = 'https://api.zaif.jp/api/1/depth/btc_jpy'


    try:
        with urllib.request.urlopen(url) as response:
            body = json.loads(response.read())

    except urllib.error.URLError as e:
        print(e.reason)
        body = ""


    if body != "":
        dict = { "Corp":"zaif",
                 "Symbol":"BTCJPY",
                 "Data":{
                     "ASKS":
                        {"Price":body['asks'][0][0],
                         "Size":body['asks'][0][1]},
                     "BIDS":
                        {"Price":body['bids'][0][0],
                         "Size":body['bids'][0][1]}
                     }
                 }  

    return dict



