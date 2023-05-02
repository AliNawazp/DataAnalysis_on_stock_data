
import pandas as pd

def func(x):
    if x == '-':
        return '0'
    else:
        return x


def preprocessing_Sunsex(df):
    df = df.applymap(func)
    df["MARKET PRICE(Rs)"] = df["MARKET PRICE(Rs)"].map(lambda x: x.replace(',', '')).astype("float")
    try:
        df["CHANGE(%)"] = df["CHANGE(%)"].astype("float")
    except:
        df["CHANGE(%)"] = df["CHANGE(%)"].map(lambda x: x.rstrip('%')).astype("float")
    df["NO OFSHARES(m)"] = df["NO OFSHARES(m)"].map(lambda x: x.replace(',', '')).astype("float")
    df["MARKET CAP.**(Rs m)"] = df["MARKET CAP.**(Rs m)"].map(lambda x: x.replace(',', '')).astype("float")
    df["FREE FLOAT ADJ. FACTOR"] = df["FREE FLOAT ADJ. FACTOR"].astype("float")
    df["WEIGHTAGE(%)"] = df["WEIGHTAGE(%)"].astype("float")
    df["EARNINGS *(Rs m)"] = df["EARNINGS *(Rs m)"].map(lambda x: x.replace(',', '')).astype("float")
    df["EPS(Rs)"] = df["EPS(Rs)"].astype("float")
    df["PER(X)"] = df["PER(X)"].astype("float")
    return df


def Sunsex_companies():
    path = "C:\Program Files (x86)\chromedriver.exe"  # path where this chrome driver is located
    driver = webdriver.Chrome(path)
    driver.get("https://www.equitymaster.com/india-markets/bse-replica.asp")
    htmlcontent = driver.page_source  # htmlpage
    soup = BeautifulSoup(htmlcontent, "html.parser")
    table = soup.find('table', class_="mystocksbig mystocks newtab cls")
    list_of_columns = []
    for i in table.find_all("th"):
        list_of_columns.append(i.text.strip())
    list_of_columns = list_of_columns[3:]
    list_of_data = []
    for i in (table.find("tbody").find_all("tr")):
        L = []
        for j in i.find_all("td"):
            L.append(j.text.strip())
        list_of_data.append(L)
    df = pd.DataFrame(data=list_of_data, columns=list_of_columns)
    df.to_csv("Sunsex_companies.csv", index=None)


if __name__ == "__main__":
    from bs4 import BeautifulSoup
    from selenium import webdriver
    Sunsex_companies()



