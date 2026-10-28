# 🇬🇧 UK Job Market Analytics

### Python | Pandas | Data Analysis | Data Visualization | Streamlit

An end-to-end data analytics project exploring the UK Data Analyst job market using real job advertisement data collected through the Adzuna API.

The project demonstrates data collection, cleaning, exploratory data analysis (EDA), visualization, and interactive dashboard development.

## 📊 Project Overview

Understanding the job market is essential for identifying career opportunities, salary expectations, and hiring trends.

This project analyzes a small sample of UK Data Analyst job advertisements to explore:

* Salary distributions and estimated salary ranges
* Job opportunities across UK locations
* Employment and contract characteristics
* Companies advertising Data Analyst positions
* Differences between advertised salary estimates

**Important:** The current dataset is a small exploratory sample and does not represent the entire UK job market.

## 🎯 Project Objectives

1. Collect real UK job advertisements using an API.
2. Clean and prepare the collected data using Python.
3. Explore salary, location, and employment patterns.
4. Create informative data visualizations.
5. Build an interactive Streamlit dashboard.
6. Communicate findings and data limitations clearly.

## 🛠️ Technologies Used

| Technology    | Purpose                               |
| ------------- | ------------------------------------- |
| Python        | Data collection and analysis          |
| Pandas        | Data cleaning and manipulation        |
| NumPy         | Numerical operations                  |
| Requests      | API data collection                   |
| Matplotlib    | Data visualization                    |
| Seaborn       | Statistical visualization             |
| Plotly        | Interactive charts                    |
| Streamlit     | Interactive web dashboard             |
| Python-dotenv | Local environment variable management |
| Git & GitHub  | Version control                       |

## 📁 Project Structure

```text
UK_Job_Market_Analytics/
│
├── charts/
│   ├── salary_distribution.png
│   ├── jobs_by_location.png
│   ├── highest_paying_jobs.png
│   └── contract_analysis.png
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   ├── explore_jobs.py
│   ├── visualize_jobs.py
│   └── check_descriptions.py
│
├── data/
│   └── (Adzuna datasets excluded; synthetic demo CSV included)
│
├── collect_jobs.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🔄 Project Workflow

**Data Collection → Data Cleaning → Exploratory Analysis → Visualization → Interactive Dashboard**

### 1. Data Collection

Collected UK Data Analyst job advertisements using the Adzuna API.

The collected fields include job titles, companies, locations, salary estimates, and job descriptions.

### 2. Data Cleaning

Used Pandas to:

* Inspect missing values
* Check duplicate records
* Examine salary ranges
* Prepare data for analysis
* Identify advertisements that may not represent conventional employment opportunities

### 3. Exploratory Data Analysis

Explored salary distributions, job locations, companies, and employment characteristics.

### 4. Data Visualization

Created four visualizations:

* Salary Distribution
* Jobs by Location
* Highest-Paying Jobs
* Contract Analysis

### 5. Interactive Dashboard

Built a Streamlit dashboard with an Apple-inspired Liquid Glass visual design.

Dashboard features include:

* Overview metrics
* Salary analysis
* Location analysis
* Job explorer
* Interactive charts and filters

## 📈 Initial Findings

The current dashboard analyzes a filtered sample of **7 job advertisements** across **6 companies** and **6 locations**.

The observed median salary midpoint, excluding a flagged possible daily-rate contract, was approximately **£44,166**.

These findings describe only the collected sample. They should not be interpreted as representative UK-wide salary statistics.

## ⚠️ Data Limitations

* The API sample is small.
* Some salary values are estimates rather than confirmed employer offers.
* Job descriptions returned by the API were truncated, limiting reliable skills analysis.
* Some advertisements may represent training programmes rather than conventional jobs.
* Job postings can change or expire.

**Dataset availability:** Adzuna-derived CSV files are excluded from this public repository. Running the dashboard requires compatible local data files.

## 💻 Local Setup

### 1. Clone the repository

Clone this project using GitHub Desktop or Git.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API credentials

Create a local `.env` file containing your own Adzuna API credentials:

```env
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Never commit your `.env` file to GitHub.

### 4. Prepare local data

Use the collection and analysis scripts to prepare the required CSV files.

API usage is subject to your account's limits and the data provider's terms.

### 5. Run the dashboard

```bash
python -m streamlit run dashboard/app.py
```

**Note:** The collected Adzuna datasets are excluded from this repository. A public dashboard is available using fictional demonstration data. The hosted dashboard automatically loads the included synthetic dataset. Running the original Adzuna analysis locally requires the separately collected datasets.

## 🚀 Future Improvements

* Expand the dataset where permitted.
* Improve job advertisement classification.
* Explore more reliable skills-demand extraction.
* Add historical comparisons.
* Expand and improve the synthetic demonstration dataset.
* Improve automated data validation.

## 👨‍💻 About This Project

This portfolio project demonstrates practical skills in Python programming, API integration, data cleaning, exploratory analysis, visualization, and interactive dashboard development.

It was developed as part of a data analytics portfolio focused on real-world business and employment questions.

---

## Live Interactive Dashboard

**[Launch UK Job Market Analytics Dashboard](https://ukjobmarketanalytics-aglfyhkx9xdqhzkkzztujv.streamlit.app/)**

Explore the interactive dashboard featuring:

- Job market overview and summary metrics
- Salary analysis and visualisations
- Location-based job analysis
- Interactive job explorer
- Filters for exploring job listings
- Apple-inspired Liquid Glass interface

### Important: Demonstration Data

The publicly hosted dashboard uses **10 entirely synthetic job listings** created for educational and portfolio demonstration purposes.

All companies, vacancies and salary figures displayed in the hosted dashboard are fictional. They do not represent actual UK employment statistics.

The original analysis uses a separate, small sample of job advertisements collected through the Adzuna API. Those datasets and API credentials are not included in this public repository.
