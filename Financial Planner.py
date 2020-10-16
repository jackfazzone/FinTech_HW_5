# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

null.tpl [markdown]
# # Unit 5 - Financial Planning
# 

# %%
# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation

get_ipython().run_line_magic('matplotlib', 'inline')


# %%
# Load .env enviroment variables
load_dotenv()

null.tpl [markdown]
# ## Part 1 - Personal Finance Planner
null.tpl [markdown]
# ### Collect Crypto Prices Using the `requests` Library

# %%
# Set current amount of crypto assets
my_btc = 1.2
my_eth = 5.3


# %%
# Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=CAD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=CAD"


# %%
# Fetch current BTC price
btc_req = requests.get(btc_url)
btc_data = btc_req.json()
btc_price = btc_data['data']['1']['quotes']['USD']['price']


# Fetch current ETH price
eth_req = requests.get(eth_url)
eth_data = eth_req.json()
eth_price = eth_data['data']['1027']['quotes']['USD']['price']

# Compute current value of my crpto
my_btc_value = my_btc * btc_price
my_eth_value = my_eth * eth_price

# Print current crypto wallet balance
print(f"The current value of your {my_btc} BTC is ${my_btc_value:0.2f}")
print(f"The current value of your {my_eth} ETH is ${my_eth_value:0.2f}")

null.tpl [markdown]
# ### Collect Investments Data Using Alpaca: `SPY` (stocks) and `AGG` (bonds)

# %%
# Current amount of shares
my_agg = 200
my_spy = 50


# %%
# Set Alpaca API key and secret
alpaca_api_key = os.getenv("APCA_API_KEY")
alpaca_secret_key = os.getenv("APCA_API_SECRET")

# Create the Alpaca API object
alpaca = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version="v2"
)


# %%
# Format current date as ISO format
start_date = pd.Timestamp("2020-10-15", tz="America/New_York").isoformat()
end_date = pd.Timestamp("2020-10-15", tz="America/New_York").isoformat()

# Set the tickers
tickers = ["AGG", "SPY"]

# Set timeframe to '1D' for Alpaca API
timeframe = "1D"

# Get current closing prices for SPY and AGG
df_ticker = alpaca.get_barset(
    tickers,
    timeframe,
    start=start_date,
    end=end_date
).df

current_date = df_ticker.index[0]
# Preview DataFrame
df_ticker.head()


# %%
# Pick AGG and SPY close prices
agg_close_price = df_ticker["AGG"]["close"][current_date]
spy_close_price = df_ticker["SPY"]["close"][current_date]

# Print AGG and SPY close prices
print(f"Current AGG closing price: ${agg_close_price}")
print(f"Current SPY closing price: ${spy_close_price}")


# %%
# Compute the current value of shares
my_agg_value = my_agg * agg_close_price
my_spy_value = my_spy * spy_close_price

# Print current value of share
print(f"The current value of your {my_spy} SPY shares is ${my_spy_value:0.2f}")
print(f"The current value of your {my_agg} AGG shares is ${my_agg_value:0.2f}")

null.tpl [markdown]
# ### Savings Health Analysis

# %%
# Set monthly household income
monthly_income = 12000

# Create savings DataFrame
df_savings = pd.DataFrame(index=["crypto","shares"], columns = ["Amount"])
df_savings['Amount']['crypto']= my_eth_value + my_btc_value
df_savings['Amount']['shares']= my_agg_value + my_spy_value

# Display savings DataFrame
display(df_savings)


# %%
# Plot savings pie chart
df_savings.plot.pie(y="Amount")


# %%
# Set ideal emergency fund
emergency_fund = monthly_income * 3

# Calculate total amount of savings
total_savings = sum(df_savings["Amount"])

# Validate saving health
if total_savings > emergency_fund:
    print("Congratulations, your savings are exceed an ideal emergency fund!")
elif total_savings == emergency_fund:
    print("Congratulations, your savings are equal to an ideal emergency fund!")
else:
    print(f"Your savings are short of an ideal emergency fund by {total_savings - emergency_fund}")

null.tpl [markdown]
# ## Part 2 - Retirement Planning
# 
# ### Monte Carlo Simulation

