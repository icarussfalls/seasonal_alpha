import os
import pandas as pd

output_dir = "decomposition_outputs"
report_path = os.path.join(output_dir, "report.md")

with open(report_path, "w") as f:
    for base in sorted(set(fn.split('_')[0] for fn in os.listdir(output_dir) if fn.endswith('.csv'))):
        f.write(f"# {base}\n\n")
        # Plots
        decomp_img = f"{base}_seasonal_decomposition.png"
        avgret_img = f"{base}_avg_monthly_returns.png"
        if os.path.exists(os.path.join(output_dir, decomp_img)):
            f.write(f"![Decomposition Plot]({decomp_img})\n\n")
        if os.path.exists(os.path.join(output_dir, avgret_img)):
            f.write(f"![Average Monthly Returns]({avgret_img})\n\n")
        # Average Monthly Returns Table
        avgret_csv = f"{base}_avg_monthly_returns.csv"
        if os.path.exists(os.path.join(output_dir, avgret_csv)):
            df = pd.read_csv(os.path.join(output_dir, avgret_csv), index_col=0)
            f.write("## Average Monthly Returns\n")
            f.write(df.to_markdown())
            f.write("\n\n")
        # Seasonality Table
        seas_csv = f"{base}_monthwise_returns_seasonality.csv"
        if os.path.exists(os.path.join(output_dir, seas_csv)):
            df = pd.read_csv(os.path.join(output_dir, seas_csv), index_col=0)
            f.write("## Average Seasonality\n")
            f.write(df.to_markdown())
            f.write("\n\n")
        f.write("---\n\n")
print(f"Report generated at {report_path}")