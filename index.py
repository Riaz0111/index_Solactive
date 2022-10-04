import numpy as np
import pandas as pd
import datetime
import warnings
warnings.filterwarnings("ignore")

prices=pd.read_csv("stock_prices.csv")
check=pd.read_csv("index_level_results_rounded.csv")

#Adding column for datetime format
dates=[]
for date in prices["Date"]:
    dates+=[datetime.datetime.strptime(date, "%d/%m/%Y")]
prices["datetime"]=dates

#Creating function to return names of Top 3 stocks
def get_top3(list):
    t_list=list
    idx=[]
    for i in range(3):
        m=max(t_list)
        i=list.index(m)
        idx+=[i+1]
        list[i]=0
        
    tickers= prices.columns[idx].to_list()
    return tickers


prices["index"]=0
the_three=get_top3(prices.iloc[0,1:-2].to_list())

for i in range(len(prices["Date"])):
    try:
        current_month=prices["datetime"][i].month
        next_month=prices["datetime"][i+1].month
    except:
        pass
    
    #Giving weights 0.5,0.25,0.25
    prices["index"][i]= prices[the_three].iloc[i][0]*0.5 + prices[the_three].iloc[i][1]*0.25 + prices[the_three].iloc[i][2]*0.25
    
    #Updating the Top 3 stocks for next month
    if not(next_month==current_month):
        the_three=get_top3(prices.iloc[i,1:-2].to_list())

prices["Final_Index"]=100
prices["Refrence_Values"]=100

#Adjusting the calculated index values
for i in range(3, len(prices["Date"])):
    prices["Final_Index"].iloc[i]= prices["Final_Index"].iloc[i-1] * (1 + ((prices["index"].iloc[i] / prices["index"].iloc[i-1])-1))

#Adding the given index values as a reference
for i in range(2, len(prices["Date"])):
    prices["Refrence_Values"].iloc[i]=check["index_level"].iloc[i-2]
    
# prices["Final_Index"] = [round(i,2) for i in prices["Final_Index"].to_list()]

#Removing  unnecessary columns
prices.drop(["index","datetime"], axis=1, inplace=True)
prices.head()