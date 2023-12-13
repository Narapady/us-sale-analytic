import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(Output("selected_col", "figure"), Input("barchart-dropdown", "value"))
    def update_barchat(selected):
        df = (
            data.groupby(selected)["total_amount"]
            .sum()
            .reset_index()
            .sort_values(by="total_amount", ascending=False)
            .head(10)
        )
        fig = px.bar(df, x=selected, y="total_amount", color=selected)
        return fig

    return html.Div(
        children=[
            html.H3("Top 10 Total Sales Amount"),
            dcc.Dropdown(
                [
                    "state",
                    "city",
                    "region",
                    "county",
                    "category",
                    "gender",
                    "payment_method",
                ],
                "state",
                id="barchart-dropdown",
            ),
            dcc.Graph(id="selected_col"),
        ],
        style={"padding": 10, "display": "inline-block", "flex": 1},
    )
