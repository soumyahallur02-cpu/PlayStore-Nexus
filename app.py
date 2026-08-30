# ============================================================
# APP SIZE vs AVERAGE RATING - BUBBLE CHART DASHBOARD
# ============================================================

import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.express as px

from dash import (
    Dash,
    html,
    dcc,
    Input,
    Output,
    State
)

import dash_bootstrap_components as dbc


# ============================================================
# 1. CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# CHANGE THIS FILE NAME IF YOUR DATASET HAS A DIFFERENT NAME
# ------------------------------------------------------------

DATA_FILE ="data/googleplaystore_merged_with_subjectivity.csv"


# IST timezone
IST = ZoneInfo("Asia/Kolkata")


# Required categories
ALLOWED_CATEGORIES = [
    "GAME",
    "BEAUTY",
    "BUSINESS",
    "COMICS",
    "COMMUNICATION",
    "DATING",
    "ENTERTAINMENT",
    "SOCIAL",
    "EVENTS"
]


# ============================================================
# 2. CATEGORY TRANSLATIONS
# ============================================================

CATEGORY_TRANSLATIONS = {

    # Beauty -> Hindi
    "BEAUTY": "सौंदर्य",

    # Business -> Tamil
    "BUSINESS": "வணிகம்",

    # Dating -> German
    "DATING": "Partnersuche",

    # Other categories remain in English
    "GAME": "Game",
    "COMICS": "Comics",
    "COMMUNICATION": "Communication",
    "ENTERTAINMENT": "Entertainment",
    "SOCIAL": "Social",
    "EVENTS": "Events"
}


# ============================================================
# 3. CATEGORY COLORS
# ============================================================

# Game MUST be pink
CATEGORY_COLORS = {

    "Game": "#FF69B4",

    "सौंदर्य": "#20B2AA",

    "வணிகம்": "#9370DB",

    "Partnersuche": "#FFA07A",

    "Comics": "#FFD166",

    "Communication": "#40C4E8",

    "Entertainment": "#FF7F9F",

    "Social": "#B8E986",

    "Events": "#C084FC"
}


# ============================================================
# 4. LOAD DATASET
# ============================================================

print("=" * 60)
print("APP BUBBLE CHART DASHBOARD")
print("=" * 60)


if not os.path.exists(DATA_FILE):

    print()
    print("ERROR: Dataset file was not found.")
    print()
    print("Current folder:")
    print(os.getcwd())
    print()
    print("Files found:")

    for file in os.listdir("."):
        print(" -", file)

    print()
    print("Change DATA_FILE at the top of app.py")
    print("to the exact name of your CSV file.")

    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )


df = pd.read_csv(DATA_FILE)


print()
print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:")
print(df.columns.tolist())


# ============================================================
# 5. CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()


# ============================================================
# 6. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "App",
    "Category",
    "Rating",
    "Reviews",
    "Size_MB",
    "Installs",
    "Sentiment_Subjectivity"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print()
    print("ERROR: Missing required columns:")
    print(missing_columns)

    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# 7. CLEAN NUMERIC COLUMNS
# ============================================================

# Rating
df["Rating"] = pd.to_numeric(
    df["Rating"],
    errors="coerce"
)


# Reviews
df["Reviews"] = pd.to_numeric(
    df["Reviews"],
    errors="coerce"
)


# Size
df["Size_MB"] = pd.to_numeric(
    df["Size_MB"],
    errors="coerce"
)


# Installs
#
# This handles values such as:
# 1,000+
# 50,000+
# 1,000,000
# 50000
#

