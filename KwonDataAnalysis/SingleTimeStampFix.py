import pandas as pd

def process_time_series(input_csv, output_csv):
    # Read the tab-delimited CSV file
    df = pd.read_csv(input_csv, delimiter="\t")

    print("Columns in CSV:", df.columns)

    df.columns = df.columns.str.strip()

    df["Time"] = df["Time"].astype(str).str.split('.').str[0]

    df = df.sort_values(by="Time")

    # Get the min and max of the Time column (still strings)
    min_time = df["Time"].min()
    max_time = df["Time"].max()

    # Filter dataset within the min and max timestamps
    df_filtered = df[(df["Time"] >= min_time) & (df["Time"] <= max_time)].copy()

    # Convert "Value" column to numeric, forcing errors to NaN
    df_filtered["Value"] = pd.to_numeric(df_filtered["Value"], errors="coerce")

    # Forward fill NaN values in the "Value" column
    df_filtered["Value"] = df_filtered["Value"].ffill()

    # Group by Time and calculate the average of 'Value' for each unique timestamp
    df_avg = df_filtered.groupby("Time", as_index=False)["Value"].mean()

    # Count duplicate values per timestamp
    df_counts = df_filtered.groupby("Time").size().reset_index(name="Duplicate Count")

    # Create a full range of time values (ensuring continuity)
    time_range = pd.date_range(start=min_time, end=max_time, freq='s').strftime("%d/%m/%Y %H:%M:%S")
    df_full = pd.DataFrame({"Time": time_range})

    # Merge with the average values and duplicate counts
    df_merged = df_full.merge(df_avg, on="Time", how="left").merge(df_counts, on="Time", how="left")

    # Forward fill missing values in 'Value' column
    df_merged["Value"] = df_merged["Value"].ffill()

    # Fill NaN in 'Duplicate Count' column with 0
    df_merged["Duplicate Count"] = df_merged["Duplicate Count"].fillna(0)

    print("Data after filling missing values after merge:")
    print(df_merged)

    # Write to output CSV
    df_merged.to_csv(output_csv, index=False)

# Example usage
process_time_series(
    "/Users/ebenezer/Documents/Project1/TimeValueTestData", 
    "/Users/ebenezer/Documents/Project1/TimeValueTestData_output5.csv"
)
