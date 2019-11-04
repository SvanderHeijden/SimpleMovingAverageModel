import urllib.parse
import json

"""

This application serves as a simple plotting tool for the US stock market. For closing 
data the financial moddeling pred API is used. 

@author: Sjoerd van der Heijden

"""

import requests
import numpy as np
import pandas as pd
from tqdm import tqdm

"""

When this definition is called the API is requested.

@return: myData is a dictionary containing the close and dates of the requested ticker.

"""
def request(ticker):
    
    myUrl  = 'https://financialmodelingprep.com/api/v3/historical-price-full/'
    
    totalUrl = urllib.parse.urljoin(myUrl, ticker)
    
    request = requests.get(totalUrl)
    
    myData = json.loads(request.text.replace("<pre>","").replace("</pre>",""))
    
    return(myData)
    
"""

When this definition is called it computes the simple moving average for the
last 50 and 200 days. Then, the score is computed by deviding the 50 days SMA
by the 200 days SMA. 

@param: ticker is the Ticker for any given stock.

@return: myScore is the score for any given stock.

"""
def score(ticker):

    
    try:
        
        myData = request(ticker)
        
        myPrice = []
        
        for i in range(0, len(myData["historical"])):
        
            myPrice.append(float(myData["historical"][i]["close"]))
        
        moving = [50, 200]
        
        totalSMA = []
        
        for h in range(0, len(moving)):
            
            mySMA = []
            
            for i in range(moving[h]-1, len(myData["historical"])):
            
                mySum = 0
            
                for j in range(0, moving[h]-1):
                
                    mySum += float(myData["historical"][i-j]["close"])
                
                mySMA.append(mySum/(moving[h]-1))    
            
        
            totalSMA.append(mySMA[len(mySMA)-1])
            
        myScore = totalSMA[0]/totalSMA[1]
    
    except:
        
        myScore = 0
    
    return(myScore)

"""

When this definition is called the summarizes the results of the program in
a dataframe. The data frame is sorted by decending order and written to
an excel file.

@param: listTickers is a list of Tickers.

"""

def result(listTickers):
    
    myScore = []
    
    myList = []
    
    for i in tqdm(range(len(listTickers))):
        
        listTickers[i] = str(listTickers[i]).strip()
        
        myScore.append(score(listTickers[i]))
        
        myList.append(listTickers[i])
        
        myResult = np.array(np.transpose(np.array([myList, myScore])))
       
    df = pd.DataFrame(myResult,  columns=['Ticker', 'Score']).sort_values(by=['Score'], ascending=False).head(50)
    
    df.to_excel(excel_writer = "/Users/SjoerdvanderHeijden/Documents/API/fcf_model/code/V1.0/result.xlsx")
    

if __name__ == '__main__':
    
    listTickers = open("ticker.csv").readlines()
    
    result(listTickers)