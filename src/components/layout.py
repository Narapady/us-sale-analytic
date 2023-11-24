import pandas as pd
from dash import Dash, dcc, html

from . import bar_chart, table


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            html.H1(app.title, "app-title"),
            html.Hr(),
            table.render(app, data),
            html.Hr(),
            bar_chart.render(app, data),
        ],
    )
