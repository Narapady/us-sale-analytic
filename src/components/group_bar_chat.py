import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(Output("gender_sale", "figure"), Input("group-bar-dropdown", "value"))
    def update_group_barchat(year):
        df = data[["total_amount", "gender", "category", "year"]]
        df = df[df["year"] == year]
        fig = px.histogram(
            df,
            x="category",
            y="total_amount",
            color="gender",
            barmode="group",
            height=400,
        )
        return fig

    return html.Div(
        children=[
            html.H3("Female Vs Male Purchases"),
            dcc.Dropdown(data["year"].unique().tolist(), 2020, id="group-bar-dropdown"),
            dcc.Graph(
                id="gender_sale",
            ),
        ],
        style={"padding": 10, "display": "inline-block", "flex": 1},
    )
