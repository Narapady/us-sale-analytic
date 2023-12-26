from operator import xor
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from components.color import BG_COLOR, COMPONENT_COLOR, FG_COLOR


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(Output("gender_sale", "figure"), Input("group-bar-dropdown", "value"))
    def update_group_barchat(year):
        df = data[["total_amount", "gender", "category", "year"]]
        df = df[df["year"] == year]
        fig = px.histogram(
            data_frame=df,
            x="category",
            y="total_amount",
            color="gender",
            barmode="group",
            height=400,
            color_discrete_sequence=px.colors.qualitative.T10,
        )
        fig.update_layout(
            xaxis_title="Product Category",
            yaxis_title="Total Sale",
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            font_color=FG_COLOR,
        )
        return fig

    return html.Div(
        children=[
            html.H3("MALE/FEMALE TOTAL PURCHASE", style={"color": COMPONENT_COLOR}),
            dcc.Dropdown(
                data["year"].unique().tolist(),
                2020,
                id="group-bar-dropdown",
                style={"backgroundColor": BG_COLOR, "color": BG_COLOR},
            ),
            dcc.Graph(
                id="gender_sale",
            ),
        ],
        style={"padding": 10, "display": "inline-block", "flex": 1},
    )
