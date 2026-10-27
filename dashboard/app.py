import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# UK JOB MARKET ANALYTICS
# APPLE-INSPIRED LIQUID GLASS DASHBOARD
# ============================================================

st.set_page_config(
    page_title="UK Job Market Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BLUE = "#007AFF"
PURPLE = "#AF52DE"
TEAL = "#30B0C7"
TEXT = "#1D1D1F"

# ============================================================
# LIQUID GLASS CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            ellipse at 10% 10%,
            rgba(179, 210, 255, 0.35),
            transparent 42%
        ),
        radial-gradient(
            ellipse at 90% 15%,
            rgba(220, 194, 255, 0.30),
            transparent 42%
        ),
        radial-gradient(
            ellipse at 55% 90%,
            rgba(177, 241, 232, 0.25),
            transparent 45%
        ),
        #F7F9FD;

    color: #1D1D1F;
}

[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-right: 1px solid rgba(255,255,255,0.8);
}

h1, h2, h3 {
    color: #1D1D1F !important;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 12px 35px rgba(70,100,150,0.08);
    min-height: 145px;
}

[data-testid="stMetricLabel"] {
    color: #6E6E73;
}

[data-testid="stMetricValue"] {
    color: #1D1D1F;
    font-weight: 750;
}

.glass-hero {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 30px;
    padding: 32px;
    margin-bottom: 22px;
    box-shadow: 0 15px 45px rgba(70,100,150,0.08);
}

.hero-eyebrow {
    color: #007AFF;
    font-size: 0.8rem;
    font-weight: 750;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero-title {
    color: #1D1D1F;
    font-size: 2.5rem;
    font-weight: 780;
    letter-spacing: -1px;
    line-height: 1.2;
    margin-bottom: 14px;
}

.hero-description {
    color: #6E6E73;
    font-size: 1rem;
    line-height: 1.7;
}

.glass-note {
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(210,222,240,0.75);
    border-radius: 18px;
    padding: 16px 20px;
    color: #626A79;
    margin-bottom: 22px;
}

.section-label {
    color: #007AFF;
    font-size: 0.82rem;
    font-weight: 750;
    letter-spacing: 1.5px;
    margin: 15px 0;
}

div.stDownloadButton > button {
    background: linear-gradient(135deg, #007AFF, #5E8BFF);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px 22px;
}

div.stDownloadButton > button:hover {
    color: white;
    background: #0066DD;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 14px;
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

REAL_DATA_FILE = PROJECT_DIR / "data" / "uk_jobs_employment_sample.csv"
DEMO_DATA_FILE = PROJECT_DIR / "data" / "uk_jobs_demo.csv"

if REAL_DATA_FILE.exists():
    DATA_FILE = REAL_DATA_FILE
    USING_DEMO_DATA = False
elif DEMO_DATA_FILE.exists():
    DATA_FILE = DEMO_DATA_FILE
    USING_DEMO_DATA = True
else:
    st.error("Dataset not found. Prepare local data or generate demo data.")
    st.stop()

if USING_DEMO_DATA:
    st.warning(
        "SYNTHETIC DEMO DATA: All displayed jobs and salaries are fictional. "
        "These are not real UK job market statistics."
    )


@st.cache_data
def load_data():

    data = pd.read_csv(DATA_FILE)

    for col in [
        "salary_min",
        "salary_max",
        "salary_midpoint"
    ]:
        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        )

    data["possible_day_rate_contract"] = (
        data["possible_day_rate_contract"]
        .astype(str)
        .str.lower()
        .eq("true")
    )

    for col in [
        "job_title",
        "company",
        "location"
    ]:
        data[col] = data[col].fillna("Unknown")

    return data


df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## UK Job Market")
    st.caption("ANALYTICS STUDIO")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Salary Analysis",
            "Location Analysis",
            "Job Explorer"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Filters")

    locations = sorted(
        df["location"].unique().tolist()
    )

    selected_location = st.selectbox(
        "Location",
        ["All Locations"] + locations
    )

    contract_filter = st.selectbox(
        "Daily-Rate Indicator",
        [
            "All Advertisements",
            "Daily-Rate Mentioned",
            "No Daily-Rate Detected"
        ]
    )

    search_query = st.text_input(
        "Search Job Titles",
        placeholder="e.g. Data Analyst"
    )

    st.divider()

    st.caption("DATA SOURCE")
    st.markdown("**Adzuna API**")
    st.caption("Research sample · 2026")

# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()

if selected_location != "All Locations":

    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]

if contract_filter == "Daily-Rate Mentioned":

    filtered_df = filtered_df[
        filtered_df["possible_day_rate_contract"]
    ]

elif contract_filter == "No Daily-Rate Detected":

    filtered_df = filtered_df[
        ~filtered_df["possible_day_rate_contract"]
    ]

if search_query.strip():

    filtered_df = filtered_df[
        filtered_df["job_title"].str.contains(
            search_query.strip(),
            case=False,
            regex=False,
            na=False
        )
    ]

salary_df = filtered_df[
    ~filtered_df["possible_day_rate_contract"]
].copy()

# ============================================================
# CHART THEME
# ============================================================

def glass_chart(fig, height=370):

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(255,255,255,0.72)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(
            family="Arial, sans-serif",
            color=TEXT,
            size=12
        ),
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        ),
        title_font=dict(
            size=17,
            color=TEXT
        ),
        showlegend=False
    )

    fig.update_xaxes(
        gridcolor="#E9EDF5",
        zerolinecolor="#E9EDF5"
    )

    fig.update_yaxes(
        gridcolor="#E9EDF5",
        zerolinecolor="#E9EDF5"
    )

    return fig

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="glass-hero">
    <div class="hero-eyebrow">
        DATA INTELLIGENCE · UNITED KINGDOM
    </div>
    <div class="hero-title">
        UK Job Market Analytics
    </div>
    <div class="hero-description">
        Discover salary patterns, explore locations,
        and analyse data-related job advertisements
        through an interactive analytics experience.
    </div>
