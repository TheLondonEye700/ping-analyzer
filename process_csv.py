import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

csv_file_path = "./output.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)
fig, (min_ax, avg_ax, max_ax) = plt.subplots(3, 1, figsize=(15, 12))
loc = plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals

min_ax.plot(df["low_min"], label="Low PCP min RTT", marker="o")
min_ax.plot(df["high_min"], label="High PCP min RTT", marker="o")

min_ax.set_xlabel("Ping")
min_ax.set_ylabel("Min RTT (ms)")
min_ax.set_title("Minimum RTT over ping")
min_ax.xaxis.set_major_locator(loc)
min_ax.legend()

# AVG
avg_ax.plot(df["low_avg"], label="Low PCP avg RTT", marker="o")
avg_ax.plot(df["high_avg"], label="High PCP avg RTT", marker="o")

avg_ax.set_xlabel("Ping")
avg_ax.set_ylabel("Avg RTT (ms)")
avg_ax.set_title("Average RTT over ping")
avg_ax.xaxis.set_major_locator(loc)
avg_ax.legend()

max_ax.plot(df["low_max"], label="Low PCP max RTT", marker="o")
max_ax.plot(df["high_max"], label="High PCP max RTT", marker="o")

max_ax.set_xlabel("Ping")
max_ax.set_ylabel("Max RTT (ms)")
max_ax.set_title("Max RTT over ping")
max_ax.xaxis.set_major_locator(loc)
max_ax.legend()

plt.tight_layout()
plt.show()
