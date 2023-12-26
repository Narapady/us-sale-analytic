import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from components.color import BG_COLOR, FG_COLOR


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output("map", "figure"),
        Input("map-radio-item", "value"),
    )
    def update_map(year: int):
        df = data[data["year"] == year]
        df = (
            df.groupby(["region", "state", "latitude", "longitude"])["total_amount"]
            .sum()
            .reset_index()
        )

        fig = px.scatter_geo(
            data_frame=df,
            lat="latitude",
            lon="longitude",
            projection="albers usa",
            size="total_amount",
            color="region",
            hover_name="state",
            scope="usa",
            width=1100,  # Bigger size
            height=900,  # Bigger size
        )
        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            width=1200,
            height=1000,
        )
        fig.update_geos(
            bgcolor=BG_COLOR,
            showcountries=True,
            countrycolor=FG_COLOR,
            # framewidth=1000,
            # coastlinewidth=1000,
        )

        return fig

    return html.Div(
        [
            html.Div(
                [
                    html.H3("TOTAL SALE BY REGION", style={"color": FG_COLOR}),
                    dcc.RadioItems(
                        options=[
                            {"label": " 2020 ", "value": 2020},
                            {"label": " 2021 ", "value": 2021},
                        ],
                        value=2020,
                        id="map-radio-item",
                        style={
                            "padding": "10px",
                            "display": "inline-block",
                            "color": FG_COLOR,
                        },
                    ),
                ]
            ),
            dcc.Graph("map"),
        ],
        style={"padding": 10, "display": "flex", "flex": 1},
    )
