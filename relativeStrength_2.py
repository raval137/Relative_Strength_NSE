# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 21:27:56 2024

@author: JAYDEV
"""

import json
import numpy as np
import pandas as pd
import csv

def relativeStrength(mainDF):
    averageGain = []
    averageLoss = []
    n = len(mainDF)
    i = 0
    for index, row in mainDF.iterrows():
        diff = row['EOD_CLOSE_INDEX_VAL'] - row ['EOD_OPEN_INDEX_VAL']
        if diff > 0:
            averageGain.append(((n-i)/n)*diff)
            averageLoss.append(0)
            i = i + 1
        elif diff < 0 :
            averageLoss.append(((n-i)/n)*diff)
            averageGain.append(0)
            i = i + 1
    return np.average(averageGain)/abs(np.average(averageLoss))

def relativeStrengthStock(mainDF):
    averageGain = []
    averageLoss = []
    n = len(mainDF)
    i = 0
    for index, row in mainDF.iterrows():
        diff = row['CH_CLOSING_PRICE'] - row ['CH_OPENING_PRICE']
        if diff > 0:
            averageGain.append(((n-i)/n)*diff)
            averageLoss.append(0)
            i = i + 1
        elif diff < 0 :
            averageLoss.append(((n-i)/n)*diff)
            averageGain.append(0)
            i = i + 1
    return np.average(averageGain)/abs(np.average(averageLoss))



def readJson(i):
    with open(i, 'r') as file:
        data = json.load(file)
    
    return data

specificIndexData = readJson('Index.json')
index = readJson("IndexList.json")
indicesDict = readJson('Sector.json')
sectorwiseStocks = readJson('SectorList.json')
specificStockData = readJson('Stock.json')

indicesList = list(pd.DataFrame(index['data'])['index'])
nseStocks = pd.read_csv(r'C:\Users\JAYDEV\Documents\Python Scripts\dataSaving\EQUITY_NSE.csv')
nseStocks = nseStocks[nseStocks[' SERIES'] == 'EQ']
nseStocksList = list(nseStocks['SYMBOL'])

indexRS = {}
relativeStrengthDict = {}
for i in indicesList:
    try:
        selectDict = specificIndexData[i]['data']['indexCloseOnlineRecords']
        selectDF = pd.DataFrame(selectDict)
        relativeStrengthDict[i] =  relativeStrength(selectDF)
        indexRS[i] = relativeStrength(selectDF)
        print(i + ' Complete!')
    except:
        pass
    
sortedRelativeStrenth = sorted(indexRS.items(), key=lambda x:x[1], reverse=True)
indexrsDF = pd.DataFrame(sortedRelativeStrenth, columns = ['Name', 'Relative Strength'])
indexrsDF = indexrsDF[indexrsDF['Relative Strength'].notna()]
indexrsDF = indexrsDF.set_index('Name')
    
    
for i in nseStocksList:
    try:
        selectDict = specificStockData[i]['data']
        selectDF = pd.DataFrame(selectDict)
        relativeStrengthDict[i] =  relativeStrengthStock(selectDF)
        print(i + ' Complete!')
    except:
        pass
    

sortedRelativeStrenth = sorted(relativeStrengthDict.items(), key=lambda x:x[1], reverse=True)
rsDF = pd.DataFrame(sortedRelativeStrenth, columns = ['Name', 'Relative Strength'])
rsDF = rsDF[rsDF['Relative Strength'].notna()]
rsDF = rsDF.set_index('Name')

result = {}
for i in sectorwiseStocks['NIFTY 50']:
    try:
        result[i] = rsDF.loc[i][0]
    except:
        pass
    


    
for j in indicesList:
    result = {}
    try:
        for i in sectorwiseStocks[j]:
            try:
                result[i] = rsDF.loc[i][0]
            except:
                pass
        sortedRelativeStrenth = sorted(result.items(), key=lambda x:x[1], reverse=True)
        resultDF = pd.DataFrame(sortedRelativeStrenth, columns = ['Name', 'Relative Strength'])
        finalList = []
        for n in list(resultDF['Name']):
            if n != j:
                 n = n.replace('-','_')
                 n = n.replace('&','_')
                 finalList.append(n)
            else:
                break
        with open('Result/RS_' + j + '.csv', 'w+',  newline = '') as f:
            write = csv.writer(f)
            write.writerow(finalList)
        # resultDF.to_csv(r'Result/' + j +'.csv', index = False)
        
    except:
        pass








    
    


    

    


