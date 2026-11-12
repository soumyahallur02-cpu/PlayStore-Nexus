
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="PlayStore Nexus | App Intelligence",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. PREMIUM CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Import font */
@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);

/* Main background */
.stApp {
    background:
    radial-gradient(circle at 10% 10%,
    rgba(126,87,255,0.13), transparent 30%),
    radial-gradient(circle at 90% 20%,
    rgba(236,72,153,0.10), transparent 28%),
    #090D1C;

    font-family: 'Inter', sans-serif;
    color: #F8FAFC;
}

/* Main content */
.block-container {
    max-width: 1550px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

/* Hide default header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #11182B,
        #0C1121
    );
    border-right: 1px solid #293451;
}

/* Text */
h1, h2, h3, h4 {
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}

p, label, li {
    color: #C3CBE0;
}

/* Hero banner */
.hero {
    position: relative;
    overflow: hidden;
    padding: 36px;
    border-radius: 24px;
    background: linear-gradient(
        120deg,
        #28215E 0%,
        #5030A6 48%,
        #A02B76 100%
    );
    border: 1px solid rgba(255,255,255,0.16);
    box-shadow: 0 15px 45px rgba(83,47,180,0.20);
    margin-bottom: 24px;
}

.hero::after {
    content: "✦";
    position: absolute;
    font-size: 170px;
    color: rgba(255,255,255,0.08);
    right: 35px;
    top: -35px;
}

.hero-label {
    color: #DDD6FE;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero-title {
    color: white;
    font-size: clamp(27px, 4vw, 43px);
    font-weight: 900;
    margin: 12px 0;
    letter-spacing: -1.5px;
}

.hero-description {
    color: #E9D5FF;
    font-size: 14px;
    line-height: 1.8;
    max-width: 700px;
}

.hero-footer {
    color: #F5D0FE;
    font-size: 11px;
    letter-spacing: 1.5px;
    margin-top: 22px;
}

/* Section headers */
.section-heading {
    font-size: 21px;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: 28px;
    margin-bottom: 5px;
}

.section-subtitle {
    font-size: 12px;
    color: #8996B5;
    margin-bottom: 20px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #1A2440,
        #11182D
    );
    border: 1px solid #344365;
    border-radius: 18px;
    padding: 19px;
    min-height: 120px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.18);
    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: #A78BFA;
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(139,92,246,0.15);
}

div[data-testid="stMetricLabel"] {
    color: #A5B4D0 !important;
    font-size: 12px !important;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 26px !important;
    font-weight: 800 !important;
}

/* Plotly charts */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    padding: 10px;
    border-radius: 18px;
    border: 1px solid #DCE1ED;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

/* Tables */
div[data-testid="stDataFrame"] {
    border: 1px solid #33415E;
    border-radius: 15px;
    overflow: hidden;
}

/* Selectbox */
div[data-baseweb="select"] {
    background: #18223A;
    border-radius: 10px;
}

/* Multiselect */
span[data-baseweb="tag"] {
    background: #7043BC !important;
}

/* Buttons */
.stDownloadButton button,
.stButton button {
    background: linear-gradient(
        100deg,
        #7545E8,
        #D946A6
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    transition: 0.2s;
}

.stDownloadButton button:hover,
.stButton button:hover {
    box-shadow: 0 5px 22px rgba(217,70,166,0.35);
    transform: translateY(-2px);
}

/* Sidebar labels */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 13px;
}

/* Divider */
hr {
    border-color: #2B3652 !important;
}

/* Captions */
.stCaption {
    color: #8D9BB8 !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 22px;
    margin-top: 35px;
    border-top: 1px solid #28334F;
    color: #8290AD;
    font-size: 11px;
    letter-spacing: 1px;
}

