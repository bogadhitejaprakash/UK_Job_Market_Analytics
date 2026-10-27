import os
import requests
import pandas as pd
from dotenv import load_dotenv

# STEP 1: Load API credentials
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

if not APP_ID or not APP_KEY:
    raise ValueError("Missing Adzuna credentials. Check your .env file.")

print("UK Job Market Analytics")
print("Connecting to Adzuna API...\n")

# STEP 2: API endpoint
url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

# STEP 3: Search parameters
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 10,
    "what": "Data Analyst",
    "content-type": "application/json"
}

# STEP 4: Request job advertisements
try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

except requests.RequestException as error:
    print("API request failed:", error)
    raise SystemExit(1)

# STEP 5: Extract useful information
jobs = []

for job in data.get("results", []):
    jobs.append({
        "job_id": job.get("id"),
        "job_title": job.get("title"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "description": job.get("description"),
        "created": job.get("created"),
        "job_url": job.get("redirect_url")
    })

# STEP 6: Convert to a DataFrame
df = pd.DataFrame(jobs)

# STEP 7: Save the dataset
os.makedirs("data", exist_ok=True)

file_path = "data/uk_data_analyst_jobs.csv"

df.to_csv(file_path, index=False)

print(f"Successfully collected {len(df)} jobs!")
print(f"Dataset saved to: {file_path}")

# STEP 8: Display sample data
print("\nFirst 5 jobs:")

if not df.empty:
    print(df[["job_title", "company", "location", "salary_min", "salary_max"]].head())
else:
    print("No jobs returned.")