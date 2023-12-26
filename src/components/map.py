import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html, dash_table
from components.color import BG_COLOR, FG_COLOR


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    def sale_diff_by_region(data: pd.DataFrame) -> pd.DataFrame:
        df = data.groupby(["year", "region"])["total_amount"].sum().reset_index()
        df = df.pivot(index="region", columns="year", values="total_amount")
        df["diff"] = df[2021] - df[2020]
        df = df.sort_values(by="diff", ascending=False).reset_index()
        return df

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
            color_discrete_sequence=px.colors.qualitative.Dark24,
            width=1300,  # Bigger size
            height=1100,  # Bigger size
        )
        fig.update_layout(
            plot_bgcolor=BG_COLOR,
            paper_bgcolor=BG_COLOR,
            legend=dict(bgcolor=BG_COLOR, font_color=FG_COLOR),
        )
        fig.update_geos(
            bgcolor=BG_COLOR,
            showcountries=True,
            countrycolor=FG_COLOR,
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
                    dash_table.DataTable(
                        data=sale_diff_by_region(data).to_dict("records"),
                        columns=[
                            {"name": "Region", "id": "region"},
                            {"name": "2020", "id": "2020"},
                            {"name": "2021", "id": "2021"},
                            {"name": "Diff", "id": "diff"},
                        ],
                        style_table={
                            "color": FG_COLOR,
                        },
                        style_as_list_view=True,
                        style_cell={"padding": "10px"},
                        style_header={
                            "backgroundColor": BG_COLOR,
                            "fontWeight": "bold",
                        },
                        style_data_conditional=[
                            {"if": {"row_index": "odd"}, "backgroundColor": BG_COLOR},
                            {"if": {"row_index": "even"}, "backgroundColor": BG_COLOR},
                        ],
                    ),
                ]
            ),
            dcc.Graph("map"),
        ],
        style={"padding": 10, "display": "flex", "flex": 1},
    )
