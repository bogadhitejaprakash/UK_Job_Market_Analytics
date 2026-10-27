import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# UK JOB MARKET ANALYTICS
# DATA VISUALISATION
# ==========================================

# STEP 1: PROJECT PATHS

project_folder = Path(__file__).resolve().parent.parent

input_path = project_folder / "data" / "uk_jobs_cleaned.csv"

charts_folder = project_folder / "charts"
charts_folder.mkdir(exist_ok=True)

# STEP 2: LOAD DATA

df = pd.read_csv(input_path)

print("\n===================================")
print("     UK JOB MARKET VISUALISATION")
print("===================================")

print("\nTotal Advertisements:", len(df))

# STEP 3: FLAG FEE-BASED TRAINING PROGRAMMES

training_pattern = (
    r"self-funded|fees apply|training programme|"
    r"job programme|placement programme"
)

df["possible_training_programme"] = (
    df["job_title"].fillna("").str.contains(
        training_pattern, case=False, regex=True
    )
    |
    df["description"].fillna("").str.contains(
        training_pattern, case=False, regex=True
    )
)

print(
    "\nPossible Training Programmes:",
    df["possible_training_programme"].sum()
)

# Exclude flagged programmes from employment charts
jobs_df = df[
    ~df["possible_training_programme"]
].copy()

print("Advertisements Remaining:", len(jobs_df))

# STEP 4: IDENTIFY POSSIBLE DAILY-RATE CONTRACTS

if "possible_day_rate_contract" not in jobs_df.columns:

    jobs_df["possible_day_rate_contract"] = (
        jobs_df["description"].fillna("").str.contains(
            r"£\s?[\d,]+\s*[-–]\s*£?\s?[\d,]+"
            r"\s*(?:per day|/day|pd\b)|"
            r"£\s?[\d,]+\s*(?:per day|/day|pd\b)",
            case=False,
            regex=True
        )
    )

else:

    jobs_df["possible_day_rate_contract"] = (
        jobs_df["possible_day_rate_contract"]
        .astype(str)
        .str.lower()
        .eq("true")
    )

# Exclude identified daily-rate contracts from
# annual salary comparisons
salary_df = jobs_df[
    ~jobs_df["possible_day_rate_contract"]
].copy()

sns.set_theme(style="whitegrid")

# ==========================================
# CHART 1: SALARY DISTRIBUTION
# ==========================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=salary_df,
    x="salary_midpoint",
    bins=6,
    kde=False
)

plt.title("Salary Distribution - Sample of UK Job Advertisements")
plt.xlabel("Salary Midpoint (£)")
plt.ylabel("Number of Advertisements")

plt.tight_layout()

plt.savefig(
    charts_folder / "salary_distribution.png",
    dpi=300
)

plt.close()

print("\nChart 1 saved: salary_distribution.png")

# ==========================================
# CHART 2: JOBS BY LOCATION
# ==========================================

location_counts = (
    jobs_df["location"]
    .fillna("Unknown")
    .value_counts()
    .head(10)
)

plt.figure(figsize=(11, 6))

sns.barplot(
    x=location_counts.values,
    y=location_counts.index
)

plt.title("Job Advertisements by Location")
plt.xlabel("Number of Advertisements")
plt.ylabel("Location")

plt.tight_layout()

plt.savefig(
    charts_folder / "jobs_by_location.png",
    dpi=300
)

plt.close()

print("Chart 2 saved: jobs_by_location.png")

# ==========================================
# CHART 3: HIGHEST-PAYING ADVERTISEMENTS
# ==========================================

top_jobs = (
    salary_df
    .sort_values("salary_midpoint", ascending=False)
    .head(10)
    .copy()
)

top_jobs["job_label"] = (
    top_jobs["job_title"].astype(str)
    + " | "
    + top_jobs["company"].astype(str)
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_jobs,
    x="salary_midpoint",
    y="job_label"
)

plt.title("Highest Salary Midpoints - Excluding Flagged Daily-Rate Contracts")
plt.xlabel("Salary Midpoint (£)")
plt.ylabel("Job Advertisement")

plt.tight_layout()

plt.savefig(
    charts_folder / "highest_paying_jobs.png",
    dpi=300
)

plt.close()

print("Chart 3 saved: highest_paying_jobs.png")

# ==========================================
# CHART 4: CONTRACT CLASSIFICATION
# ==========================================

contract_counts = (
    jobs_df["possible_day_rate_contract"]
    .map({
        True: "Daily-Rate Mentioned",
        False: "No Daily-Rate Detected"
    })
    .value_counts()
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=contract_counts.index,
    y=contract_counts.values
)

plt.title("Daily-Rate Mentions in Job Advertisements")
plt.xlabel("Classification")
plt.ylabel("Number of Advertisements")

plt.tight_layout()

plt.savefig(
    charts_folder / "contract_analysis.png",
    dpi=300
)

plt.close()

print("Chart 4 saved: contract_analysis.png")

# ==========================================
# STEP 5: SAVE ANALYSIS DATA
# ==========================================

jobs_df.to_csv(
    project_folder / "data" / "uk_jobs_employment_sample.csv",
    index=False
)

print("\n===================================")
print("     VISUALISATION COMPLETED")
print("===================================")

print("\nCharts saved in:", charts_folder)
print("Employment sample saved successfully!")

print("\nIMPORTANT:")
print("- Results are based on a small sample.")
print("- Training programme detection is rule-based.")
print("- Contract detection is not exhaustive.")
print("- Salary values may include estimates.")
print("- Skill demand cannot be reliably measured")
print("  using the truncated descriptions.")