# %%
# Set start and end dates of five years back from today.
# Sample results may vary from the solution based on the time frame chosen
start_date = pd.Timestamp('2015-08-07', tz='America/New_York').isoformat()
end_date = pd.Timestamp('2020-10-15', tz='America/New_York').isoformat()


# %%
# Get 5 years' worth of historical data for SPY and AGG
df_stock_data = alpaca.get_barset(
    tickers,
    timeframe,
    start=start_date,
    end=end_date
).df

# Display sample data
df_stock_data


# %%
# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns
MC_thirtyyear = MCSimulation(
    portfolio_data = df_stock_data,
    weights = [.40,.60],
    num_simulation = 500,
    num_trading_days = 252*30
)


# %%
# Printing the simulation input data
MC_thirtyyear.portfolio_data.head()


# %%
# Running a Monte Carlo simulation to forecast 30 years cumulative returns
MC_thirtyyear.calc_cumulative_return()


# %%
# Plot simulation outcomes
line_plot = MC_thirtyyear.plot_simulation()


# %%
# Plot probability distribution and confidence intervals
dist_plot = MC_thirtyyear.plot_distribution()

null.tpl [markdown]
# ### Retirement Analysis

# %%
# Fetch summary statistics from the Monte Carlo simulation results
summary = MC_thirtyyear.summarize_cumulative_return()

# Print summary statistics
print(summary)

null.tpl [markdown]
# ### Calculate the expected portfolio return at the 95% lower and upper confidence intervals based on a `$20,000` initial investment.

# %%
# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
ci_lower = round(summary[8]*initial_investment,2)
ci_upper = round(summary[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")

null.tpl [markdown]
# ### Calculate the expected portfolio return at the `95%` lower and upper confidence intervals based on a `50%` increase in the initial investment.

# %%
# Set initial investment
initial_investment = 20000 * 1.5

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000
ci_lower = round(summary[8]*initial_investment,2)
ci_upper = round(summary[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")

null.tpl [markdown]
# ## Optional Challenge - Early Retirement
# 
# 
# ### Five Years Retirement Option

# %%
# Configuring a Monte Carlo simulation to forecast 5 years cumulative returns
MC_fiveyear = MCSimulation(
    portfolio_data = df_stock_data,
    weights = [.10,.90],
    num_simulation = 500,
    num_trading_days = 252*5
)


# %%
# Running a Monte Carlo simulation to forecast 5 years cumulative returns
MC_fiveyear.calc_cumulative_return()


# %%
# Plot simulation outcomes
line_plot = MC_fiveyear.plot_simulation()


# %%
# Plot probability distribution and confidence intervals
dist_plot = MC_fiveyear.plot_distribution()


# %%
# Fetch summary statistics from the Monte Carlo simulation results
summary_five_year = MC_fiveyear.summarize_cumulative_return()

# Print summary statistics
print(summary_five_year)


# %%
# Set initial investment
initial_investment = 60000
# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
ci_lower_five = round(summary_five_year[8]*initial_investment,2)
ci_upper_five = round(summary_five_year[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 5 years will end within in the range of"
      f" ${ci_lower_five} and ${ci_upper_five}")

null.tpl [markdown]
# ### Ten Years Retirement Option

# %%
# Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
MC_tenyear = MCSimulation(
    portfolio_data = df_stock_data,
    weights = [.20,.80],
    num_simulation = 500,
    num_trading_days = 252*10
)


# %%
# Running a Monte Carlo simulation to forecast 10 years cumulative returns
MC_tenyear.calc_cumulative_return()


# %%
# Plot simulation outcomes
line_plot = MC_tenyear.plot_simulation()


# %%
# Plot probability distribution and confidence intervals
dist_plot = MC_tenyear.plot_distribution()


# %%
# Fetch summary statistics from the Monte Carlo simulation results
summary_ten_year = MC_tenyear.summarize_cumulative_return()

# Print summary statistics
print(summary_ten_year)


# %%
# Set initial investment
initial_investment = 60000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
ci_lower_ten = round(summary_ten_year[8]*initial_investment,2)
ci_upper_ten = round(summary_ten_year[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 10 years will end within in the range of"
      f" ${ci_lower_ten} and ${ci_upper_ten}")


# %%