/* Status pill */
.status-pill {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 30px;
    background: rgba(52,211,153,0.12);
    color: #6EE7B7;
    border: 1px solid rgba(52,211,153,0.35);
    font-size: 11px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. FILE PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

PLAYSTORE_FILE = BASE_DIR / "Play Store Data(3).csv"
REVIEWS_FILE = BASE_DIR / "User Reviews(3).csv"


# ==========================================================
# 4. CATEGORY TRANSLATIONS
# ==========================================================

CATEGORY_TRANSLATIONS = {
    "GAME": "Game",
    "BEAUTY": "सौंदर्य",
    "BUSINESS": "வணிகம்",
    "COMICS": "Comics",
    "COMMUNICATION": "Communication",
    "DATING": "Partnersuche",
    "ENTERTAINMENT": "Entertainment",
    "SOCIAL": "Social",
    "EVENTS": "Events"
}

CATEGORY_ORDER = list(CATEGORY_TRANSLATIONS.values())

COLOR_MAP = {
    "Game": "#FF69B4",
    "सौंदर्य": "#38BDF8",
    "வணிகம்": "#34D399",
    "Comics": "#FBBF24",
    "Communication": "#A78BFA",
    "Partnersuche": "#FB7185",
    "Entertainment": "#22D3EE",
    "Social": "#A3E635",
    "Events": "#F97316"
}


# ==========================================================
# 5. DATA CLEANING
# ==========================================================

def convert_size(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if value.lower() == "varies with device":
        return np.nan

    match = re.search(
        r"([\d.]+)\s*([KMG]?)",
        value,
        re.IGNORECASE
    )

    if not match:
        return np.nan

    number = float(match.group(1))
    unit = match.group(2).upper()

    if unit == "K":
        return number / 1024

    if unit == "G":
        return number * 1024

    return number


def convert_installs(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    value = value.replace(",", "").replace("+", "")

    try:
        return float(value)
    except ValueError:
        return np.nan


# ==========================================================
# 6. LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    apps = pd.read_csv(PLAYSTORE_FILE)

    reviews = pd.read_csv(REVIEWS_FILE)

    return apps, reviews


# ==========================================================
# 7. DATA PROCESSING
# ==========================================================

@st.cache_data
def process_data(apps, reviews):

    apps = apps.copy()
    reviews = reviews.copy()

    apps["App"] = apps["App"].astype(str).str.strip()
    reviews["App"] = reviews["App"].astype(str).str.strip()

    apps["Category"] = (
        apps["Category"].astype(str).str.upper().str.strip()
    )

    apps["Rating"] = pd.to_numeric(
        apps["Rating"], errors="coerce"
    )

    apps["Reviews"] = pd.to_numeric(
        apps["Reviews"], errors="coerce"
    )

    apps["Size_MB"] = apps["Size"].apply(convert_size)

    apps["Installs_Num"] = (
        apps["Installs"].apply(convert_installs)
    )

    reviews["Sentiment_Subjectivity"] = pd.to_numeric(
        reviews["Sentiment_Subjectivity"],
        errors="coerce"
    )

    # Average subjectivity for each application
    review_summary = (
        reviews.groupby("App")["Sentiment_Subjectivity"]
        .mean()
        .reset_index()
    )

    review_summary.rename(
        columns={
            "Sentiment_Subjectivity":
            "Average_Subjectivity"
        },
        inplace=True
    )

    # Merge datasets
    df = pd.merge(
        apps,
        review_summary,
        on="App",
        how="inner"
    )

    return df


# ==========================================================
# 8. APPLY FILTERS
# ==========================================================

def apply_filters(df):

    required_categories = list(CATEGORY_TRANSLATIONS.keys())

    filtered = df[
        (df["Rating"] > 3.5)
        & (df["Category"].isin(required_categories))
        & (df["Reviews"] > 500)
        & (~df["App"].str.contains("S", case=False, na=False))
        & (df["Average_Subjectivity"] > 0.5)
        & (df["Installs_Num"] > 50000)
        & (df["Size_MB"].notna())
    ].copy()

    filtered["Display_Category"] = (
        filtered["Category"].map(CATEGORY_TRANSLATIONS)
    )

    return filtered


# ==========================================================
# 9. HERO SECTION
# ==========================================================


# ==========================================================
# 9. HERO SECTION - FIXED HTML RENDERING
# ==========================================================

st.html("""
<div class="hero">

    <div class="hero-label">
        ✦ DATA INTELLIGENCE PLATFORM
    </div>

    <div class="hero-title">
        PlayStore Nexus
    </div>

    <div class="hero-description">
        Discover the hidden patterns behind application
        performance. Analyze ratings, downloads, application
        sizes and customer sentiment through interactive
        data visualization.
    </div>

    <div class="hero-footer">
        APP INTELLIGENCE &nbsp; • &nbsp;
        DATA VISUALIZATION &nbsp; • &nbsp;
        SENTIMENT ANALYTICS
    </div>

</div>
""")



# ==========================================================
# 10. CURRENT TIME / ACCESS WINDOW
# ==========================================================

IST = ZoneInfo("Asia/Kolkata")

current_time = datetime.now(IST)

is_available = 17 <= current_time.hour < 19

time_col1, time_col2 = st.columns([3, 1])

with time_col1:

    st.markdown(
        f"""
        <div style="color:#A5B4D0;font-size:13px;">
        <span style="color:#A78BFA;">●</span>
        INDIA STANDARD TIME &nbsp; |
        {current_time.strftime('%d %B %Y')}
        &nbsp; | &nbsp;
        {current_time.strftime('%I:%M:%S %p')}
        </div>
        """,
        unsafe_allow_html=True
    )

with time_col2:

    if is_available:

        st.markdown(
            '<span class="status-pill">● CHART ACTIVE</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <span style="
            background:rgba(251,191,36,0.12);
            color:#FCD34D;
            border:1px solid #854D0E;
            padding:7px 13px;
            border-radius:30px;
            font-size:11px;
            font-weight:700;">
            ◷ CHART LOCKED
            </span>
            """,
            unsafe_allow_html=True
        )


# ==========================================================
# 11. LOAD DATA AND ERROR HANDLING
# ==========================================================

try:

    if not PLAYSTORE_FILE.exists():
        st.error("Play Store CSV file is missing.")
        st.stop()

    if not REVIEWS_FILE.exists():
        st.error("User Reviews CSV file is missing.")
        st.stop()

    apps, reviews = load_data()

    df = process_data(apps, reviews)

    filtered = apply_filters(df)

except Exception as error:

    st.error(f"Unable to load or process the data: {error}")
    st.stop()


# ==========================================================
# 12. SIDEBAR
# ==========================================================

# ==========================================================
# 12. SIDEBAR
# ==========================================================

# Sidebar Branding
st.sidebar.html("""
<div style="padding:10px 0 22px 0;">

    <div style="
        font-size:25px;
        font-weight:900;
        color:#C4B5FD;
        line-height:1.3;">
        ◈ NEXUS
    </div>

    <div style="
        font-size:10px;
        letter-spacing:2px;
        color:#8290AD;
        margin-top:4px;">
        ANALYTICS CONTROL CENTER
    </div>

</div>
""")

st.sidebar.markdown("### 🎛️ Dashboard Controls")

st.sidebar.caption(
    "Customize your application analysis."
)

selected_categories = st.sidebar.multiselect(
    "Select categories",
    options=CATEGORY_ORDER,
    default=CATEGORY_ORDER
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🔍 Filter Summary")

st.sidebar.markdown("""
**Applied Conditions**

- Rating above 3.5
- Reviews above 500
- Installs above 50,000
- Subjectivity above 0.5
- App name excludes letter S
- Nine specified categories
""")

st.sidebar.markdown("---")

st.sidebar.markdown("### ⏰ Chart Availability")

st.sidebar.info(
    "Available daily from 5:00 PM to 7:00 PM IST."
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "PlayStore Nexus | Version 1.0"
)

# ==========================================================
# 13. CATEGORY SELECTION
# ==========================================================

chart_data = filtered[
    filtered["Display_Category"].isin(selected_categories)
].copy()


# ==========================================================
# 14. KPI CARDS
# ==========================================================

st.markdown(
    '<div class="section-heading">◈ Performance Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Key indicators calculated from the filtered dataset.'
    '</div>',
    unsafe_allow_html=True
)

if chart_data.empty:

    st.warning(
        "No applications match the selected categories "
        "and filtering conditions."
    )

else:

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "📱 TOTAL APPS",
        f"{len(chart_data):,}"
    )

    k2.metric(
        "⭐ AVG RATING",
        f"{chart_data['Rating'].mean():.2f} / 5"
    )

    k3.metric(
        "💾 AVG APP SIZE",
        f"{chart_data['Size_MB'].mean():.2f} MB"
    )

    k4.metric(
        "⬇ TOTAL INSTALLS",
        f"{chart_data['Installs_Num'].sum():,.0f}"
    )


# ==========================================================
# 15. BUBBLE CHART
# ==========================================================

st.markdown(
    '<div class="section-heading">◉ Application Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore the relationship between app size, ratings '
    'and download popularity.'
    '</div>',
    unsafe_allow_html=True
)

if not is_available:

    st.markdown("""
    <div style="
        background:linear-gradient(120deg,#25213F,#171C32);
        border:1px solid #6D4BB8;
        border-radius:18px;
        padding:35px;
        text-align:center;
        margin:15px 0 25px 0;
    ">
        <div style="font-size:40px;">🔒</div>
        <h2 style="color:white;">Visualization Temporarily Locked</h2>
        <p style="color:#B9B8D8;">
        The interactive Bubble Chart is accessible only
        between 5:00 PM and 7:00 PM Indian Standard Time.
        </p>
        <div style="
        display:inline-block;
        background:#33265E;
        color:#DDD6FE;
        padding:10px 20px;
        border-radius:30px;
        font-weight:700;
        margin-top:10px;">
        AVAILABLE: 05:00 PM – 07:00 PM IST
        </div>
    </div>
    """, unsafe_allow_html=True)

else:

    if chart_data.empty:

        st.warning("No chart data available.")

    else:

        max_installs = chart_data["Installs_Num"].max()

        size_reference = (
            2.0 * max_installs / (45 ** 2)
            if max_installs > 0 else 1
        )

        fig = px.scatter(

            chart_data,

            x="Size_MB",

            y="Rating",

            size="Installs_Num",

            color="Display_Category",

            color_discrete_map=COLOR_MAP,

            hover_name="App",

            hover_data={

                "Size_MB": ":.2f",

                "Rating": ":.2f",

                "Reviews": ":,.0f",

                "Installs_Num": ":,.0f",

                "Average_Subjectivity": ":.3f",

                "Display_Category": True

            },

            category_orders={
                "Display_Category": CATEGORY_ORDER
            },

            size_max=45,

            title="App Size vs Average Rating"

        )

        fig.update_traces(

            marker=dict(

                sizemode="area",

                sizeref=size_reference,

                opacity=0.78,

                line=dict(
                    width=1.3,
                    color="white"
                )

            )

        )

        fig.update_layout(

            height=680,

            template="plotly_white",

            paper_bgcolor="#FFFFFF",

            plot_bgcolor="#FFFFFF",

            title=dict(

                text="APP SIZE × RATING × INSTALLS",

                font=dict(
                    size=20,
                    color="#211B45",
                    family="Arial"
                ),

                x=0.04

            ),

            xaxis=dict(

                title="Application Size (MB)",

                gridcolor="#E9EAF2",

                zeroline=False

            ),

            yaxis=dict(

                title="Average Rating",

                range=[3.5, 5.1],

                gridcolor="#E9EAF2",

                zeroline=False

            ),

            legend=dict(

                title="APP CATEGORY",

                orientation="h",

                yanchor="bottom",

                y=-0.24,

                xanchor="left",

                x=0

            ),

            hoverlabel=dict(

                bgcolor="#17172E",

                font_color="white",

                font_size=13

            ),

            margin=dict(
                l=45,
                r=30,
                t=75,
                b=100
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={
                "displayModeBar": True,
                "displaylogo": False,
                "scrollZoom": True,
                "responsive": True
            }

        )

        st.caption(
            "Bubble area represents install volume. "
            "Pink bubbles identify Game applications."
        )


# ==========================================================
# 16. CATEGORY ANALYSIS
# ==========================================================

st.markdown("---")

st.markdown(
    '<div class="section-heading">▦ Category Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Compare application counts and average ratings by category.'
    '</div>',
    unsafe_allow_html=True
)

if not chart_data.empty:

    category_summary = (
        chart_data.groupby("Display_Category")
        .agg(
            App_Count=("App", "count"),
            Average_Rating=("Rating", "mean"),
            Average_Size=("Size_MB", "mean"),
            Total_Installs=("Installs_Num", "sum")
        )
        .reset_index()
    )

    category_summary["Average_Rating"] = (
        category_summary["Average_Rating"].round(2)
    )

    category_summary["Average_Size"] = (
        category_summary["Average_Size"].round(2)
    )

    left, right = st.columns(2)

    with left:

        category_bar = px.bar(

            category_summary,

            x="Display_Category",

            y="App_Count",

            color="Display_Category",

            color_discrete_map=COLOR_MAP,

            title="Applications by Category",

            text="App_Count"

        )

        category_bar.update_layout(
            template="plotly_white",
            height=400,
            showlegend=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Category",
            yaxis_title="Number of Applications"
        )

        category_bar.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            category_bar,
            use_container_width=True
        )

    with right:

        rating_chart = px.bar(

            category_summary,

            x="Display_Category",

            y="Average_Rating",

            color="Display_Category",

            color_discrete_map=COLOR_MAP,

            title="Average Rating by Category",

            text="Average_Rating"

        )

        rating_chart.update_layout(
            template="plotly_white",
            height=400,
            showlegend=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Category",
            yaxis_title="Average Rating",
            yaxis_range=[0, 5.2]
        )

        rating_chart.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            rating_chart,
            use_container_width=True
        )


# ==========================================================
# 17. APPLICATION DATA TABLE
# ==========================================================

st.markdown("---")

st.markdown(
    '<div class="section-heading">▤ Application Explorer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore the filtered applications and their metrics.'
    '</div>',
    unsafe_allow_html=True
)

if not chart_data.empty:

    search = st.text_input(
        "🔎 Search application",
        placeholder="Enter an application name..."
    )

    table_data = chart_data.copy()

    if search:

        table_data = table_data[
            table_data["App"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    output_columns = [

        "App",
        "Display_Category",
        "Size_MB",
        "Rating",
        "Reviews",
        "Installs_Num",
        "Average_Subjectivity"

    ]

    display_data = table_data[output_columns].rename(

        columns={

            "Display_Category": "Category",

            "Size_MB": "Size (MB)",

            "Installs_Num": "Installs",

            "Average_Subjectivity":
            "Average Subjectivity"

        }

    )

    st.dataframe(

        display_data,

        use_container_width=True,

        hide_index=True,

        height=380,

        column_config={

            "Size (MB)": st.column_config.NumberColumn(
                format="%.2f MB"
            ),

            "Rating": st.column_config.NumberColumn(
                format="%.2f ⭐"
            ),

            "Installs": st.column_config.NumberColumn(
                format="%,.0f"
            ),

            "Average Subjectivity":
            st.column_config.NumberColumn(
                format="%.3f"
            )

        }

    )

    csv = display_data.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(

        "⬇ Download Filtered Applications",

        data=csv,

        file_name="PlayStore_Nexus_Filtered_Data.csv",

        mime="text/csv"

    )


# ==========================================================
# 18. FOOTER
# ==========================================================


# ==========================================================
# 18. PREMIUM FOOTER - FIXED
# ==========================================================

st.markdown("---")

st.html("""
<div style="
    background: linear-gradient(
        120deg,
        #191C38,
        #30205C,
        #54245E
    );
    border: 1px solid #62469A;
    border-radius: 18px;
    padding: 35px 20px;
    text-align: center;
    margin-top: 25px;
">

    <div style="
        font-size: 25px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #C4B5FD;
        margin-bottom: 12px;
    ">
        ◈ PLAYSTORE NEXUS
    </div>

    <div style="
        font-size: 12px;
        color: #E9D5FF;
        letter-spacing: 1.5px;
        line-height: 2.2;
    ">
        POWERED BY PYTHON &nbsp; • &nbsp;
        STREAMLIT &nbsp; • &nbsp;
        PANDAS &nbsp; • &nbsp; PLOTLY
    </div>

    <div style="
        height: 1px;
        background: rgba(255,255,255,0.18);
        margin: 20px auto;
        max-width: 450px;
    "></div>

    <div style="
        font-size: 11px;
        color: #C4B5FD;
        letter-spacing: 2px;
        line-height: 2.5;
    ">
        APP INTELLIGENCE &nbsp; | &nbsp;
        DATA ANALYTICS &nbsp; | &nbsp;
        INTERACTIVE VISUALIZATION
    </div>

    <div style="
        color: #A5A5C5;
        font-size: 12px;
        margin-top: 20px;
    ">
        © 2026 PlayStore Nexus.
        All Rights Reserved.
    </div>

    <div style="
        color: #8B7EBB;
        font-size: 10px;
        margin-top: 8px;
    ">
        TURNING APP DATA INTO INTELLIGENCE ✦
    </div>

</div>
""")
