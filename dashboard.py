from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("output/earthquake_analytics.csv")

# Convert date column
df["event_time"] = pd.to_datetime(df["event_time"])

app = Dash(__name__)

# Layout
app.layout = html.Div([

    html.H1(
        "Earthquake Analytics Dashboard",
        style={
            "textAlign": "center",
            "color": "#2c3e50"
        }
    ),

    html.P(
        "Interactive analysis of earthquake events generated through the ETL pipeline",
        style={
            "textAlign": "center",
            "fontSize": "18px",
            "color": "#555"
        }
    ),

    html.Hr(),

    html.Div([
        html.Label(
            "Select Magnitude Category",
            style={"fontWeight": "bold"}
        ),

        dcc.Dropdown(
            id="category-filter",
            options=[
                {"label": "All", "value": "All"}
            ] + [
                {"label": cat, "value": cat}
                for cat in sorted(df["magnitude_category"].dropna().unique())
            ],
            value="All"
        )
    ],
    style={
        "width": "40%",
        "margin": "auto"
    }),

    html.Br(),

    html.Div(
        id="kpi-card",
        style={
            "textAlign": "center",
            "fontSize": "32px",
            "fontWeight": "bold",
            "backgroundColor": "#f4f6f7",
            "padding": "25px",
            "borderRadius": "10px",
            "margin": "20px"
        }
    ),

    html.Div([

        dcc.Graph(
            id="bar-chart",
            config={"displayModeBar": False},
            style={"width": "48%"}
        ),

        dcc.Graph(
            id="line-chart",
            config={"displayModeBar": False},
            style={"width": "48%"}
        )

    ],
    style={
        "display": "flex",
        "justifyContent": "space-between"
    })

],
style={
    "padding": "20px"
})

# Callback
@app.callback(
    Output("kpi-card", "children"),
    Output("bar-chart", "figure"),
    Output("line-chart", "figure"),
    Input("category-filter", "value")
)
def update_dashboard(selected_category):

    filtered_df = df

    if selected_category != "All":
        filtered_df = df[
            df["magnitude_category"] == selected_category
        ]

    # KPI
    kpi = f"Total Earthquakes: {len(filtered_df)}"

    # Bar Chart
    category_counts = (
        filtered_df["magnitude_category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "Magnitude Category",
        "Count"
    ]

    bar_fig = px.bar(
        category_counts,
        x="Magnitude Category",
        y="Count",
        title="Earthquakes by Magnitude Category"
    )

    # Line Chart
    daily_counts = (
        filtered_df
        .groupby(filtered_df["event_time"].dt.date)
        .size()
        .reset_index(name="Count")
    )

    line_fig = px.line(
        daily_counts,
        x="event_time",
        y="Count",
        title="Earthquakes Over Time"
    )

    return kpi, bar_fig, line_fig


if __name__ == "__main__":
    app.run(debug=True)