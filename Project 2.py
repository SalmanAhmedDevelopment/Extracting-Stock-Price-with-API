import json
import requests 
from bs4 import BeautifulSoup
#Web scraping 
url1 = 'https://www.stockmonitor.com/sp500-stocks/'
page = requests.get(url1)

soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

right_table = soup.find('table', class_='table table-hover top-stocks') 
#print(right_table())

L1 = []
L2 = []
L3 = []
L4 = []
L5 = []
L6 = []
L7 = []
L8 = []


for row in right_table.findAll('tr'):
    cells = row.findAll('td')
    if(len(cells) == 7):
        L1.append(cells[1].text.replace('\n', '').replace('\r', ''))
        L2.append(cells[2].find(text=True).replace('\n', '').replace('\r', ''))
     
      
import pandas as pd
df=pd.DataFrame()
df['SY']               = L1
df['Name']       = L2

print("\n")
print("List of quotes for S&P 500 stocks which make up the S&P 500 index")
print("\n")
print(df)   


print("\n")
print("List of quotes for S&P 50 stocks current Market Summary")
print("\n")

#API and Json

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

counter = 0
for index in range(50):
    Com =(df.loc[index, 'SY'])
    querystring = {"symbol": Com ,"region":"US"}
    
    headers = {
        'x-rapidapi-key': "a14f7e5722msh776e85ffb186429p1f09bbjsnaa77b0983079",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
        
        #print(json.dumps(data, indent = 4))
    L3.append(data["symbol"])
    L4.append(data["financialData"]['currentPrice']['raw'])#current
    L5.append(data["summaryDetail"]['regularMarketOpen']['raw']) #open
    L6.append(data["summaryDetail"]['previousClose']['raw']) #oldclose 
    L7.append(data["summaryDetail"]['marketCap']['fmt']) #cap
    L8.append(data["summaryDetail"]['regularMarketVolume']['fmt']) #Volume
    #print(L3)
   
            

Stockdata = { 
        'SY' : L3, 
        'Current' : L4, 
        'Open': L5,
        'Previous Close':L6,
        'Market Cap' : L7,
        'Volume': L8}
        
import pandas as pd2    
df2 = pd2.DataFrame(Stockdata)


df3 = pd.merge(df, df2, how='right', on=['SY'])


print(df2)
print("\n")
print("Combined dataframes")
print("\n")
print(df3)
print("\n")
print("Description statistics for the combined data frame")
print("\n")
print(df3.describe())      
     
df3.to_csv('Project2.csv')

