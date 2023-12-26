import pandas as pd
from dash import Dash, html
from components.color import BG_COLOR, TITLE_COLOR

from . import bar_chart, histogram, map, pie_chart, table


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            html.H1(app.title, "app-title", style={"color": TITLE_COLOR}),
            html.Hr(),
            table.render(app, data),
            html.Hr(),
            html.Div(
                [
                    bar_chart.render(app, data),
                    histogram.render(app, data),
                ],
                style={"display": "flex"},
            ),
            html.Div(
                [
                    pie_chart.render(app, data),
                    pie_chart.render(app, data, "F"),
                    pie_chart.render(app, data, "M"),
                ],
                style={"display": "flex"},
            ),
            map.render(app, data),
        ],
        style={
            "padding": "0 2rem",
            "backgroundColor": BG_COLOR,
            "fontFamily": "JetBrains Mono",
        },
    )