if df["Installs"].dtype == "object":

    df["Installs"] = (
        df["Installs"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip()
    )


df["Installs"] = pd.to_numeric(
    df["Installs"],
    errors="coerce"
)


# Sentiment subjectivity
df["Sentiment_Subjectivity"] = pd.to_numeric(
    df["Sentiment_Subjectivity"],
    errors="coerce"
)


# ============================================================
# 8. CLEAN CATEGORY
# ============================================================

df["Category"] = (
    df["Category"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# Clean app names
df["App"] = (
    df["App"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 9. REMOVE INVALID ROWS
# ============================================================

df = df.dropna(
    subset=[
        "App",
        "Category",
        "Rating",
        "Reviews",
        "Size_MB",
        "Installs",
        "Sentiment_Subjectivity"
    ]
).copy()


# ============================================================
# 10. CREATE CATEGORY DISPLAY COLUMN
# ============================================================

df["Category_Display"] = (
    df["Category"]
    .map(CATEGORY_TRANSLATIONS)
)


# ============================================================
# 11. KEEP ONLY REQUIRED CATEGORIES
# ============================================================

category_df = df[
    df["Category"].isin(
        ALLOWED_CATEGORIES
    )
].copy()


# ============================================================
# 12. FILTER FUNCTION
# ============================================================

def apply_filters(
    min_rating=3.5,
    min_reviews=500,
    min_installs=50000,
    min_subjectivity=0.5,
    selected_categories=None
):
    """
    Applies all mandatory project filters.

    Mandatory:
        Rating > 3.5
        Reviews > 500
        Installs > 50,000
        Sentiment Subjectivity > 0.5
        App name must NOT contain letter S
        Category must be one of the required categories

    Interactive filters can only make the thresholds stricter.
    """

    result = category_df.copy()


    # --------------------------------------------------------
    # Mandatory minimum values
    # --------------------------------------------------------

    # Prevent the user from going below project requirements
    min_rating = max(
        float(min_rating),
        3.5
    )

    min_reviews = max(
        int(min_reviews),
        500
    )

    min_installs = max(
        int(min_installs),
        50000
    )

    min_subjectivity = max(
        float(min_subjectivity),
        0.5
    )


    # --------------------------------------------------------
    # Rating
    # --------------------------------------------------------

    result = result[
        result["Rating"] > min_rating
    ]


    # --------------------------------------------------------
    # Reviews
    # --------------------------------------------------------

    result = result[
        result["Reviews"] > min_reviews
    ]


    # --------------------------------------------------------
    # Installs
    # --------------------------------------------------------

    result = result[
        result["Installs"] > min_installs
    ]


    # --------------------------------------------------------
    # Sentiment Subjectivity
    # --------------------------------------------------------

    result = result[
        result["Sentiment_Subjectivity"]
        > min_subjectivity
    ]


    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    if selected_categories:

        result = result[
            result["Category"].isin(
                selected_categories
            )
        ]


    # --------------------------------------------------------
    # App name MUST NOT contain letter S
    # Case insensitive
    # --------------------------------------------------------

    result = result[
        ~result["App"]
        .str.contains(
            "S",
            case=False,
            na=False
        )
    ]


    return result.copy()


# ============================================================
# 13. DEFAULT FILTERED DATA
# ============================================================

filtered_df = apply_filters(
    min_rating=3.5,
    min_reviews=500,
    min_installs=50000,
    min_subjectivity=0.5,
    selected_categories=ALLOWED_CATEGORIES
)


print()
print("Original rows:", len(df))
print("Filtered rows:", len(filtered_df))


print()
print("Translated categories:")

print(
    filtered_df[
        [
            "Category",
            "Category_Display"
        ]
    ]
    .drop_duplicates()
    .sort_values("Category")
    .to_string(index=False)
)


# ============================================================
# 14. IST TIME FUNCTION
# ============================================================

def get_current_ist_time():

    return datetime.now(IST)


# ============================================================
# 15. CHECK 5 PM - 7 PM IST
# ============================================================

def is_allowed_time():

    current_time = get_current_ist_time()

    current_minutes = (
        current_time.hour * 60
        + current_time.minute
    )

    start_minutes = 17 * 60      # 5:00 PM
    end_minutes = 19 * 60        # 7:00 PM

    return (
        start_minutes
        <= current_minutes
        < end_minutes
    )


# ============================================================
# 16. FORMAT NUMBERS
# ============================================================

def format_number(value):

    if value is None:
        return "0"

    try:
        value = int(value)
    except:
        return "0"

    return f"{value:,}"


# ============================================================
# 17. CREATE DASH APP
# ============================================================

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ],
    suppress_callback_exceptions=True
)


app.title = (
    "App Size vs Average Rating"
)


# ============================================================
# 18. STYLES
# ============================================================

PAGE_STYLE = {

    "backgroundColor": "#F4F7FB",

    "minHeight": "100vh",

    "padding": "30px"
}


CARD_STYLE = {

    "backgroundColor": "white",

    "borderRadius": "12px",

    "padding": "25px",

    "boxShadow":
        "0 2px 10px rgba(0,0,0,0.08)",

    "marginBottom": "25px"
}


# ============================================================
# 19. CATEGORY DROPDOWN OPTIONS
# ============================================================

category_options = [

    {
        "label": CATEGORY_TRANSLATIONS[category],
        "value": category
    }

    for category in ALLOWED_CATEGORIES

]


# ============================================================
# 20. DASHBOARD LAYOUT
# ============================================================

app.layout = html.Div(

    [

        # ----------------------------------------------------
        # PAGE TITLE
        # ----------------------------------------------------

        html.H1(

            "App Size vs Average Rating",

            style={
                "textAlign": "center",
                "fontWeight": "700",
                "fontSize": "52px",
                "color": "#202124",
                "marginBottom": "10px"
            }
        ),


        html.H3(

            "Bubble Size represents Number of Installs",

            style={
                "textAlign": "center",
                "fontWeight": "400",
                "color": "#555",
                "marginBottom": "25px"
            }
        ),


        # ----------------------------------------------------
        # PROJECT REQUIREMENTS
        # ----------------------------------------------------

        html.P(

            "Mandatory Requirements: "
            "Rating > 3.5 | "
            "Reviews > 500 | "
            "Installs > 50K | "
            "Subjectivity > 0.5 | "
            "App name does not contain 'S'",

            style={
                "textAlign": "center",
                "fontSize": "18px",
                "color": "#666"
            }
        ),


        html.H5(

            "Visualization available only from "
            "5:00 PM to 7:00 PM IST",

            style={
                "textAlign": "center",
                "fontWeight": "700",
                "marginTop": "25px"
            }
        ),


        # ----------------------------------------------------
        # CURRENT TIME
        # ----------------------------------------------------

        html.Div(

            id="current-time",

            style={
                "textAlign": "center",
                "fontSize": "20px",
                "marginTop": "15px",
                "marginBottom": "25px"
            }
        ),


        # ----------------------------------------------------
        # FILTER PANEL
        # ----------------------------------------------------

        dbc.Card(

            [

                dbc.CardBody(

                    [

                        html.H2(

                            "Dashboard Filters",

                            style={
                                "fontWeight": "700",
                                "marginBottom": "25px"
                            }
                        ),


                        # ------------------------------------
                        # CATEGORY
                        # ------------------------------------

                        html.Label(

                            "Category",

                            style={
                                "fontWeight": "600",
                                "fontSize": "17px"
                            }
                        ),


                        dcc.Dropdown(

                            id="category-filter",

                            options=category_options,

                            value=ALLOWED_CATEGORIES,

                            multi=True,

                            clearable=False,

                            placeholder=
                                "Select categories..."
                        ),


                        html.Br(),


                        # ------------------------------------
                        # MINIMUM RATING
                        # ------------------------------------

                        html.Label(

                            "Minimum Rating",

                            style={
                                "fontWeight": "600",
                                "fontSize": "17px"
                            }
                        ),


                        dcc.Input(

                            id="rating-filter",

                            type="number",

                            value=3.5,

                            min=3.5,

                            max=5,

                            step=0.1,

                            style={
                                "width": "100%",
                                "padding": "10px",
                                "borderRadius": "6px",
                                "border":
                                    "1px solid #ccc"
                            }
                        ),


                        html.Small(

                            "Requirement: Rating > 3.5",

                            style={
                                "color": "#777"
                            }
                        ),


                        html.Br(),
                        html.Br(),


                        # ------------------------------------
                        # REVIEWS
                        # ------------------------------------

                        html.Label(

                            "Minimum Reviews",

                            style={
                                "fontWeight": "600",
                                "fontSize": "17px"
                            }
                        ),


                        dcc.Input(

                            id="reviews-filter",

                            type="number",

                            value=500,

                            min=500,

                            step=100,

                            style={
                                "width": "100%",
                                "padding": "10px",
                                "borderRadius": "6px",
                                "border":
                                    "1px solid #ccc"
                            }
                        ),


                        html.Small(

                            "Requirement: Reviews > 500",

                            style={
                                "color": "#777"
                            }
                        ),


                        html.Br(),
                        html.Br(),


                        # ------------------------------------
                        # INSTALLS
                        # ------------------------------------

                        html.Label(

                            "Minimum Installs",

                            style={
                                "fontWeight": "600",
                                "fontSize": "17px"
                            }
                        ),


                        dcc.Input(

                            id="installs-filter",

                            type="number",

                            value=50000,

                            min=50000,

                            step=10000,

                            style={
                                "width": "100%",
                                "padding": "10px",
                                "borderRadius": "6px",
                                "border":
                                    "1px solid #ccc"
                            }
                        ),


                        html.Small(

                            "Requirement: Installs > 50,000",

                            style={
                                "color": "#777"
                            }
                        ),


                        html.Br(),
                        html.Br(),


                        # ------------------------------------
                        # SUBJECTIVITY
                        # ------------------------------------

                        html.Label(

                            "Minimum Sentiment Subjectivity",

                            style={
                                "fontWeight": "600",
                                "fontSize": "17px"
                            }
                        ),


                        dcc.Input(

                            id="subjectivity-filter",

                            type="number",

                            value=0.5,

                            min=0.5,

                            max=1,

                            step=0.05,

                            style={
                                "width": "100%",
                                "padding": "10px",
                                "borderRadius": "6px",
                                "border":
                                    "1px solid #ccc"
                            }
                        ),


                        html.Small(

                            "Requirement: Subjectivity > 0.5",

                            style={
                                "color": "#777"
                            }
                        ),


                        html.Br(),
                        html.Br(),


                        # ------------------------------------
                        # FIXED REQUIREMENTS
                        # ------------------------------------

                        dbc.Alert(

                            [

                                html.Strong(
                                    "Fixed filter: "
                                ),

                                "App names containing "
                                "the letter 'S' are excluded."
                            ],

                            color="info",

                            style={
                                "marginTop": "15px"
                            }
                        ),


                        # ------------------------------------
                        # APPLY BUTTON
                        # ------------------------------------

                        dbc.Button(

                            "Apply Filters",

                            id="apply-button",

                            color="primary",

                            size="lg",

                            n_clicks=0,

                            style={
                                "width": "100%",
                                "marginTop": "15px"
                            }
                        )

                    ]

                )

            ],

            style=CARD_STYLE
        ),


        # ----------------------------------------------------
        # DASHBOARD CONTENT
        # ----------------------------------------------------

        html.Div(

            id="dashboard-content"

        ),


        # ----------------------------------------------------
        # TIME CHECK
        # ----------------------------------------------------

        dcc.Interval(

            id="time-check",

            interval=30 * 1000,

            n_intervals=0

        )

    ],

    style=PAGE_STYLE
)


# ============================================================
# 21. CALLBACK
# ============================================================

@app.callback(

    Output(
        "dashboard-content",
        "children"
    ),

    Output(
        "current-time",
        "children"
    ),

    Input(
        "time-check",
        "n_intervals"
    ),

    Input(
        "apply-button",
        "n_clicks"
    ),

    State(
        "category-filter",
        "value"
    ),

    State(
        "rating-filter",
        "value"
    ),

    State(
        "reviews-filter",
        "value"
    ),

    State(
        "installs-filter",
        "value"
    ),

    State(
        "subjectivity-filter",
        "value"
    )
)
def update_dashboard(

    n_intervals,

    n_clicks,

    selected_categories,

    min_rating,

    min_reviews,

    min_installs,

    min_subjectivity

):


    # ========================================================
    # CURRENT IST TIME
    # ========================================================

    current_time = get_current_ist_time()


    formatted_time = (

        "Current IST Time: "

        + current_time.strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

    )


    # ========================================================
    # TIME RESTRICTION
    # ========================================================

    if not is_allowed_time():

        unavailable_content = html.Div(

            [

                html.H1(

                    "Bubble Chart Currently Unavailable",

                    style={
                        "fontWeight": "700",
                        "fontSize": "38px"
                    }
                ),


                html.P(

                    "This visualization is available "
                    "only between 5:00 PM and 7:00 PM IST.",

                    style={
                        "fontSize": "22px",
                        "marginTop": "20px"
                    }
                ),


                html.P(

                    "Please return during the "
                    "allowed time window.",

                    style={
                        "fontSize": "18px",
                        "color": "#777"
                    }
                )

            ],

            style={

                "backgroundColor": "white",

                "borderRadius": "15px",

                "padding": "70px 30px",

                "textAlign": "center",

                "boxShadow":
                    "0 3px 15px rgba(0,0,0,0.08)"

            }

        )


        return (
            unavailable_content,
            formatted_time
        )


    # ========================================================
    # SAFETY CHECK FOR CATEGORY
    # ========================================================

    if not selected_categories:

        selected_categories = ALLOWED_CATEGORIES


    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered_data = apply_filters(

        min_rating=(
            min_rating
            if min_rating is not None
            else 3.5
        ),

        min_reviews=(
            min_reviews
            if min_reviews is not None
            else 500
        ),

        min_installs=(
            min_installs
            if min_installs is not None
            else 50000
        ),

        min_subjectivity=(
            min_subjectivity
            if min_subjectivity is not None
            else 0.5
        ),

        selected_categories=selected_categories

    )


    # ========================================================
    # EMPTY DATA CHECK
    # ========================================================

    if filtered_data.empty:

        empty_content = html.Div(

            [

                html.H2(

                    "No Apps Match the Selected Filters",

                    style={
                        "fontWeight": "700"
                    }

                ),

                html.P(

                    "Try selecting more categories "
                    "or reducing the filter values "
                    "while keeping the mandatory "
                    "minimum requirements.",

                    style={
                        "fontSize": "18px",
                        "color": "#666"
                    }

                )

            ],

            style={

                "backgroundColor": "white",

                "padding": "80px",

                "textAlign": "center",

                "borderRadius": "15px"

            }

        )


        return (
            empty_content,
            formatted_time
        )


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    qualified_apps = len(
        filtered_data
    )


    average_rating = round(

        filtered_data[
            "Rating"
        ].mean(),

        2

    )


    total_installs = int(

        filtered_data[
            "Installs"
        ].sum()

    )


    # ========================================================
    # CREATE BUBBLE CHART
    # ========================================================

    fig = px.scatter(

        filtered_data,

        x="Size_MB",

        y="Rating",

        size="Installs",

        color="Category_Display",

        color_discrete_map=CATEGORY_COLORS,

        hover_name="App",

        hover_data={

            "Size_MB":
                ":.2f",

            "Rating":
                ":.2f",

            "Reviews":
                ":,",

            "Installs":
                ":,",

            "Sentiment_Subjectivity":
                ":.2f",

            "Category_Display":
                True

        },

        size_max=45,

        title="App Size vs Average Rating"

    )


    # ========================================================
    # CHART STYLING
    # ========================================================

    fig.update_traces(

        marker=dict(

            opacity=0.78,

            line=dict(
                width=1,
                color="white"
            )

        )

    )


    fig.update_layout(

        template="plotly_white",

        height=700,

        title={

            "text":
                "App Size vs Average Rating",

            "x":
                0.5,

            "xanchor":
                "center",

            "font":
                {
                    "size": 28
                }

        },

        xaxis={

            "title":
                "App Size (MB)",

            "rangemode":
                "tozero",

            "showgrid":
                True

        },

        yaxis={

            "title":
                "Average Rating",

            "range":
                [
                    3.5,
                    max(
                        5,
                        float(
                            filtered_data[
                                "Rating"
                            ].max()
                        ) + 0.1
                    )
                ]

        },

        legend={

            "title":
                "Category",

            "orientation":
                "v"

        },

        margin={

            "l": 80,

            "r": 80,

            "t": 100,

            "b": 80

        }

    )


    # ========================================================
    # KPI CARD FUNCTION
    # ========================================================

    def create_kpi_card(
        title,
        value
    ):

        return dbc.Card(

            dbc.CardBody(

                [

                    html.H4(

                        title,

                        style={
                            "textAlign": "center",
                            "fontWeight": "600",
                            "color": "#333"
                        }

                    ),

                    html.H2(

                        value,

                        style={
                            "textAlign": "center",
                            "fontSize": "40px",
                            "fontWeight": "700",
                            "marginTop": "15px"
                        }

                    )

                ]

            ),

            style={

                "height": "160px",

                "borderRadius": "12px",

                "boxShadow":
                    "0 2px 10px rgba(0,0,0,0.08)"

            }

        )


    # ========================================================
    # KPI ROW
    # ========================================================

    kpi_row = dbc.Row(

        [

            dbc.Col(

                create_kpi_card(

                    "Qualified Apps",

                    format_number(
                        qualified_apps
                    )

                ),

                md=4

            ),

            dbc.Col(

                create_kpi_card(

                    "Average Rating",

                    f"{average_rating:.2f}"

                ),

                md=4

            ),

            dbc.Col(

                create_kpi_card(

                    "Total Installs",

                    format_number(
                        total_installs
                    )

                ),

                md=4

            )

        ],

        className="g-4",

        style={
            "marginBottom": "30px"
        }

    )


    # ========================================================
    # FILTER SUMMARY
    # ========================================================

    selected_display_categories = [

        CATEGORY_TRANSLATIONS.get(
            category,
            category
        )

        for category in selected_categories

    ]


    filter_summary = dbc.Card(

        dbc.CardBody(

            [

                html.H4(

                    "Applied Filters",

                    style={
                        "fontWeight": "700",
                        "marginBottom": "15px"
                    }

                ),

                html.P(

                    [

                        html.Strong(
                            "Average Rating: "
                        ),

                        f"> {max(float(min_rating), 3.5)}"

                    ]

                ),

                html.P(

                    [

                        html.Strong(
                            "Reviews: "
                        ),

                        f"> {max(int(min_reviews), 500):,}"

                    ]

                ),

                html.P(

                    [

                        html.Strong(
                            "Installs: "
                        ),

                        f"> {max(int(min_installs), 50000):,}"

                    ]

                ),

                html.P(

                    [

                        html.Strong(
                            "Sentiment Subjectivity: "
                        ),

                        f"> {max(float(min_subjectivity), 0.5)}"

                    ]

                ),

                html.P(

                    [

                        html.Strong(
                            "App Name: "
                        ),

                        "Does not contain letter 'S'"

                    ]

                ),

                html.P(

                    [

                        html.Strong(
                            "Categories: "
                        ),

                        ", ".join(
                            selected_display_categories
                        )

                    ]

                ),

                html.P(

                    [

                        html.Strong(
                            "Game Category: "
                        ),

                        "Highlighted in Pink"

                    ],

                    style={
                        "marginBottom": "0"
                    }

                )

            ]

        ),

        style={

            "marginTop": "25px",

            "borderRadius": "12px",

            "boxShadow":
                "0 2px 10px rgba(0,0,0,0.08)"

        }

    )


    # ========================================================
    # FINAL DASHBOARD
    # ========================================================

    dashboard_content = [

        # KPI cards
        kpi_row,


        # Chart
        dbc.Card(

            dbc.CardBody(

                [

                    dcc.Graph(

                        id="bubble-chart",

                        figure=fig,

                        config={

                            "displayModeBar": True,

                            "displaylogo": False

                        }

                    )

                ]

            ),

            style={

                "borderRadius": "12px",

                "boxShadow":
                    "0 2px 10px rgba(0,0,0,0.08)"

            }

        ),


        # Applied filters
        filter_summary

    ]


    return (

        dashboard_content,

        formatted_time

    )


# ============================================================
# 22. RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("Dashboard starting...")
    print("=" * 60)

    print()
    print(
        "Allowed visualization time:"
    )

    print(
        "5:00 PM - 7:00 PM IST"
    )

    print()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=8050
    )