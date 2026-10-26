
"""
Standard Interactive Student Performance Dashboard (Plotly Dash)

Install: pip install dash pandas numpy plotly
Run: python student_dashboard.py
Open: http://127.0.0.1:8050
"""

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

# ---------------------------------------------------------------
# 1. DATA LAYER
# ---------------------------------------------------------------

rng = np.random.default_rng(42)
n = 5000

df = pd.DataFrame(
    {
        "date": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "department": rng.choice(["Computer", "IT", "Mechanical", "Electrical"], n),
        "subject": rng.choice(["Python", "Mathematics", "DBMS", "Data Analysis"], n),
        "student": [f"Student_{i}" for i in range(1, n + 1)],
        "marks": rng.integers(35, 101, n),
    }
)

df["result"] = np.where(df["marks"] >= 40, "Pass", "Fail")

# ---------------------------------------------------------------
# 2. APP + LAYOUT
# ---------------------------------------------------------------

app = Dash(__name__)
app.title = "Student Dashboard"

CARD = {
    "background": "#f7f7f9",
    "padding": "16px",
    "borderRadius": "8px",
    "textAlign": "center",
    "flex": "1",
}

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
        "maxWidth": "1200px",
        "margin": "auto",
    },
    children=[
        html.H1("Student Performance Dashboard"),

        # ---- Filters ----
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "20px",
                "flexWrap": "wrap",
            },
            children=[
                html.Div(
                    style={"flex": "1"},children=[html.Label("Department"),
                        dcc.Dropdown(id="department-filter",options=sorted(
                            df["department"].unique() ),
                            value=sorted(df["department"].unique() ),
                            multi=True,
                        ),
                    ],
                ),

                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.Label("Subject"),
                        dcc.Dropdown(
                            id="subject-filter",
                            options=sorted(df["subject"].unique() ),
                            value=sorted(df["subject"].unique() ),
                            multi=True,
                        ),
                    ],
                ),

                html.Div(
                    children=[
                        html.Label("Exam Range"),
                        html.Br(),
                        dcc.DatePickerRange(
                            id="date-filter",
                            min_date_allowed=df["date"].min(),
                            max_date_allowed=df["date"].max(),
                            start_date=df["date"].min(),
                            end_date=df["date"].max(),
                        ),
                    ]
                ),
            ],
        ),

        # ---- KPI Cards ----
        html.Div(
            id="kpi-row",
            style={
                "display": "flex",
                "gap": "16px",
                "marginBottom": "20px",
                "flexWrap": "wrap",
            },
        ),

        # ---- Charts ----
        dcc.Graph(id="trend-chart"),

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
            },
            children=[
                dcc.Graph(
                    id="subject-chart",
                    style={"flex": "1"},
                ),
                dcc.Graph(
                    id="department-chart",
                    style={"flex": "1"},
                ),
            ],
        ),
    ],
)

# ---------------------------------------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------------------------------------

def filter_data(departments, subjects, start, end) :
    departments = departments or []
    subjects = subjects or []

    return df[
        df["department"].isin(departments)
        & df["subject"].isin(subjects)
        & df["date"].between(
            pd.Timestamp(start),
            pd.Timestamp(end),
        )
    ]


def kpi_card(title, value):
    return html.Div(
        style=CARD,
        children=[
            html.Div(title, style={"color": "#666"}),
            html.H2(value, style={"margin": "4px 0 0"}),
        ],
    )


# ---------------------------------------------------------------
# 4. CALLBACKS
# ---------------------------------------------------------------

@app.callback(
    Output("kpi-row", "children"),
    Output("trend-chart", "figure"),
    Output("subject-chart", "figure"),
    Output("department-chart", "figure"),
    Input("department-filter", "value"),
    Input("subject-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_dashboard(departments, subjects, start, end):

    d = filter_data(departments, subjects, start, end)

    # ---- Handle empty data ----
    if d.empty:
        empty = px.scatter(title="No data for the selected filters")

        return [
            kpi_card("Total Students", "0"),
            kpi_card("Average Marks", "0"),
            kpi_card("Pass Percentage", "0%"),
            kpi_card("Highest Marks", "0"),
        ], empty, empty, empty

    # ---- Calculate KPIs ----
    total_students = len(d)
    average_marks = d["marks"].mean()
    pass_percentage = (d["result"] == "Pass").mean() * 100
    highest_marks = d["marks"].max()

    kpis = [
        kpi_card(
            "Total Records",
            f"{total_students:,}",
        ),
        kpi_card(
            "Average Marks",
            f"{average_marks:.2f}",
        ),
        kpi_card(
            "Pass Percentage",
            f"{pass_percentage:.1f}%",
        ),
        kpi_card(
            "Highest Marks",
            f"{highest_marks}",
        ),
    ]

    # ---- Monthly Average Marks Trend ----
    monthly = (
        d.set_index("date")
        .resample("MS")["marks"]
        .mean()
        .reset_index()
    )

    fig_trend = px.line(
        monthly,
        x="date",
        y="marks",
        markers=True,
        title="Monthly Average Marks Trend",
        labels={
            "date": "Exam Date",
            "marks": "Average Marks",
        },
    )

    # ---- Average Marks by Subject ----
    by_subject = (
        d.groupby("subject", as_index=False)["marks"]
        .mean()
        .sort_values("marks")
    )

    fig_subject = px.bar(
        by_subject,
        x="marks",
        y="subject",
        orientation="h",
        title="Average Marks by Subject",
        labels={
            "marks": "Average Marks",
            "subject": "Subject",
        },
    )

    # ---- Average Marks by Department ----
    by_department = (
        d.groupby("department", as_index=False)["marks"]
        .mean())

    fig_department = px.bar(
        by_department,
        x="department",
        y="marks",
        title="Average Marks by Department",
        labels={
            "department": "Department",
            "marks": "Average Marks",
        },
    )

    return (
        kpis,
        fig_trend,
        fig_subject,
        fig_department,
    )

# ---------------------------------------------------------------
# 5. RUN APPLICATION
# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
