import pandas as pd
from dash import Dash, dash_table, dcc, html


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-table",
        children=[
            html.H3("US Sales Dataset (First 20 Rows))"),
            dash_table.DataTable(
                data.head(20).to_dict("records"),
                [{"name": i, "id": i} for i in data.columns],
                style_table={"overflowX": "auto"},
            ),
        ],
    )
