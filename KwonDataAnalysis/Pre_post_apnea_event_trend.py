import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the new dataset
file_path = "/mnt/data/Apnea_event_data_v6.xlxs.xlsx"

# Read the Excel file
xls = pd.ExcelFile(file_path)

# Load the data from the first sheet
df = pd.read_excel(xls, sheet_name="Sheet1")

# Convert time column to datetime format for proper visualization
df["Time(in seconds)"] = pd.to_datetime(df["Time(in seconds)"])

# Create a scatter plot using the updated dataset
plt.figure(figsize=(8, 5))

# Plot Systolic Blood Pressure during the event
plt.scatter(df["Time(in seconds)"], df["Systolic"], 
            color='b', alpha=0.7, label="Systolic Blood Pressure During Event")

# Plot Avg Systolic Blood Pressure in the 60 seconds before event
plt.scatter(df["Time(in seconds)"], df["avg_systolic_last_60s"], 
            color='r', alpha=0.7, label="Avg Systolic Blood Pressure (Last 60s Before Event)")

# Format x-axis to show only HH:MM:SS
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

# Labels and title
plt.xlabel("Time (HH:MM:SS)")
plt.ylabel("Systolic Blood Pressure (mmHg)")
plt.title("Average Systolic Blood Pressure for the Last 60 Seconds Before the Event of Obstructive Apnea\n"
          "vs. Systolic Blood Pressure During the Event")

# Updated legend
plt.legend()
plt.grid(True)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show plot
plt.show()