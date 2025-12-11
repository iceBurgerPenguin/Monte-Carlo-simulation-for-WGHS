import pandas as pd
import numpy as np
import fetch_data
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=".*DataFrameGroupBy.apply operated on the grouping columns.*"
)


# Get std, mean for every set of portfolio
class Index():
    def __init__(self, name, mean, std, weight):
        self.name = name
        self.mean = mean
        self.std = std
        self.weight = weight

    def get_std(self):
        return self.std

    def get_mean(self):
        return self.mean

    def get_name(self):
        return self.name

    def get_weight(self):
        return self.weight


mid_dict = {
    "XLK": 0.10,  # S&P 500 Information Technology
    "XLV": 0.05,  # S&P 500 Health Care
    "XLP": 0.05,  # S&P 500 Consumer Staples
    "XLI": 0.05,  # S&P 500 Industrials
    "ACWI": 0.20,  # S&P Global BMI
    "NOBL": 0.13,  # S&P 500 High Dividend Growth
    "XLE": 0.07,  # S&P 500 Energy
    "LQD": 0.15,  # Investment Grade Corporate Bond Index
    "AGG": 0.10,  # Morningstar US Core Bond
    "GSG": 0.05  # S&P GSCI
}

low_dict = {
    "XLU": 0.04,  # Utilities
    "XLP": 0.09,  # Consumer Staples
    "XLV": 0.11,  # Health Care
    "SPLV": 0.16,  # Low Volatility Index
    "GOVT": 0.20,  # US Government Bond Index
    "SHV": 0.15,  # Ultra Short Treasury
    "TLT": 0.10,  # 10+ Year Treasury
    "TIP": 0.05,  # TIPS
    "GLD": 0.05  # GSCI Gold
}

#High risk portfolio by index
# high_dict = {
#     "ROBO": 0.08,   # AI exposure (OpenAI replacement)
#     "QQQ": 0.49,    # Mega-cap tech + growth exposure
#     "KWEB": 0.05,   # China Internet
#     "XLV": 0.03,    # US Health Care sector
#     "IYE": 0.10,    # Energy sector
#     "GLD": 0.05,    # Gold
#     "PPLT": 0.05,   # Platinum
#     "TLT": 0.03,    # Long-term US Treasuries
#     "LQD": 0.02,    # Investment-grade corporate bonds
#     "CASH": 0.10    # Cash
# }

high_dict = {
    "MSFT": 0.22,   # 14% original + 8% from OpenAI
    "GOOG": 0.10,   # Mega-cap tech / growth
    "AMZN": 0.10,   # Mega-cap tech / growth
    "BABA": 0.05,   # China Internet
    "UNH": 0.03,    # US Health Care sector
    "QQQ": 0.15,    # Broad tech / growth ETF
    "IYE": 0.10,    # Energy sector
    "GLD": 0.05,    # Gold
    "PPLT": 0.05,   # Platinum
    "TLT": 0.03,    # Long-term US Treasuries
    "LQD": 0.02,    # Investment-grade corporate bonds
    "CASH": 0.10    # Cash
}



def tickers_to_object_lists(ticker_dict):
    list = []
    for key, value in ticker_dict.items():
        mean, std = fetch_data.main(key, 2015, 2024)
        object = Index(key, mean, std, value)
        list.append(object)

    return list


def compute_overall_mean_and_std(obj_list):
    mean_list = [obj.get_mean() * obj.get_weight() for obj in obj_list]
    mean = np.sum(mean_list)

    std_array = np.array([obj.get_std() for obj in obj_list])
    weight_array = np.array([obj.get_weight() for obj in obj_list])

    variance = np.sum((weight_array ** 2) * (std_array ** 2))
    std = np.sqrt(variance)

    return mean, std


def main(dict):
    # MID RISK PORTFOLIO
    obj_list = tickers_to_object_lists(dict)
    mean, std = compute_overall_mean_and_std(obj_list)
    return mean, std


high_mean, high_std = main(high_dict)
print("high_risk_mean", high_mean, "high_risk_std", high_std)

mid_mean, mid_std = main(mid_dict)
print("mid_risk_mean", mid_mean, "mid_risk_std", mid_std)

low_mean, low_std = main(low_dict)
print("low_risk_mean", low_mean, "low_risk_std", low_std)

