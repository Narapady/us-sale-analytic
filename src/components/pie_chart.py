import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


def render(app: Dash, data: pd.DataFrame, filter="") -> html.Div:
    if filter:
        data = data[data["gender"] == filter]

    @app.callback(
        Output(f"pie-chart-{filter}", "figure"),
        Input(f"piechart-dropdown-{filter}", "value"),
    )
    def update_piechart(selected_year: int):
        df = data[data["year"] == selected_year]
        df = (
            df.groupby("month_name")["total_amount"]
            .sum()
            .reset_index()
            .sort_values(by="total_amount", ascending=True)
        )
        fig = px.pie(df, values="total_amount", names="month_name")
        return fig

    piechart_title = (
        "Sale By Year (All Gender)"
        if filter == ""
        else "Sale By Year (Male)"
        if filter == "M"
        else "Sale By Year (Female)"
    )
    return html.Div(
        [
            html.H3(piechart_title),
            dcc.Dropdown([2020, 2021], 2020, id=f"piechart-dropdown-{filter}"),
            dcc.Graph(f"pie-chart-{filter}"),
        ],
        style={"padding": 10, "display": "inline-block", "flex": 1},
    )
