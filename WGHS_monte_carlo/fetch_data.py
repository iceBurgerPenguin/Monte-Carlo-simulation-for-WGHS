import yfinance as yf
import pandas as pd
import numpy as np
import warnings
import os

warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

# proxy = '185.152.67.39:7890'
# os.environ['HTTP_PROXY'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

# proxies = {
#     "http": "127.0.0.1:8080",
#     "https": "127.0.0.1:8080",
# }



def get_returns(ticker, start_year, end_year):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=f'{start_year}-01-01' ,end = f'{end_year+1}-01-01',interval="1d")
    hist = hist["Close"]
    df  = pd.DataFrame(hist)
    df = df.reset_index()
    return df

def get_annual_prices(group):
    jan = group[group['Date'].dt.month == 1].iloc[:5]['Close'].mean()
    dec = group[group['Date'].dt.month == 12].iloc[-5:]['Close'].mean()
    return pd.Series({'Jan_First_Price': jan, 'Dec_Last_Price': dec})


def calc_arr(df):
    df = df[(df["Date"].dt.month == 1) | (df["Date"].dt.month == 12)]
    df["Year"] = df["Date"].dt.year
    annual_prices = df.groupby('Year').apply(get_annual_prices).reset_index()
    annual_prices["ARR"] = (annual_prices["Dec_Last_Price"]/annual_prices["Jan_First_Price"])-1
    return annual_prices



def mean_spread(df):
    annual_rates = list(df["ARR"])
    mean = np.mean(annual_rates)
    std = np.std(annual_rates)
    return mean, std


def main(ticker,start_yr=2015,end_yr=2024):
    df = get_returns(ticker, start_yr, end_yr)
    annual_rate_df = calc_arr(df)
    mean, std = mean_spread(annual_rate_df)
    print(ticker,mean,std)
    return mean, std

# df = get_returns('GOOGL', 2015, 2024)
# annual_rate_df = calc_arr(df)
# print(annual_rate_df)