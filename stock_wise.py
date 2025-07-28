import pandas as pd
import matplotlib.pyplot as plt
import calendar

# List of stocks and corresponding file names
stocks = {
    "TRH": "https://github.com/icarussfalls/AnomalyDetectionNepse/raw/main/datas/TRH.csv",
    "SHL": "https://github.com/icarussfalls/AnomalyDetectionNepse/raw/main/datas/SHL.csv"
}

monthly_avg_returns = {}

for name, url in stocks.items():
    # Load CSV (expects 'timestamp' and 'close' columns)
    df = pd.read_csv(url, parse_dates=['date'])
    df = df.sort_values('date')
    df.set_index('date', inplace=True)

    # Resample to monthly close
    monthly_close = df['close'].resample('M').last()

    # Compute monthly returns
    monthly_returns = monthly_close.pct_change().dropna()

    # Assign month number
    monthly_returns = monthly_returns.to_frame(name='return')
    monthly_returns['month'] = monthly_returns.index.month

    # Compute average return by calendar month
    avg_returns = monthly_returns.groupby('month')['return'].mean() * 100  # in percent
    monthly_avg_returns[name] = avg_returns

# Combine into one DataFrame
seasonal_df = pd.DataFrame(monthly_avg_returns)
seasonal_df.index = [calendar.month_abbr[m] for m in seasonal_df.index]

# Display
print("Average Monthly Return (%) by Stock:")
print(seasonal_df.round(2))

# Optional: plot
seasonal_df.plot(kind='bar', figsize=(12, 6), title="Seasonal Monthly Return Pattern (TRH vs SHL)")
plt.ylabel("Average Monthly Return (%)")
plt.xlabel("Month")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
plt.savefig("monthly_avg_returns_stocks.png", dpi=300)