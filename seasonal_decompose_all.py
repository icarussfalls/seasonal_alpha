import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
import numpy as np
import os

input_dir = "index_data"
output_dir = "decomposition_outputs"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(input_dir, filename)
        try:
            df = pd.read_csv(filepath)
            if "timestamp" not in df.columns or "close" not in df.columns:
                print(f"Skipping {filename}: missing required columns.")
                continue
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df.set_index("timestamp", inplace=True)
            series = df['close']

            # Calculate monthly returns using first and last close of each month
            monthly_first = series.resample('M').first()
            monthly_last = series.resample('M').last()
            monthly_returns = ((monthly_last - monthly_first) / monthly_first * 100).dropna()

            monthly_series = series.resample('M').mean().dropna()
            if len(monthly_series) < 24:
                print(f"Skipping {filename}: not enough data for decomposition.")
                continue


            if len(monthly_returns) < 24:
                print(f"Skipping {filename}: not enough return data for decomposition.")
                continue

            result = seasonal_decompose(monthly_returns, model='additive', period=12)

            fig, axes = plt.subplots(5, 1, figsize=(16, 16), sharex=False)
            for ax in axes[:4]:
                ax.xaxis.set_major_locator(mdates.YearLocator())
                ax.xaxis.set_minor_locator(mdates.MonthLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                ax.tick_params(axis='x', rotation=45, labelsize=10)
                ax.grid(True, which='major', linestyle='--', linewidth=0.5)
                ax.grid(True, which='minor', linestyle=':', linewidth=0.3)

            axes[0].plot(result.observed, color='blue', label="Observed Returns")
            axes[0].set_ylabel("Monthly Return (%)", fontsize=12)
            axes[0].set_title(f"Observed {filename} (Monthly Returns)", fontsize=14)
            axes[0].legend()

            axes[1].plot(result.trend, color='green', label="Trend")
            axes[1].set_ylabel("Trend", fontsize=12)
            axes[1].set_title("Trend Component", fontsize=14)
            axes[1].legend()

            axes[2].plot(result.seasonal, color='orange', label="Seasonal")
            axes[2].set_ylabel("Seasonality", fontsize=12)
            axes[2].set_title("Seasonal Component (Annual Cycle Over Time)", fontsize=14)
            axes[2].legend()

            axes[3].plot(result.resid, color='gray', label="Residuals")
            axes[3].set_ylabel("Residuals", fontsize=12)
            axes[3].set_title("Residual Component", fontsize=14)
            axes[3].set_xlabel("Date (YYYY-MM)", fontsize=12)
            axes[3].legend()

            seasonal_df = result.seasonal.to_frame(name='seasonality')
            seasonal_df['month'] = seasonal_df.index.month
            avg_seasonality = seasonal_df.groupby('month').mean().reindex(np.arange(1,13))
            # Prepare month names
            month_names = list(calendar.month_abbr)[1:]

            # Plot average seasonal effect by month
            axes[4].bar(month_names, avg_seasonality['seasonality'], color='orange', edgecolor='black')
            axes[4].set_title("Average Seasonal Effect by Month", fontsize=14)
            axes[4].set_ylabel("Seasonal Impact (%)")
            axes[4].grid(True, linestyle='--', linewidth=0.4)

            plt.tight_layout()
            decomp_plot_path = os.path.join(output_dir, f"{filename[:-4]}_seasonal_decomposition.png")
            plt.savefig(decomp_plot_path, dpi=300)
            plt.close(fig)


            # Compute average monthly returns
            monthly_returns_df = monthly_returns.to_frame(name='returns')
            monthly_returns_df['month'] = monthly_returns_df.index.month
            avg_monthly_returns = monthly_returns_df.groupby('month').mean().reindex(np.arange(1,13))

            avg_monthly_returns.index = month_names
            avg_returns_csv_path = os.path.join(output_dir, f"{filename[:-4]}_avg_monthly_returns.csv")
            avg_monthly_returns.to_csv(avg_returns_csv_path, float_format="%.2f")
            
            # Create a new figure for average returns
            fig2, ax2 = plt.subplots(figsize=(12, 4))
            ax2.bar(month_names, avg_monthly_returns['returns'], color='skyblue', edgecolor='black')
            ax2.set_title("Average Monthly Returns by Month", fontsize=14)
            ax2.set_ylabel("Average Return (%)")
            ax2.grid(True, linestyle='--', linewidth=0.4)
            plt.tight_layout()
            # Save the average returns plot
            avg_returns_path = os.path.join(output_dir, f"{filename[:-4]}_avg_monthly_returns.png")
            plt.savefig(avg_returns_path, dpi=300)
            plt.close(fig2)

            avg_seasonality.index = month_names
            csv_path = os.path.join(output_dir, f"{filename[:-4]}_monthwise_returns_seasonality.csv")
            avg_seasonality.to_csv(csv_path, float_format="%.2f")
            print(f"Processed {filename}: return plots and CSV saved.")

            august_returns = monthly_returns_df[monthly_returns_df['month'] == 8]['returns']
            print("All August returns:")
            print(august_returns)
            print(f"Count: {len(august_returns)}, Mean: {august_returns.mean():.2f}, Median: {august_returns.median():.2f}")
            print(f"Negative count: {(august_returns < 0).sum()}, Positive count: {(august_returns > 0).sum()}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")