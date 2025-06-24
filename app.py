import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(url)
df["Period"] = df["Recession"].map({1: "Recession", 0: "Non-Recession"})

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Automobile Sales Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id="report-dropdown",
            options=[
                {"label": "Recession Report", "value": "recession"},
                {"label": "Yearly Report", "value": "yearly"}
            ],
            value="recession"
        )
    ], style={'width': '40%', 'margin': 'auto'}),

    html.Div(id="output-container", className="output-area"),

    dcc.Graph(id="main-graph-1"),
    dcc.Graph(id="main-graph-2")
])

# Callback to update content based on dropdown
@app.callback(
    Output("output-container", "children"),
    Output("main-graph-1", "figure"),
    Output("main-graph-2", "figure"),
    Input("report-dropdown", "value")
)
def update_output(report_type):
    if report_type == "recession":
        recession_data = df[df["Recession"] == 1]
        output_msg = "Displaying statistics during Recession period"

        # Plot 1: Sales by Year (Recession)
        fig1 = px.line(
            recession_data.groupby("Year")["Automobile_Sales"].sum().reset_index(),
            x="Year", y="Automobile_Sales",
            title="Total Automobile Sales During Recession"
        )

        # Plot 2: Ad Spend vs Sales by Vehicle Type
        fig2 = px.scatter(
            recession_data,
            x="Advertising_Expenditure", y="Automobile_Sales",
            color="Vehicle_Type",
            size="Automobile_Sales",
            title="Ad Spend vs Sales (Recession Period)"
        )

    else:
        yearly_sales = df.groupby("Year")["Automobile_Sales"].sum().reset_index()
        avg_price = df.groupby("Year")["Price"].mean().reset_index()
        output_msg = "Displaying Yearly Automobile Statistics"

        # Plot 1: Yearly Sales
        fig1 = px.line(
            yearly_sales,
            x="Year", y="Automobile_Sales",
            title="Yearly Automobile Sales"
        )

        # Plot 2: Average Price by Year
        fig2 = px.bar(
            avg_price,
            x="Year", y="Price",
            title="Average Vehicle Price by Year"
        )

    return output_msg, fig1, fig2

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

