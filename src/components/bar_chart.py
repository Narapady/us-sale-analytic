import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from components.color import BG_COLOR, FG_COLOR


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(Output("selected_col", "figure"), Input("barchart-dropdown", "value"))
    def update_barchat(selected):
        df = (
            data.groupby(selected)["total_amount"]
            .sum()
            .round(2)
            .reset_index()
            .sort_values(by="total_amount", ascending=False)
            .head(10)
        )
        fig = px.bar(
            df,
            x=selected,
            y="total_amount",
            color=selected,
            color_discrete_sequence=px.colors.qualitative.T10,
        )
        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font_color=FG_COLOR,
            xaxis_title=str(selected).capitalize(),
            yaxis_title="Total Sale",
        )
        return fig

    return html.Div(
        children=[
            html.H3("TOP 10 TOTAL SALES", style={"color": FG_COLOR}),
            dcc.Dropdown(
                options=[
                    {"label": "state", "value": "state"},
                    {"label": "city", "value": "city"},
                    {"label": "region", "value": "region"},
                    {"label": "county", "value": "county"},
                    {"label": "category", "value": "category"},
                    {"label": "gender", "value": "gender"},
                    {"label": "payment_method", "value": "payment_method"},
                ],
                value="state",
                id="barchart-dropdown",
                style={"backgroundColor": BG_COLOR, "color": FG_COLOR},
            ),
            dcc.Graph(id="selected_col"),
        ],
        style={
            "padding": 10,
            "display": "inline-block",
            "flex": 1,
            "backgroundColor": BG_COLOR,
        },
    )
