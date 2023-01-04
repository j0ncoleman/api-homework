# Initial imports
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import yfinance as yf
from MCForecastTools import MCSimulation
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

# Collect Crypto Prices Using the `requests` Library

# Load .env enviroment variables
load_dotenv()


# Set current amount of crypto assets
my_btc = 1.2
my_eth = 5.3

# Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=CAD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=CAD"

# Fetch current BTC price
btc_data = requests.get(btc_url).json()

btc_price = btc_data["data"]["1"]["quotes"]["CAD"]["price"]
print(btc_price)

# Fetch current ETH price
eth_data = requests.get(eth_url).json()

eth_price = eth_data["data"]["1027"]["quotes"]["CAD"]["price"]
print(eth_price)

# Compute current value of my crpto
my_btc_value = my_btc * btc_price
my_eth_value = my_eth * eth_price

# Print current crypto wallet balance
print(f"The current value of your {my_btc} BTC is ${my_btc_value:0.2f}")
print(f"The current value of your {my_eth} ETH is ${my_eth_value:0.2f}")


# Set current amount of shares
my_agg = 200
my_spy = 50

# Set the tickers
tickers = ["agg", "spy"]

# Set DataFrames
agg_data = yf.Ticker(tickers[0])
spy_data = yf.Ticker(tickers[1])

# Format current date as ISO format
start_date = dt.datetime(2022, 12, 30)
end_date = dt.datetime(2022, 12, 31)

agg_df = pd.DataFrame(agg_data.history(
    period='1d', start=start_date, end=end_date))
agg_df.insert(0, "Symbol", 'AGG')
spy_df = pd.DataFrame(spy_data.history(
    period='1d', start=start_date, end=end_date))
spy_df.insert(0, "Symbol", 'SPY')

# Get current closing prices for SPY and AGG
agg_price = agg_df.iloc[0, 4]
spy_price = spy_df.iloc[0, 4]

# Concatenate the ticker DataFrames
ticker_data = pd.concat([agg_df, spy_df], axis="rows", join="inner")

# Preview DataFrame
ticker_data.head()

# Print AGG and SPY close prices
print(f"Current AGG closing price: ${agg_price}")
print(f"Current SPY closing price: ${spy_price}")

# Compute the current value of shares
my_agg_value = my_agg * agg_price
my_spy_value = my_spy * spy_price

# Print current value of shares
print(f"The current value of your {my_spy} SPY shares is ${my_spy_value:0.2f}")
print(f"The current value of your {my_agg} AGG shares is ${my_agg_value:0.2f}")


# Set monthly household income
monthly_income = 12000

crypto_value = my_btc_value + my_eth_value
stocks_value = my_agg_value + my_spy_value

# Consolidate financial assets data
df_savings = pd.DataFrame(
    data=[crypto_value, stocks_value], index=["crypto", "shares"], columns=["amount"])

# Display savings DataFrame
display(df_savings)

# Plot savings pie chart
savings_pie_chart = df_savings.plot.pie(y="amount")

# Set ideal emergency fund
emergency_fund = monthly_income * 3

# Calculate total amount of savings
total_savings = crypto_value + stocks_value

# Validate saving health
if(total_savings >= emergency_fund):
    print("Congratulations! You have enough money in the emergency fund.")
elif(total_savings < emergency_fund):
    print(
        f"Sorry! You need ${emergency_fund - total_savings} to reach your goal.")


# Set start and end dates of five years back from today.
# Sample results may vary from the solution based on the time frame chosen

# Get 5 years' worth of historical data for SPY and AGG
# Format current date as ISO format
start_date = dt.datetime(2016, 5, 1)
end_date = dt.datetime(2021, 5, 1)

agg_5y_df = pd.DataFrame(agg_data.history(
    period='1d', start=start_date, end=end_date))
# agg_5y_df.insert(0, "Symbol", 'AGG')
spy_5y_df = pd.DataFrame(spy_data.history(
    period='1d', start=start_date, end=end_date))
# spy_5y_df.insert(0, "Symbol", 'SPY')

# Reorganize the DataFrame
# Separate ticker data
weights = [0.6, 0.4]


# Concatenate the ticker DataFrames
df_stock_data = pd.concat([agg_5y_df, spy_5y_df],
                          axis=1, join="inner", keys=["AGG", "SPY"])
df_stock_data = df_stock_data.rename(columns=str.lower)
# Display sample data
df_stock_data.head()

# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns
# Set number of simulations
num_sims = 500

# Configure a Monte Carlo simulation to forecast one year daily returns
MC_PORTFOLIO = MCSimulation(
    portfolio_data=df_stock_data,
    weights=weights,
    num_simulation=num_sims,
    num_trading_days=252 * 30
)

# Printing the simulation input data

# Running a Monte Carlo simulation to forecast 30 years cumulative returns
cumulative_returns = MC_PORTFOLIO.calc_cumulative_return()

# Plot simulation outcomes
line_plot = MC_PORTFOLIO.plot_simulation()

# Plot probability distribution and confidence intervals
distribution_plot = MC_PORTFOLIO.plot_distribution()

# Fetch summary statistics from the Monte Carlo simulation results
summary = MC_PORTFOLIO.summarize_cumulative_return()

# Print summary statistics
print(summary)

# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
# YOUR CODE HERE!

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")

# Set initial investment
initial_investment = 20000 * 1.5

# Use the lower and`` upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000
# YOUR CODE HERE!

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")
