import pandas as pd
import re
from pathlib import Path

# =====================================================
# UK JOB MARKET ANALYTICS
# COMPLETE DATA ANALYSIS SCRIPT
# =====================================================

# STEP 1: PROJECT PATHS

project_folder = Path(__file__).resolve().parent.parent

input_path = project_folder / "data" / "uk_data_analyst_jobs.csv"
output_path = project_folder / "data" / "uk_jobs_cleaned.csv"
skills_output = project_folder / "data" / "uk_skills_demand.csv"

# STEP 2: LOAD DATASET

df = pd.read_csv(input_path)

print("\n====================================")
print("       UK JOB MARKET ANALYTICS")
print("====================================")

print("\nTotal Jobs:", len(df))

print("\nDataset Columns:")
print(df.columns.tolist())

print("\nFirst 5 Jobs:")
print(df.head())

# STEP 3: DATA QUALITY CHECKS

print("\n--- DATA QUALITY CHECKS ---")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Job IDs:")
print(df["job_id"].duplicated().sum())

# STEP 4: CLEAN DATASET

clean_df = df.copy()

# Remove duplicate advertisements
clean_df = clean_df.drop_duplicates(
    subset=["job_id"]
).copy()

# Convert salary columns to numeric
clean_df["salary_min"] = pd.to_numeric(
    clean_df["salary_min"],
    errors="coerce"
)

clean_df["salary_max"] = pd.to_numeric(
    clean_df["salary_max"],
    errors="coerce"
)

# Remove invalid salary ranges
clean_df = clean_df[
    clean_df["salary_min"].notna()
    & clean_df["salary_max"].notna()
    & (clean_df["salary_min"] <= clean_df["salary_max"])
].copy()

# Calculate salary midpoint
clean_df["salary_midpoint"] = (
    clean_df["salary_min"] + clean_df["salary_max"]
) / 2

# Convert posting dates
clean_df["created"] = pd.to_datetime(
    clean_df["created"],
    errors="coerce",
    utc=True
)

clean_df = clean_df.dropna(
    subset=["created"]
).copy()

clean_df["created"] = clean_df["created"].dt.strftime(
    "%Y-%m-%d"
)

print("\n--- CLEANED DATASET ---")
print("Original Jobs:", len(df))
print("Cleaned Jobs:", len(clean_df))

# STEP 5: SALARY ANALYSIS

print("\n--- SALARY ANALYSIS ---")

print(
    clean_df[
        ["salary_min", "salary_max", "salary_midpoint"]
    ].describe().round(2)
)

# STEP 6: HIGHEST-PAYING JOB

print("\n--- HIGHEST PAYING JOB ---")

if not clean_df.empty:

    highest_job = clean_df.loc[
        clean_df["salary_midpoint"].idxmax()
    ]

    print("Job Title:", highest_job["job_title"])
    print("Company:", highest_job["company"])
    print("Location:", highest_job["location"])
    print("Salary Midpoint: £", highest_job["salary_midpoint"])

# STEP 7: IDENTIFY POSSIBLE DAILY-RATE CONTRACTS

print("\n--- CONTRACT JOB ANALYSIS ---")

day_rate_pattern = (
    r"£\s?[\d,]+\s*[-–]\s*£?\s?[\d,]+"
    r"\s*(?:per day|/day|pd\b)|"
    r"£\s?[\d,]+\s*(?:per day|/day|pd\b)"
)

clean_df["possible_day_rate_contract"] = (
    clean_df["description"]
    .fillna("")
    .str.contains(
        day_rate_pattern,
        case=False,
        regex=True
    )
)

print("\nPossible Daily-Rate Contract Jobs:")
print(
    clean_df["possible_day_rate_contract"].value_counts()
)

# STEP 8: TECHNICAL SKILLS EXTRACTION

print("\n--- TECHNICAL SKILLS ANALYSIS ---")

skills = {
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Excel": r"\bexcel\b",
    "Power BI": r"\bpower\s*bi\b",
    "Tableau": r"\btableau\b",
    "R": r"\bR\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "Machine Learning": r"\bmachine learning\b",
    "Azure": r"\bazure\b",
    "AWS": r"\baws\b",
    "Spark": r"\bspark\b"
}

skill_counts = {}

for skill, pattern in skills.items():

    # Match against the original description text
    matches = clean_df["description"].fillna("").str.contains(
        pattern,
        case=False if skill != "R" else True,
        regex=True
    )

    # Add a True/False column for each skill
    column_name = (
        "skill_"
        + skill.lower().replace(" ", "_")
    )

    clean_df[column_name] = matches

    # Count advertisements mentioning each skill
    skill_counts[skill] = int(matches.sum())

# STEP 9: CREATE SKILL DEMAND DATASET

skills_df = pd.DataFrame(
    list(skill_counts.items()),
    columns=["skill", "job_count"]
)

skills_df = skills_df.sort_values(
    by="job_count",
    ascending=False
)

skills_df["percentage"] = (
    skills_df["job_count"] / len(clean_df) * 100
    if len(clean_df) > 0
    else 0
)

print("\nUK Technical Skills Demand:")
print(skills_df.to_string(index=False))

# STEP 10: SAVE RESULTS

clean_df.to_csv(
    output_path,
    index=False
)

skills_df.to_csv(
    skills_output,
    index=False
)

print("\n--- FILES SAVED SUCCESSFULLY ---")

print("Cleaned Dataset:", output_path)
print("Skills Analysis:", skills_output)

print("\n====================================")
print("      ANALYSIS COMPLETED")
print("====================================")