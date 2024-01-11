import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from src.components.color import BG_COLOR, COMPONENT_COLOR, FG_COLOR


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
        fig = px.pie(
            df,
            values="total_amount",
            names="month_name",
            color_discrete_sequence=px.colors.qualitative.T10,
        )
        fig.update_layout(
            plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR, font_color=FG_COLOR
        )
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
            html.H3(piechart_title, style={"color": COMPONENT_COLOR}),
            dcc.RadioItems(
                options=[
                    {"label": " 2020 ", "value": 2020},
                    {"label": " 2021 ", "value": 2021},
                ],
                labelStyle={"display": "inline-block", "margin-right": "20px"},
                value=2020,
                id=f"piechart-dropdown-{filter}",
                style={
                    "backgroundColor": BG_COLOR,
                    "color": FG_COLOR,
                    "display": "inline-flex",
                },
            ),
            dcc.Graph(f"pie-chart-{filter}"),
        ],
        style={"padding": 10, "display": "inline-block", "flex": 1},
    )
