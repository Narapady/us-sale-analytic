import pandas as pd
from dash import Dash, html

from . import bar_chart, group_bar_chat, pie_chart, table


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            html.H1(app.title, "app-title"),
            html.Hr(),
            table.render(app, data),
            html.Hr(),
            bar_chart.render(app, data),
            group_bar_chat.render(app, data),
            html.Div(
                [
                    pie_chart.render(app, data),
                    pie_chart.render(app, data, "F"),
                    pie_chart.render(app, data, "M"),
                ],
                style={"display": "flex"},
            ),
        ],
    )
