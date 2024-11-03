# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:46:16 2024

@author: JAYDEV
"""

import pandas as pd
import numpy as np
import selenium
from bs4 import BeautifulSoup
import requests
import json
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
from datetime import timedelta, date

today = date.today()
weekago = today - timedelta(days=7)
oneMonth = today - timedelta(days = 30)
threeMonth = today - timedelta(days = 90)

tday = today.strftime('%d-%m-%Y')
wday = weekago.strftime('%d-%m-%Y')
omonth = oneMonth.strftime('%d-%m-%Y')
tmonth = threeMonth.strftime('%d-%m-%Y')

def fetchData(urls):

    headers = {
    'accept': '*/*',
    'accept-encoding' : 'gzip, deflate, br, zstd',
    'accept-language' : 'en-US,en;q=0.9,gu-IN;q=0.8,gu;q=0.7',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'cookie' : '_ga=GA1.1.1180596736.1720400349; _abck=B51836B14214C2CE308A955D2D9C6BB4~0~YAAQ5xghF86B5cuSAQAA+DIt0Azgybs8bBdga/+anC86RCvC8wyNegWsNM9Dt9b6kPuhcbl19H9B0XYoOzUKPjdbaTYkk7zYxuf4F6BOHy5BZ/IvfGVcfT7+qsZpyVTt47z7IePmpurSOu1Z9AaYvOXKe1rKBe4/ZRBNOMRGiiYNSvRwyvobKgrHwMSBC6VL6iNzEJFPWXHmVn9uarkAC416cMDdZFoUpe+xJjO3xwnpfDmhCWSXmfEyd51aqp+hjNDPCQBTihClla3b9tR50+YDKavAjIi6cCZiOO3XtXkTsUZbpbnS+fx95fuRhfNs1Y8PdxvSC4z1BRZ1O+mtamS9g+mXleTo/iSRDSHLG/oIGAigso8qmtRV8qO0D6iCbWYBFIYm8B82hSGHnGgdWPOtoWScu6eHeF0=~-1~-1~-1; nsit=A2kXzzutuJAk1Nv1LtpH5zl0; AKA_A2=A; bm_mi=3D218D06EF8B215B4943BDE954D72E00~YAAQ5xghF72x5cuSAQAAiH4t0BlSlGoDpa0kT6ylAnMteFGBOEKj8zK1LHvV3GFZA8pJ0CT2RlsIBTygK/YkjRrw60OjFCHbg96XIMyYPRjIZMtwXwSLaLvBdLd5ZoYao4SVFDwCRq896U4rPWH1b5gbWjD8yKOLeuN7IrRSc/b+fL6DfXb2zFx4YeIn60f6awJ7cgMkOdFohSYkvUIgF+9l0Ra9446G3kul+JYXQnaTM/fxcbo12j3iB/UM7y6hHkDOCJZkTZm3UgyVF+m2AOQriCE7AP+Fpr7NxnfisgFdWzucVE2hP2ja/p2LmUxE~1; bm_sz=B24E68426C46010E28D2363167177019~YAAQ5xghF7+x5cuSAQAAiH4t0Bk/eSOk2s7NsHmEkvvfi008lIV4pAnmW5HKvXBtgQSR2k+MTj5GRFkqnXur7RQBxzHlE9Yqt4BT5Z6h6q/QtbHZ0Eiz3SYNzbperCq/XOGT34DqWehmphMt06JfC2BGT9szz8iF+47s7s9m7WT2YbMwZekOFlocWwBYaK1wzmdNvKG15Eowplrtr3kP4XnRXGJEpL3rmo8e1uB8zMu6NbMchG4+rlUOOsmeluK1iI22HvTGtm8iwmo9n4i/f+a7aF5eCfIQv4mxjsdddbBT8PmBBHBeL7vH/0KxgqqvH8rgqVo2Kv/NSX03XaSCpmLGy7nFbL+m54n1vEQzw/MO3V90y2OEA6Xs5zIvrQWBwxgxS8F56VOMK4VXy8TOmaz38e44lUetol0=~4599864~3290162; defaultLang=en; _ga_87M7PJ3R97=GS1.1.1730069340.24.1.1730069340.60.0.0; _ga_WM2NSQKJEK=GS1.1.1730069340.1.0.1730069340.0.0.0; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTczMDA2OTQ5NiwiZXhwIjoxNzMwMDc2Njk2fQ.y2BF8NZh57U6zN5zedOHJJP9Dggq_lKDh8fHI55ofXQ; ak_bmsc=2D3F4C80B3EF70A9E746BB06D8F0CCAA~000000000000000000000000000000~YAAQ6hghF98A7suSAQAAvIYt0Bn52vqgUWfEArbsPgNQCFCrnlMRGWPSPtsiL6INme2yt42vnacmyMh00s09d3WZE/ct9e+6gHXITI8giDLGkx3M0KnxUhbrDZOJbMIp5hJe/yje/Km3RqCg0rUX3FhHB8Hc8R6EcTHca/cRxrukebmf+9R9akrjB8m+O7Wsm1ZE+dT9UDwoAMl/9s+AscCFh7Po3vC+CvHiaEXd3YWqALZfZxRRkz6wJACdp6gXX8nGdZBPXh7sNvkLEnbWxAff4D/Ntc1vdfRFnHRDdpSpdjO9EdOjkdO9IbQxuZvFRVuoaU3hRoE3i+tgdi+76xxp6UYH8r40HQay7c7kTLpLLXLNcrYRJCc2gwTwRSRLVQUGFaczPyVgQF3lNQEENjCeBu6LwsgEKEFfSOmszxvwo3hrerKBno8pHGwPGTTuZEIpXd8Nr9N3EODCxE47aCe0p2wOYLNOSxd6jNvRNxnNRd/SaNw8fw==; bm_sv=485DFEC34F285358E900532A4B9502F2~YAAQ5xghF5S/5cuSAQAA2JMt0BniiSInbrAU9AN/o7trlbpmz8/wxOeNHxbQoV72wLjbjJGnWUwgZjI8ysbgiBjvXbHRPHahbKxBojPtLoz2szIlTgoaP6iZJiDxdYNHp7K1jR1BLjR2iEFkE1cyYwszdH/z3s9pjbrYwg3bK8AOfYTMlA1kKQNB6V4haT+6OZ3eBCESQAPSWecFdGwRrj1lbvAUVDRpSbsq96G0cEEihiNVDlZe7TttYRG3jfvhH0w=~1; RT="z=1&dm=nseindia.com&si=3ae02fdf-7efe-44d4-b8cf-f31186156266&ss=m2s6m4q5&sl=1&se=8c&tt=4jp&bcn=%2F%2F173bf10e.akstat.io%2F&ld=5bq&ul=8cw"'
    }
    try:
        requests.get('https://www.nseindia.com/',  headers = headers)
        response = requests.get(url = urls, headers = headers)
    except:
        pass
    content = json.loads(response.text)
    dataDF = pd.DataFrame([content])
    rdic = response.json()
    return rdic

def relativeStrength(mainDF):
    averageGain = []
    averageLoss = []
    for index, row in mainDF.iterrows():
        diff = row['EOD_CLOSE_INDEX_VAL'] - row ['EOD_OPEN_INDEX_VAL']
        if diff > 0:
            averageGain.append(diff)
            averageLoss.append(0)
        elif diff < 0 :
            averageLoss.append(diff)
            averageGain.append(0)
    return np.average(averageGain)/abs(np.average(averageLoss))

allIndices = r"https://www.nseindia.com/api/allIndices"
indicesDF = fetchData(allIndices)
indicesDFactual = pd.DataFrame(indicesDF['data'])
indicesList = list(indicesDFactual['index'])

with open("IndexList.json", "w") as outfile: 
    json.dump(indicesDF, outfile)

specificIndexData = {}
for i in indicesList:
    indexName = i.replace(' ','%20')
    indexfetch = 'https://www.nseindia.com/api/historical/indicesHistory?indexType='+indexName+'&from='+ tmonth +'&to=' + tday
    specificIndexData[i] = fetchData(indexfetch)
    print(i + ' Complete!')
    
with open("Index.json", "w") as outfile: 
    json.dump(specificIndexData, outfile)
    
indicesDict = {}
for i in indicesList:
    print(i)
    try:
        fetchLink = r'https://www.nseindia.com/api/equity-stockIndices?index='
        indicesDict[i] = fetchData(fetchLink + i.replace(' ','%20'))
        print('Complete')
    except:
        print("Not Complete")
        pass
    
with open("Sector.json", 'w') as outfile:
    json.dump(indicesDict, outfile)
    
sectorwiseStocks = {}
for i in list(indicesDict.keys()):
    try:
        sectorwiseStocks[i] = list(pd.DataFrame(indicesDict[i]['data'])['symbol'])
    except:
        pass
    
with open("SectorList.json", 'w') as outfile:
    json.dump(sectorwiseStocks, outfile)
    
nseStocks = pd.read_csv(r'C:\Users\JAYDEV\Documents\Python Scripts\dataSaving\EQUITY_NSE.csv')
nseStocks = nseStocks[nseStocks[' SERIES'] == 'EQ']
nseStocksList = list(nseStocks['SYMBOL'])

specificStockData = {}
for i in nseStocksList[1328:]:
    stockfetch = 'https://www.nseindia.com/api/historical/cm/equity?symbol='+ i +'&series=[%22EQ%22]&from='+ tmonth +'&to=' + tday
    print(stockfetch)
    specificStockData[i] = fetchData(stockfetch)
    print(i + ' Complete!')
    
with open("Stock.json", "w") as outfile: 
    json.dump(specificStockData, outfile)



relativeStrengthDict = {}
for i in indicesList:
    try:
        selectDict = specificIndexData[i]['data']['indexCloseOnlineRecords']
        selectDF = pd.DataFrame(selectDict)
        relativeStrengthDict[i] =  relativeStrength(selectDF)
        print(i + ' Complete!')
    except:
        pass

sortedRelativeStrenth = sorted(relativeStrengthDict.items(), key=lambda x:x[1], reverse=True)
sortedindexDF = pd.DataFrame(sortedRelativeStrenth, columns = ['Name', 'Relative Strength'])
sortedindexDF = sortedindexDF[sortedindexDF['Relative Strength'].notna()]
sortedindexDF.to_csv('indexRelativeStrength.csv', header = True, index = None)


nseStocks = pd.read_csv(r'C:\Users\JAYDEV\Documents\Python Scripts\dataSaving\EQUITY_NSE.csv')
nseStocks = nseStocks[nseStocks[' SERIES'] == 'EQ']
nseStocksList = list(nseStocks['SYMBOL'])



