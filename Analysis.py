import numpy as np
import pandas as pd
import plotly as plt
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
import web_Scraping_Nifty
import web_Scraping_Sunsex
import web_Scraping_Nifty_companies
import web_Scraping_Sunsex_companies
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


st.set_page_config(layout="wide") #defaultly it set the web page in wide mode


def data_fetching():
    df_nifty = pd.read_csv("Nifty.csv")
    df_nifty = web_Scraping_Nifty.preprocessing_Nifty(df_nifty)
    df_sunsex = pd.read_csv("Sunsex.csv")
    df_sunsex = web_Scraping_Sunsex.preprocessing_Sunsex(df_sunsex)
    df_nifty_companies = pd.read_csv("Nifty_companies.csv")
    df_nifty_companies = web_Scraping_Nifty_companies.preprocessing_Nifty(df_nifty_companies)
    df_sunsex_companies = pd.read_csv("Sunsex_companies.csv")
    df_sunsex_companies = web_Scraping_Sunsex_companies.preprocessing_Sunsex(df_sunsex_companies)
    return df_nifty,df_sunsex,df_nifty_companies,df_sunsex_companies

def Analysis_on_Nifty():
    global df_nifty,df_nifty_companies
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='text-align: left; color: black;'>'Descriptive Statistic on Nifty --------------------------------------->'</h4>", unsafe_allow_html=True)
        with col2:
            descriptive_nifty = df_nifty[["Open","Close*","Low","High","Volume","Adj Close**"]].describe()
            st.write(descriptive_nifty)
    st.markdown("---")
    with st.container():
        st.subheader("Univariate Analysis")
        option = st.selectbox(
            "Choose",
            ("Open","Close*","Low","High","Volume","Adj Close**"))
        col1,col2,col3 = st.columns(3)
        with col1:
            st.write("PDF of {}".format(option))
            fig,ax = plt.subplots()
            sns.distplot(df_nifty[option])
            st.pyplot(fig)
        with col2:
            st.write("CDF of {}".format(option))
            fig,ax = plt.subplots()
            sns.ecdfplot(df_nifty[option])
            st.pyplot(fig)
        with col3:
            st.write("Box plot of {}".format(option))
            fig, ax = plt.subplots()
            sns.boxplot(df_nifty[option])
            st.pyplot(fig)

        st.subheader("Conclusions from above")
        ma=df_nifty[option].max()
        mi=df_nifty[option].min()
        avg=df_nifty[option].mean()
        p_25=np.percentile(df_nifty[option],25)
        p_75=np.percentile(df_nifty[option],75)
        st.write("The Maximum {} is  {} at this Date {}".format(option,ma,df_nifty[df_nifty[option]==ma]["Date"]))
        st.write("The minimum {} is {} at this Date {}".format(option,mi,df_nifty[df_nifty[option]==mi]["Date"]))
        st.write("The avg {} is {}".format(option,avg))
        st.write("most of the time {} lie between {} and {}".format(option,p_25,p_75))
    st.markdown("---")

    with st.container():
        st.subheader("Bivariate Analysis")
        col1,col2 = st.columns(2)
        with col1:
            option = st.selectbox(
                "choose",
                ("Open", "Close*", "Low", "High", "Volume", "Adj Close**"))
        with col2:
            option1 = st.selectbox(
                "choose other",
                ( "Close*","Open","Low", "High", "Volume", "Adj Close**"))
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Scatter plot between {} and {}".format(option,option1))
            fig, ax = plt.subplots()
            sns.scatterplot(data=df_nifty, x=option, y=option1)
            st.pyplot(fig)
        with col2:
            st.write("Line plot between {} and {}".format(option,option1))
            fig, ax = plt.subplots()
            sns.lineplot(x =option, y =option1, data = df_nifty)
            st.pyplot(fig)
        with col3:
            st.write("Regression plot between {} and {}".format(option,option1))
            fig, ax = plt.subplots()
            sns.regplot(x=option, y=option1, data=df_nifty)
            st.pyplot(fig)

        st.subheader("Conclusions from above")
        st.write("Just visualize how features are behaving with each other")
    st.markdown("---")

    st.markdown("<h2 style='text-align: center; color: black;'>'Technical analysis on Nifty'</h2>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,1,3])
        with col1:
            option = st.selectbox(
                'Slect on what basis you need to analyse',
                ('Daily', 'Weekly', 'Monthly'))
        with col2:
            option1 = st.selectbox(
                'Slect one',
                ('Volume','Open', 'Close', 'Low', 'High'))
        with col3:
            if option == 'Weekly':
                df_nifty.set_index(["Date"],inplace=True)
                df_weekly = df_nifty.resample('W').mean()
                if option1 == "Open":
                    st.bar_chart(df_weekly["Open"])
                if option1 == "Close":
                    st.bar_chart(df_weekly["Close*"])
                if option1 == "Low":
                    st.bar_chart(df_weekly["Low"])
                if option1 == "High":
                    st.bar_chart(df_weekly["High"])
                if option1 == "Volume":
                    st.bar_chart(df_weekly["Volume"])
                df_nifty.reset_index(inplace=True)
            if option == 'Monthly':
                df_nifty.set_index(["Date"], inplace=True)
                df_Monthly = df_nifty.resample('M').mean()
                if option1 == "Open":
                    st.bar_chart(df_Monthly["Open"])
                if option1 == "Close":
                    st.bar_chart(df_Monthly["Close*"])
                if option1 == "Low":
                    st.bar_chart(df_Monthly["Low"])
                if option1 == "High":
                    st.bar_chart(df_Monthly["High"])
                if option1 == "Volume":
                    st.bar_chart(df_Monthly["Volume"])
                df_nifty.reset_index(inplace=True)
            if option == 'Daily':
                df_nifty.set_index(["Date"], inplace=True)
                df_Daily = df_nifty.resample('D').mean()
                if option1 == "Open":
                    st.bar_chart(df_Daily["Open"])
                if option1 == "Close":
                    st.bar_chart(df_Daily["Close*"])
                if option1 == "Low":
                    st.bar_chart(df_Daily["Low"])
                if option1 == "High":
                    st.bar_chart(df_Daily["High"])
                if option1 == "Volume":
                    st.bar_chart(df_Daily["Volume"])
                df_nifty.reset_index(inplace=True)
    st.subheader("Conclusions")
    st.write("Just change the frequency like daily or monthly or weekly and see how stock price is changing ")
    st.markdown("---")

    with st.container():
        col1,col2,col3 = st.columns([1,1,3])
        with col1:
            candle_plot = st.radio("select yes or not to see the Candle stick plot", ("yes", "no"))
        if candle_plot == "yes":
            with col2:
                option = st.selectbox(
                    'Slect',
                    ('Daily', 'Monthly','Weekly'))
            with col3:
                if option == 'Weekly':
                    df_nifty.set_index(["Date"], inplace=True)
                    df_weekly = df_nifty.resample('W').mean()
                    fig = go.Figure(data=[go.Candlestick(x=df_weekly.index,
                                        open=df_weekly['Open'], high=df_weekly['High'],
                                        low=df_weekly['Low'], close=df_weekly['Close*'])])
                    fig.update_layout(xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                    df_nifty.reset_index(inplace=True)
                if option == 'Monthly':
                    df_nifty.set_index(["Date"], inplace=True)
                    df_monthly = df_nifty.resample('M').mean()
                    fig = go.Figure(data=[go.Candlestick(x=df_monthly.index,
                                                         open=df_monthly['Open'], high=df_monthly['High'],
                                                         low=df_monthly['Low'], close=df_monthly['Close*'])])
                    fig.update_layout(xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                    df_nifty.reset_index(inplace=True)
                if option == 'Daily':
                    df_nifty.set_index(["Date"], inplace=True)
                    df_daily = df_nifty.resample('D').mean()
                    fig = go.Figure(data=[go.Candlestick(x=df_daily.index,
                                                         open=df_daily['Open'], high=df_daily['High'],
                                                         low=df_daily['Low'], close=df_daily['Close*'])])
                    fig.update_layout(xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                    df_nifty.reset_index(inplace=True)
        if candle_plot == "no":
            pass
    st.subheader("Conclusions")
    st.write("Candle_stick plot is main resource for income to traders it will tell how market is moving"
             " whether it is in uptrend or downtrend just change the frequency and observe the trend in market")
    st.markdown("---")

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_nifty['Date'],y=df_nifty['Open'],name='Stock_open'))
            fig.add_trace(go.Scatter(x=df_nifty['Date'], y=df_nifty['Close*'],name='Stock_close'))
            fig.layout.update(title_text="Time_Series_data",xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
            st.subheader("Conclusions")
            st.write("This plot is between closing price and open price"
                     " we can say both are very similar with suttle difference that difference gives traders the good profit")
        with col2:
            st.write("Correlation_plot")
            fig,ax=plt.subplots(figsize=(4,2))
            sns.heatmap(df_nifty.corr(), cmap="YlGnBu", annot=True)
            st.pyplot(fig)
            st.subheader("Conclusion")
            st.write("1 indicate good correlation and 0 indicates no correlatio"
                     " ,if values are positive it indicates positive correlation(means if one feature increases"
                     " the other also increases vice versa)"
                     " ,if value is negative then it indicates negative correlation (means if one feature increases"
                     " the other also increases vice versa)")
            st.write("we can say there is a good correlation between the all features")
    st.markdown("----")

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            option = st.selectbox(
                'Slect company Nifty',
                df_nifty_companies["COMPANY"])
        with col2:
            df_nifty_companies.set_index(["COMPANY"],inplace=True)
            st.subheader("Company Current Stats")
            st.write(df_nifty_companies.loc[option])
            df_nifty_companies.reset_index(inplace=True)
    st.subheader("Conclusions")
    st.write("this shows the current market price of the company that is present in Nifty index"
             " choose the company according to you and see the particular company data")


def Analysis_on_Sunsex():
    global df_sunsex, df_sunsex_companies

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='text-align: left; color: black;'>'Descriptive Statistic on Sunsex --------------------------------------->'</h4>", unsafe_allow_html=True)
        with col2:
            descriptive_sunsex = df_sunsex[["Open","Close*","Low","High","Volume","Adj Close**"]].describe()
            st.write(descriptive_sunsex)
    st.markdown("---")
    with st.container():
        st.subheader("Univariate Analysis")
        option = st.selectbox(
            "Choose__",
            ("Open","Close*","Low","High","Volume","Adj Close**"))
        col1,col2,col3 = st.columns(3)
        with col1:
            st.write("PDF of {}".format(option))
            fig,ax = plt.subplots()
            sns.distplot(df_sunsex[option])
            st.pyplot(fig)
        with col2:
            st.write("CDF of {}".format(option))
            fig,ax = plt.subplots()
            sns.ecdfplot(df_sunsex[option])
            st.pyplot(fig)
        with col3:
            st.write("Box plot of {}".format(option))
            fig, ax = plt.subplots()
            sns.boxplot(df_sunsex[option])
            st.pyplot(fig)
        st.subheader("Conclusions")
        ma = df_sunsex[option].max()
        mi = df_sunsex[option].min()
        avg = df_sunsex[option].mean()
        p_25 = np.percentile(df_sunsex[option], 25)
        p_75 = np.percentile(df_sunsex[option], 75)
        st.write("The Maximum {} is  {} at this Date {}".format(option, ma, df_nifty[df_sunsex[option] == ma]["Date"]))
        st.write("The minimum {} is {} at this Date {}".format(option, mi, df_nifty[df_sunsex[option] == mi]["Date"]))
        st.write("The avg {} is {}".format(option, avg))
        st.write("most of the time {} lie between {} and {}".format(option, p_25, p_75))

    st.markdown("---")
    with st.container():
        st.subheader("Bivariate Analysis")
        col1,col2 = st.columns(2)
        with col1:
            option = st.selectbox(
                "choose_any_1_",
                ("Open", "Close*", "Low", "High", "Volume", "Adj Close**"))
        with col2:
            option1 = st.selectbox(
                "choose_other_1",
                ( "Close*","Open","Low", "High", "Volume", "Adj Close**"))
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Scatter plot between {} and {}".format(option,option1))
            fig, ax = plt.subplots()
            sns.scatterplot(data=df_sunsex, x=option, y=option1)
            st.pyplot(fig)
        with col2:
            st.write("Line plot between {} and {}".format(option,option1))
            fig, ax = plt.subplots()
            sns.lineplot(x =option, y =option1, data = df_sunsex)
            st.pyplot(fig)
        with col3:
            st.write("Regression plot between {} and {}".format(option,option1))
            fig, ax = plt.subplots()
            sns.regplot(x=option, y=option1, data=df_sunsex)
            st.pyplot(fig)

        st.subheader("Conclusions")
        st.write("Just visualize how features are behaving with each other")

    st.markdown("---")

    st.markdown("<h2 style='text-align: center; color: black;'>'Technical analysis on Sensex'</h2>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            option = st.selectbox(
                'Slect_on',
                ('Daily','Weekly', 'Monthly'))
            if option == None:
                st.write("Please Select")
        with col2:
            option1 = st.selectbox(
                'Slect_o',
                ('Volume','Open', 'Close', 'Low', 'High'))
            if option1 == None:
                st.write("Please Select")
        with col3:
            if option == 'Weekly':
                df_sunsex.set_index(["Date"], inplace=True)
                df_weekly = df_sunsex.resample('W').mean()
                if option1 == "Open":
                    st.bar_chart(df_weekly["Open"])
                if option1 == "Close":
                    st.bar_chart(df_weekly["Close*"])
                if option1 == "Low":
                    st.bar_chart(df_weekly["Low"])
                if option1 == "High":
                    st.bar_chart(df_weekly["High"])
                if option1 == "Volume":
                    st.bar_chart(df_weekly["Volume"])
                df_sunsex.reset_index(inplace=True)
            if option == 'Monthly':
                df_sunsex.set_index(["Date"], inplace=True)
                df_Monthly = df_sunsex.resample('M').mean()
                if option1 == "Open":
                    st.bar_chart(df_Monthly["Open"])
                if option1 == "Close":
                    st.bar_chart(df_Monthly["Close*"])
                if option1 == "Low":
                    st.bar_chart(df_Monthly["Low"])
                if option1 == "High":
                    st.bar_chart(df_Monthly["High"])
                if option1 == "Volume":
                    st.bar_chart(df_Monthly["Volume"])
                df_sunsex.reset_index(inplace=True)
            if option == 'Daily':
                df_sunsex.set_index(["Date"], inplace=True)
                df_Daily = df_sunsex.resample('D').mean()
                if option1 == "Open":
                    st.bar_chart(df_Daily["Open"])
                if option1 == "Close":
                    st.bar_chart(df_Daily["Close*"])
                if option1 == "Low":
                    st.bar_chart(df_Daily["Low"])
                if option1 == "High":
                    st.bar_chart(df_Daily["High"])
                if option1 == "Volume":
                    st.bar_chart(df_Daily["Volume"])
                df_sunsex.reset_index(inplace=True)

    st.subheader("Conclusions")
    st.write("Just change the frequency like daily or monthly or weekly and see how stock price is changing ")
    st.markdown("---")

    with st.container():
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            candle_plot = st.radio("please_select_yes_or_not_to_see_the_Candle_stick_plot", ("yes", "no"))
        if candle_plot == "yes":
            with col2:
                option = st.selectbox(
                    'Slect_below',
                    ('Daily','Monthly', 'Weekly'))
            with col3:
                if option == 'Weekly':
                    df_sunsex.set_index(["Date"], inplace=True)
                    df_weekly = df_sunsex.resample('W').mean()
                    fig = go.Figure(data=[go.Candlestick(x=df_weekly.index,
                                                         open=df_weekly['Open'], high=df_weekly['High'],
                                                         low=df_weekly['Low'], close=df_weekly['Close*'])])
                    fig.update_layout(xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                    df_sunsex.reset_index(inplace=True)
                if option == 'Monthly':
                    df_sunsex.set_index(["Date"], inplace=True)
                    df_monthly = df_sunsex.resample('M').mean()
                    fig = go.Figure(data=[go.Candlestick(x=df_monthly.index,
                                                         open=df_monthly['Open'], high=df_monthly['High'],
                                                         low=df_monthly['Low'], close=df_monthly['Close*'])])
                    fig.update_layout(xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                    df_sunsex.reset_index(inplace=True)
                if option == 'Daily':
                    df_sunsex.set_index(["Date"], inplace=True)
                    df_daily = df_sunsex.resample('D').mean()
                    fig = go.Figure(data=[go.Candlestick(x=df_daily.index,
                                                         open=df_daily['Open'], high=df_daily['High'],
                                                         low=df_daily['Low'], close=df_daily['Close*'])])
                    fig.update_layout(xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)
                    df_sunsex.reset_index(inplace=True)
        if candle_plot == "no":
            pass
    st.subheader("Conclusions")
    st.write("Candle_stick plot is main resource for income to traders it will tell how market is moving"
             " whether it is in uptrend or downtrend just change the frequency and observe the trend in market")
    st.markdown("---")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_sunsex['Date'], y=df_sunsex['Open'], name='Stock_open'))
            fig.add_trace(go.Scatter(x=df_sunsex['Date'], y=df_sunsex['Close*'], name='Stock_close'))
            fig.layout.update(title_text="Time_Series_data", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
            st.subheader("Conclusions")
            st.write("This plot is between closing price and open price"
                     " we can say both are very similar with suttle difference that difference gives traders the good profit")
        with col2:
            st.write("Correlation_plot")
            fig, ax = plt.subplots(figsize=(4,2))
            sns.heatmap(df_sunsex.corr(), cmap="YlGnBu", annot=True)
            st.pyplot(fig)
            st.subheader("Conclusion")
            st.write("1 indicate good correlation and 0 indicates no correlatio"
                     " ,if values are positive it indicates positive correlation(means if one feature increases"
                     " the other also increases vice versa)"
                     " ,if value is negative then it indicates negative correlation (means if one feature increases"
                     " the other also increases vice versa)")
            st.write("we can say there is a good correlation between the all features")
    st.markdown("---")

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            option = st.selectbox(
                'Slect company Sunsex',
                df_sunsex_companies["COMPANY"])
        with col2:
            df_sunsex_companies.set_index(["COMPANY"],inplace=True)
            st.write("Company Current Stats")
            st.write(df_sunsex_companies.loc[option])
            df_sunsex_companies.reset_index(inplace=True)
        st.subheader("Conclusions")
        st.write("this shows the current market price of the company that is present in Nifty index"
                 " choose the company according to you and see the particular company data")

def predict():
    st.markdown("<h2 style='text-align: center; color: black;'>'Prediction of Closing price'</h2>",
                unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        option = st.selectbox("Choose",
                              ('Nifty','Sunsex'))
        st.write("You selected",option)
    with col2:
        option1 = st.text_input("Please give the open value 👇","15000")
        st.write("You entered",option1)
    with col3:
        if option == "Nifty":
            X = np.array(df_nifty["Open"].copy()).reshape(-1, 1)
            y = np.array(df_nifty["Close*"].copy()).reshape(-1, 1)
            model = LinearRegression()
            model.fit(X, y)
            try:
                temp = np.array(int(option1)).reshape(1,-1)
                st.subheader("the predicted value for Nifty is:")
                st.write(model.predict(temp))
            except:
                st.markdown("<h2 style='text-align: left; color: red;'>'Please Enter the Open Value'</h2>", unsafe_allow_html=True)
        if option == "Sunsex":
            X = np.array(df_sunsex["Open"].copy()).reshape(-1, 1)
            y = np.array(df_sunsex["Close*"].copy()).reshape(-1, 1)
            model = LinearRegression()
            model.fit(X, y)
            try:
                temp = np.array(int(option1)).reshape(1, -1)
                st.subheader("the predicted value for Sunsex is:")
                st.write(model.predict(temp))
            except:
                st.markdown("<h2 style='text-align: left; color: red;'>'Please Enter the Open Value'</h2>", unsafe_allow_html=True)


if __name__ == "__main__":
    df_nifty, df_sunsex, df_nifty_companies, df_sunsex_companies = data_fetching()
    st.markdown("<h1 style='text-align: center; color: black;'>Data Analysis on NSE(NIFTY) and BSE(SUNSEX)</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: right; color: black;'>'By Ali Nawaz'</h2>",unsafe_allow_html=True)
    st.subheader("The stock market refers to a marketplace where publicly "
             " traded company stocks are bought and sold. Investors can purchase stocks in companies they believe"
             " will perform well, with the goal of making a profit by selling the stock for more than they paid for it.")
    st.subheader("The stock market is often considered a barometer of a country's economic health, as well as a means for "
                 " companies to raise capital. Stock prices are influenced by a number of factors, including a "
                 " company's financial performance, economic conditions, and investor sentiment.")
    st.subheader("The largest stock market in the world is the New York Stock Exchange (NYSE), followed by the NASDAQ"
                 " when it comes to india NSE and BSE plays major role.")
    st.markdown('---')
    st.markdown('---')



    st.subheader("The Nifty stock data")
    st.write("Nifty 50 is a stock market index in India, representing the performance of 50 of the largest and "
             " most actively traded stocks listed on the National Stock Exchange of India (NSE). The Nifty 50 is widely used as"
             " a barometer of the Indian stock market and is considered one of the leading benchmarks of the Indian equity market.")

    col1, col2 = st.columns(2)
    with col1:
        st.write(df_nifty)
    with col2:
        image = Image.open("NSE_image.jpg")
        st.image(image, caption='NSE_office')
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: black;'>'Data analysis on Nifty'</h2>", unsafe_allow_html=True)
    Analysis_on_Nifty()

    st.markdown('---')
    st.markdown('----')

    st.subheader("The Sensex stock data")
    st.write("The Sensex, also known as the BSE 30 or the Bombay Stock Exchange 30, is a stock market index in"
             " India that represents the performance of 30 of the largest and most actively traded stocks listed on the Bombay"
             " Stock Exchange (BSE). The Sensex is widely used as a barometer of the Indian stock market and is considered"
             " one of the leading benchmarks of the Indian equity market")
    col1, col2 = st.columns(2)
    with col1:
        st.write(df_sunsex)
    with col2:
        image = Image.open("BSE_image.jpg")
        st.image(image, caption='SUNSEX_office')
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: black;'>'Data analysis on Sensex'</h2>", unsafe_allow_html=True)
    Analysis_on_Sunsex()

    st.markdown('---')
    st.markdown('----')

    predict()

    st.markdown('----')
    st.markdown('----')

    st.markdown("<h2 style='text-align: center; color: black;'>'THANK YOU'</h2>", unsafe_allow_html=True)