</div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="glass-note">
    <strong>Research sample:</strong>
    These charts describe a small collection of advertisements,
    not the entire UK labour market.
    Salary figures may be estimates, and daily-rate
    classifications are preliminary.
</div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# KPI CARDS — FIXED TWO-COLUMN LAYOUT
# ============================================================

total_jobs = len(filtered_df)
total_companies = filtered_df["company"].nunique()
total_locations = filtered_df["location"].nunique()

median_salary = salary_df["salary_midpoint"].median()

median_display = (
    f"£{median_salary:,.0f}"
    if pd.notna(median_salary)
    else "N/A"
)

st.markdown(
    '<div class="section-label">FILTERED OVERVIEW</div>',
    unsafe_allow_html=True
)

# First row
col1, col2 = st.columns(2)

col1.metric("Job Ads", total_jobs)
col2.metric("Companies", total_companies)

# Second row
col3, col4 = st.columns(2)

col3.metric("Locations", total_locations)
col4.metric("Median Salary", median_display)

st.caption(
    "*Median of salary midpoints excluding advertisements "
    "flagged as daily-rate contracts. Other figures may "
    "still be estimated or non-comparable."
)

st.write("")

# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="section-label">MARKET OVERVIEW</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        if not salary_df.empty:

            fig = px.histogram(
                salary_df,
                x="salary_midpoint",
                nbins=6,
                title="Salary Distribution",
                color_discrete_sequence=[BLUE],
                labels={
                    "salary_midpoint": "Salary Midpoint (£)"
                }
            )

            fig = glass_chart(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info("No salary data matches these filters.")

    with right:

        if not filtered_df.empty:

            counts = (
                filtered_df["location"]
                .value_counts()
                .reset_index()
            )

            counts.columns = [
                "Location",
                "Advertisements"
            ]

            fig = px.bar(
                counts,
                x="Advertisements",
                y="Location",
                orientation="h",
                title="Advertisements by Location",
                color_discrete_sequence=[TEAL]
            )

            fig = glass_chart(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info("No location data matches these filters.")

    st.markdown(
        '<div class="section-label">CONTRACT INDICATORS</div>',
        unsafe_allow_html=True
    )

    if not filtered_df.empty:

        counts = (
            filtered_df["possible_day_rate_contract"]
            .map({
                True: "Daily-Rate Mentioned",
                False: "No Daily-Rate Detected"
            })
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Classification",
            "Advertisements"
        ]

        fig = px.pie(
            counts,
            names="Classification",
            values="Advertisements",
            hole=0.65,
            title="Daily-Rate Contract Indicators",
            color_discrete_sequence=[
                BLUE,
                PURPLE
            ]
        )

        fig = glass_chart(
            fig,
            height=350
        )

        fig.update_layout(
            showlegend=True
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    else:

        st.info("No advertisements match these filters.")

# ============================================================
# SALARY ANALYSIS PAGE
# ============================================================

elif page == "Salary Analysis":

    st.subheader("Salary Intelligence")

    if not salary_df.empty:

        fig = px.box(
            salary_df,
            x="salary_midpoint",
            title="Salary Midpoint Distribution",
            color_discrete_sequence=[BLUE]
        )

        fig = glass_chart(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )

        top_jobs = (
            salary_df
            .sort_values(
                "salary_midpoint",
                ascending=False
            )
            .head(10)
            .copy()
        )

        top_jobs["Job"] = (
            top_jobs["job_title"]
            + " — "
            + top_jobs["company"]
        )

        fig = px.bar(
            top_jobs,
            x="salary_midpoint",
            y="Job",
            orientation="h",
            title="Highest Salary Midpoints",
            color_discrete_sequence=[TEAL],
            labels={
                "salary_midpoint": "Salary Midpoint (£)"
            }
        )

        fig = glass_chart(
            fig,
            height=450
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    else:

        st.info("No salary records match your filters.")

# ============================================================
# LOCATION ANALYSIS PAGE
# ============================================================

elif page == "Location Analysis":

    st.subheader("Geographic Distribution")

    if not filtered_df.empty:

        counts = (
            filtered_df["location"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Location",
            "Advertisements"
        ]

        fig = px.bar(
            counts,
            x="Advertisements",
            y="Location",
            orientation="h",
            title="Advertisements by Location",
            color_discrete_sequence=[BLUE]
        )

        fig = glass_chart(
            fig,
            height=450
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.dataframe(
            counts,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No location records match your filters.")

# ============================================================
# JOB EXPLORER PAGE
# ============================================================

elif page == "Job Explorer":

    st.subheader("Explore Job Advertisements")

    columns = [
        "job_title",
        "company",
        "location",
        "salary_min",
        "salary_max",
        "salary_midpoint",
        "created",
        "job_url"
    ]

    st.dataframe(
        filtered_df[columns],
        width="stretch",
        hide_index=True,
        column_config={
            "job_title": "Job Title",
            "company": "Company",
            "location": "Location",
            "salary_min": st.column_config.NumberColumn(
                "Salary Min",
                format="£%.0f"
            ),
            "salary_max": st.column_config.NumberColumn(
                "Salary Max",
                format="£%.0f"
            ),
            "salary_midpoint": st.column_config.NumberColumn(
                "Salary Midpoint",
                format="£%.0f"
            ),
            "created": "Posted",
            "job_url": st.column_config.LinkColumn(
                "Job Link",
                display_text="View Job"
            )
        }
    )

    csv = filtered_df[columns].to_csv(
        index=False
    )

    st.download_button(
        "Download Filtered Jobs",
        data=csv,
        file_name="uk_jobs_filtered.csv",
        mime="text/csv"
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "UK Job Market Analytics · Python · Pandas · "
    "Plotly · Streamlit"
)

st.caption(
    "Three advertisements flagged as possible fee-based "
    "training programmes were excluded. Classification "
    "is rule-based and requires manual verification."
)

st.caption(
    "Technical skill-demand charts are unavailable because "
    "the saved descriptions contain only 500 characters."
)