import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
import numpy as np

# --- Step 1: Load and prepare daily data ---
hotels_df = pd.read_csv("HOTELS_saved.csv")
hotels_df["timestamp"] = pd.to_datetime(hotels_df["timestamp"])
hotels_df.set_index("timestamp", inplace=True)
print("HOTELS.csv loaded successfully.")

series = hotels_df['close']
monthly_series = series.resample('M').mean().dropna()

# --- Step 2: Perform seasonal decomposition ---
result = seasonal_decompose(monthly_series, model='additive', period=12)

# --- Step 3: Plot decomposition and monthwise seasonal pattern ---
fig, axes = plt.subplots(5, 1, figsize=(16, 16), sharex=False)

# Format shared style
for ax in axes[:4]:
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.grid(True, which='major', linestyle='--', linewidth=0.5)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.3)

# Observed
axes[0].plot(result.observed, color='blue', label="Observed Index")
axes[0].set_ylabel("Index Level", fontsize=12)
axes[0].set_title("Observed Hotels Index (Monthly Avg)", fontsize=14)
axes[0].legend()

# Trend
axes[1].plot(result.trend, color='green', label="Trend")
axes[1].set_ylabel("Trend", fontsize=12)
axes[1].set_title("Trend Component", fontsize=14)
axes[1].legend()

# Seasonal (full time series)
axes[2].plot(result.seasonal, color='orange', label="Seasonal")
axes[2].set_ylabel("Seasonality", fontsize=12)
axes[2].set_title("Seasonal Component (Annual Cycle Over Time)", fontsize=14)
axes[2].legend()

# Residual
axes[3].plot(result.resid, color='gray', label="Residuals")
axes[3].set_ylabel("Residuals", fontsize=12)
axes[3].set_title("Residual Component", fontsize=14)
axes[3].set_xlabel("Date (YYYY-MM)", fontsize=12)
axes[3].legend()

# --- Step 4: Aggregate seasonality by month for descriptive plot ---
seasonal_df = result.seasonal.to_frame(name='seasonality')
seasonal_df['month'] = seasonal_df.index.month
avg_seasonality = seasonal_df.groupby('month').mean().reindex(np.arange(1,13))

# Descriptive seasonal pattern: Bar plot by month
month_names = list(calendar.month_abbr)[1:]  # Jan to Dec
axes[4].bar(month_names, avg_seasonality['seasonality'], color='orange', edgecolor='black')
axes[4].set_title("Average Seasonal Effect by Month – Hotels Sector", fontsize=14)
axes[4].set_ylabel("Seasonal Impact")
axes[4].grid(True, linestyle='--', linewidth=0.4)

# --- Final formatting ---
fig.suptitle("Seasonal Decomposition of NEPSE Hotels Sector Index", fontsize=18, y=1.02)
plt.tight_layout()
plt.savefig("seasonal_decomposition_hotels_with_monthwise_barplot.png", dpi=300)
print("Full seasonal decomposition with monthwise bar chart saved.")
plt.show()

# Save monthwise average seasonal index for LaTeX report
avg_seasonality.index = month_names  # Set index to month names for clarity
avg_seasonality.to_csv("hotels_monthwise_seasonality.csv", float_format="%.2f")
print("Monthwise seasonal index data saved to hotels_monthwise_seasonality.csv.")
