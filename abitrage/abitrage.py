import urllib.request
import json
import time
import datetime
import csv
import pprint
import numpy as np
import yaml
import os

def main():

    with open('config.yml', 'r') as yml:
        config = yaml.load(yml)


    # ログフォルダ・ログファイル設定
    # path = r'C:\Users\softbank\Documents\log.log'
    path = config['log_path']
    file = config['log_file']

    init = False

    diff = 1000

    abtr_json = {} 

    while True:
        markets = {}
        time.sleep(5)

        dt_now = datetime.datetime.now()
        logging = "timestamp", dt_now.strftime('%Y') +"/"+ dt_now.strftime('%m') +"/"+ dt_now.strftime('%d') +" "+ dt_now.strftime('%H') +":"+ dt_now.strftime('%M') +":"+ dt_now.strftime('%S')


        n = 0
        for i in config['markets']:
            if (i == "bitflyer")&(config['markets'][i]):
                markets[n]  = bitflyer()       
                n = n + 1
            elif (i == "bitflyerFX")&(config['markets'][i]):
                    markets[n]  = bitflyerFX()       
                    n = n + 1
            elif (i == "bitbank")&(config['markets'][i]):
                markets[n]  = bitbank()       
                n = n + 1
            elif (i == "coincheck")&(config['markets'][i]):
                markets[n]  = coincheck()       
                n = n + 1
            elif (i == "zaif")&(config['markets'][i]):
                markets[n]  = zaif()
                n = n + 1

        print("===============================================")
        print(dt_now,'\n')

        # print(markets)

        if init == False:
            stackA = [[[99999999 for k in range(1)] for j in markets] for i in markets]
            stackB = [[[99999999 for k in range(1)] for j in markets] for i in markets]


            init = True

        for i in range(markets.__len__()):
            ASK_Corp = markets[i]['Corp']
            ASK_Prise = markets[i]['Data']['ASKS']['Price']

            for j in range(markets.__len__()):
                BID_Corp = markets[j]['Corp']
                BID_Prise = markets[j]['Data']['BIDS']['Price']
                


                stackA[i][j].append(int(BID_Prise)-int(ASK_Prise))
                stackB[i][j].append(int(markets[i]['Data']['BIDS']['Price']) - int(markets[j]['Data']['ASKS']['Price']))


                if (stackA[i][j].__len__() >= 330)|(stackA[i][j][0] == 99999999):
                    stackA[i][j].pop(0)
                    stackB[i][j].pop(0)



                stackAmax = max(stackA[i][j])
                stackAave = np.mean(stackA[i][j])
                stackBmin = max(stackB[i][j])
                stackBave = np.mean(stackB[i][j])


                
                if ASK_Corp != BID_Corp:
                    if int(BID_Prise) - int(ASK_Prise) > diff :
                        print('[アビトラ発動]')
                        print('ASK',ASK_Corp,ASK_Prise)
                        print('BID',BID_Corp,BID_Prise)
                        print('ASK_' + ASK_Corp,'-BID_' + BID_Corp,':', "現在値" ,float(BID_Prise)-float(ASK_Prise), "最大値" ,int(stackAmax), "平均値" ,int(stackAave) )
                        print('ASK_' + BID_Corp,'-BID_' + ASK_Corp,':', "現在値" ,float(markets[i]['Data']['BIDS']['Price']) - float(markets[j]['Data']['ASKS']['Price']), "最大値" ,int(stackBmin), "平均値" ,int(stackBave) )
                        print('\n')

                        logging += 'ASKS_' + ASK_Corp , float(BID_Prise)
                        logging += 'ASKS_' + ASK_Corp + '-BIDS_' + BID_Corp , float(BID_Prise) - float(ASK_Prise) , stackAmax , stackAave
                        logging += 'ASKS_' + BID_Corp + '-BIDS_' + ASK_Corp , float(markets[i]['Data']['BIDS']['Price']) - float(markets[j]['Data']['ASKS']['Price']) , stackBmin , stackBave

        print(logging)

        os.makedirs(path, exist_ok=True)
        with open(path + file, mode='a') as f:
            f.write(str(logging)+ '\n') 




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
            # headers = response.getheaders()
            # status = response.getcode()            
            # print(body)

    except urllib.error.URLError as e:
        print(e.reason)


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
            # headers = response.getheaders()
            # status = response.getcode()            
            # print(body)

    except urllib.error.URLError as e:
        print(e.reason)


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
            # headers = response.getheaders()
            # status = response.getcode()            
            # print(body)

    except urllib.error.URLError as e:
        print(e.reason)


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
            # headers = response.getheaders()
            # status = response.getcode()            
            # print(body)

    except urllib.error.URLError as e:
        print(e.reason)


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


main()


