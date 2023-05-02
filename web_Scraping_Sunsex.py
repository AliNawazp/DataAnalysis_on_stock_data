import pandas as pd
import numpy as np
def handling_nan_values(df):
    df.fillna({'Open':df['Open'].median(),'Low':df['Low'].median(),'High':df['High'].median(),'Close*':df['Close*'].median(),\
              'Volume':df['Volume'].median(),'Adj Close**':df['Adj Close**'].median()},inplace=True)
    return df

def preprocessing_Sunsex(df):
    df.replace(('-',"0"),inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%b %d, %Y")
    df["Open"] = df["Open"].map(lambda x: x.replace(',', '')).astype("float")
    df["High"] = df["High"].map(lambda x: x.replace(',', '')).astype("float")
    df["Low"] = df["Low"].map(lambda x: x.replace(',', '')).astype("float")
    df["Close*"] = df["Close*"].map(lambda x: x.replace(',', '')).astype("float")
    df["Volume"] = df["Volume"].map(lambda x: x.replace(',', '')).astype("float")
    df["Adj Close**"] = df["Adj Close**"].map(lambda x: x.replace(',', '')).astype("float")
    df.replace((0.0, np.nan), inplace=True)
    df = handling_nan_values(df)
    return df

def Sunsex():
    path="C:\Program Files (x86)\chromedriver.exe" # path where this chrome driver is located
    driver=webdriver.Chrome(path)
    driver.get("https://finance.yahoo.com/quote/%5EBSESN/history/")
    htmlcontent=driver.page_source #htmlpage
    soup=BeautifulSoup(htmlcontent,"html.parser")
    table = soup.find('table',class_="W(100%) M(0)")
    list_of_columns = []
    for i in table.find_all("th"):
        list_of_columns.append(i.text.strip())
    list_of_data = []
    for i in (table.find("tbody").find_all("tr")):
        L=[]
        for j in i.find_all("td"):
            L.append(j.text.strip())
        list_of_data.append(L)
    hour = datetime.now().time().strftime('%H')
    if int(hour) >= 23:
        pass
    else:
        list_of_data = list_of_data[1:]
    df = pd.DataFrame(data=list_of_data, columns=list_of_columns)
    df.to_csv("Sunsex.csv",index=None)

if __name__ == "__main__":
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from datetime import datetime
    #Sunsex()
    df=pd.read_csv("Sunsex.csv")
    preprocessing_Sunsex(df)

