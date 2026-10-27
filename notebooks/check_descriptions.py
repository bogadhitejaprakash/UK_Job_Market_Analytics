import pandas as pd
from pathlib import Path

# Project folder
project_folder = Path(__file__).resolve().parent.parent

# Load original dataset
file_path = project_folder / "data" / "uk_data_analyst_jobs.csv"

df = pd.read_csv(file_path)

print("\n===================================")
print("     JOB DESCRIPTION ANALYSIS")
print("===================================")

print("\nTotal Jobs:", len(df))

# Check description lengths
df["description_length"] = (
    df["description"]
    .fillna("")
    .str.len()
)

print("\n--- DESCRIPTION LENGTH STATISTICS ---")
print(df["description_length"].describe())

# Display descriptions
for index, row in df.iterrows():

    print("\n" + "=" * 60)
    print("JOB", index + 1)
    print("=" * 60)

    print("Title:", row["job_title"])
    print("Company:", row["company"])

    print("\nDescription:")
    print(row["description"])

    print("\nCharacter Count:", row["description_length"])

print("\n===================================")
print("     DIAGNOSTIC COMPLETED")
print("===================================")