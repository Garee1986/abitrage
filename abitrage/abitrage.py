import time
import datetime
import csv
import pprint
import numpy as np
import yaml
import os

import ApiFunction


def main():

    with open('config.yml', 'r') as yml:
        config = yaml.load(yml)


    # ログフォルダ・ログファイル設定
    path = config['log_path']
    file = config['log_file']

    init = False

    ApiFunction.coincheckMountCheck(config['API']['coincheck'])


    while True:
        markets = {}
        time.sleep(5)

        dt_now = datetime.datetime.now()
        logging = "timestamp", dt_now.strftime('%Y') +"/"+ dt_now.strftime('%m') +"/"+ dt_now.strftime('%d') +" "+ dt_now.strftime('%H') +":"+ dt_now.strftime('%M') +":"+ dt_now.strftime('%S')


        n = 0
        for i in config['markets']:
            if (i == "bitflyer")&(config['markets'][i]):
                markets[n]  = ApiFunction.bitflyerRateCheck()       
                n = n + 1
            elif (i == "bitflyerFX")&(config['markets'][i]):
                    markets[n]  = ApiFunction.bitflyerFXRateCheck()       
                    n = n + 1
            elif (i == "bitbank")&(config['markets'][i]):
                markets[n]  = ApiFunction.bitbankRateCheck()       
                n = n + 1
            elif (i == "coincheck")&(config['markets'][i]):
                markets[n]  = ApiFunction.coincheckRateCheck()       
                n = n + 1
            elif (i == "zaif")&(config['markets'][i]):
                markets[n]  = ApiFunction.zaifRateCheck()
                n = n + 1

        print("===============================================")
        print(dt_now)

        if init == False:
            stackA = [[[99999999 for k in range(1)] for j in markets] for i in markets]
            stackB = [[[99999999 for k in range(1)] for j in markets] for i in markets]


            init = True

        for i in range(markets.__len__()):
            ASK_Corp = markets[i]['Corp']
            ASK_Prise = int(float(markets[i]['Data']['ASKS']['Price']))

            for j in range(markets.__len__()):
                BID_Corp = markets[j]['Corp']
                BID_Prise = int(float(markets[j]['Data']['BIDS']['Price']))
                


                stackA[i][j].append(int(float(BID_Prise)-float(ASK_Prise)))
                stackB[i][j].append(int(float(markets[i]['Data']['BIDS']['Price']) - float(markets[j]['Data']['ASKS']['Price'])))


                if (stackA[i][j].__len__() >= 330)|(stackA[i][j][0] == 99999999):
                    stackA[i][j].pop(0)
                    stackB[i][j].pop(0)



                stackAmax = max(stackA[i][j])
                stackAave = np.mean(stackA[i][j])
                stackBmin = max(stackB[i][j])
                stackBave = np.mean(stackB[i][j])


                
                if ASK_Corp != BID_Corp:
                    if float(BID_Prise) - float(ASK_Prise) > config['diff'] :
                        print('===============================================')
                        print('ASK',ASK_Corp,ASK_Prise)
                        print('BID',BID_Corp,BID_Prise)
                        print('ASK_' + ASK_Corp,'-BID_' + BID_Corp,':', "現在値" ,int(float(BID_Prise)-float(ASK_Prise)), "最大値" ,int(stackAmax), "平均値" ,int(stackAave) )
                        print('ASK_' + BID_Corp,'-BID_' + ASK_Corp,':', "現在値" ,int(float(markets[i]['Data']['BIDS']['Price']) - float(markets[j]['Data']['ASKS']['Price'])), "最大値" ,int(stackBmin), "平均値" ,int(stackBave) )

                        logging += 'ASKS_' + ASK_Corp , float(BID_Prise)
                        logging += 'ASKS_' + ASK_Corp + '-BIDS_' + BID_Corp , int(float(BID_Prise) - float(ASK_Prise)) , stackAmax , stackAave
                        logging += 'ASKS_' + BID_Corp + '-BIDS_' + ASK_Corp , int(float(markets[i]['Data']['BIDS']['Price']) - float(markets[j]['Data']['ASKS']['Price'])) , stackBmin , stackBave

        print("\n",logging,"\n")

        os.makedirs(path, exist_ok=True)
        with open(path + file, mode='a') as f:
            f.write(str(logging)+ '\n') 




main()


