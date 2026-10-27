from pathlib import Path
import pandas as pd

# Fictional data for portfolio demonstration only.
# Not sourced from Adzuna or real job advertisements.

PROJECT_DIR = Path(__file__).resolve().parent

jobs = [
    ("Junior Data Analyst", "Demo Analytics Ltd", "London", 28000, 35000),
    ("Data Analyst", "Sample Insights Ltd", "Manchester", 32000, 42000),
    ("Business Data Analyst", "Example Digital Ltd", "Birmingham", 35000, 48000),
    ("Reporting Analyst", "Demo Reporting Ltd", "Leicester", 27000, 36000),
    ("SQL Data Analyst", "Sample Technology Ltd", "Bristol", 38000, 50000),
    ("Power BI Analyst", "Example Solutions Ltd", "Leeds", 33000, 45000),
    ("Senior Data Analyst", "Demo Intelligence Ltd", "London", 50000, 68000),
    ("Data Insights Analyst", "Sample Research Ltd", "Nottingham", 30000, 41000),
    ("Operations Analyst", "Example Operations Ltd", "Liverpool", 29000, 39000),
    ("Analytics Specialist", "Demo Data Group Ltd", "Edinburgh", 42000, 56000),
]

rows = []

for i, (title, company, location, salary_min, salary_max) in enumerate(jobs, 1):
    rows.append({
        "job_id": f"DEMO-{i:03d}",
        "job_title": title,
        "company": company,
        "location": location,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "description": (
            "Synthetic job advertisement created for dashboard "
            "demonstration. This is not a real vacancy."
        ),
        "created": "2026-10-01",
        "job_url": "",
        "salary_midpoint": (salary_min + salary_max) / 2,
        "possible_day_rate_contract": False,
        "skill_python": False,
        "skill_sql": False,
        "skill_excel": False,
        "skill_power_bi": False,
        "skill_tableau": False,
        "skill_r": False,
        "skill_pandas": False,
        "skill_numpy": False,
        "skill_machine_learning": False,
        "skill_azure": False,
        "skill_aws": False,
        "skill_spark": False,
        "possible_training_programme": False,
    })

df = pd.DataFrame(rows)

output = PROJECT_DIR / "data" / "uk_jobs_demo.csv"
output.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output, index=False)

print(f"Created {len(df)} synthetic job listings.")
print(f"Saved to: {output}")