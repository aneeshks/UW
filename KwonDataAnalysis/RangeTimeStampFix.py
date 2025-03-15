import pandas as pd
from datetime import datetime, timedelta

# Load input data from CSV
df = pd.read_csv("/Users/ebenezer/Documents/SleepApnea/Test/Sys_source.csv", delimiter="\t")

df.columns = df.columns.str.strip()

df["Time"] = df["Time"].astype(str).str.split('.').str[0]

df["Time"] = pd.to_datetime(df["Time"], format='%d/%m/%Y %H:%M:%S')


print(df["Time"].min(), "Min Time")
print(df["Time"].max(), "Max Time")

time_diff_seconds = (df["Time"].max() - df["Time"].min()).total_seconds()
print(time_diff_seconds, "Seconds between min and max time")



import pandas as pd
from datetime import timedelta


# Load input data from CSV
df = pd.read_csv("/Users/ebenezer/Documents/SleepApnea/Test/testRange", delimiter="\t")

df.columns = df.columns.str.strip()

df["start"] = df["start"].astype(str).str.split('.').str[0]
df["end"] = df["end"].astype(str).str.split('.').str[0]

df["start"] = pd.to_datetime(df["start"], format='%d/%m/%Y %H:%M:%S')
df["end"] = pd.to_datetime(df["end"], format='%d/%m/%Y %H:%M:%S')

# Define specific start and end times for expansion
specified_start = pd.to_datetime("2025-03-03 23:57:00", format='%Y-%m-%d %H:%M:%S')
specified_end = pd.to_datetime("2025-03-04 06:33:59", format='%Y-%m-%d %H:%M:%S')

print(specified_start, "specified_start")
print(specified_end, "specified_end")

df.head(3)

time_diff_seconds = (specified_end - specified_start).total_seconds()
print(time_diff_seconds, "Seconds between min and max time")


#---


# Assuming df is already loaded with necessary data
expanded_rows = []
total_rows_processed = 0  # Counter for processed rows
Rng_int = 0 

# Iterate over the full range of time from specified_start to specified_end
current_time = specified_start

while current_time <= specified_end:
    # Find matching rows where the current time is within a start-end range
    matching_row = df[(df["start"] <= current_time) & (df["end"] >= current_time)]
    Rng_int += 1
    if Rng_int % 300 == 0:
        print(Rng_int, "Rng_int")

    if not matching_row.empty:
        # If there's a match, get the corresponding row
        row = matching_row.iloc[0]
        expanded_rows.append({
            "Timestamp": current_time,
            "Value": row["Value"],
            "Event": row["event"],
            "sleep_stage": row["sleep_stage"]
        })
    else:
        # If no match, fill with default/empty values
        expanded_rows.append({
            "Timestamp": current_time,
            "Value": "",
            "Event": "",
            "sleep_stage": ""
        })
    
    # Print the range being processed (start and end)
#    print(f"Processing range: {row['start']} to {row['end']}" if not matching_row.empty else f"Processing timestamp: {current_time}")
    
    # Increment counters and move to the next second
    total_rows_processed += 1
    current_time += timedelta(seconds=1)  # Increment by 1 second

# Create expanded DataFrame
expanded_df = pd.DataFrame(expanded_rows)

# Save output to CSV
output_file = "/Users/ebenezer/Documents/SleepApnea/Test/output12.csv"
expanded_df.to_csv(output_file, index=False, na_rep="None")  # Ensures None is explicitly written as "None"

# Display result summary
print(f"Expanded data saved to {output_file}")
print(f"Total rows processed: {total_rows_processed}")
