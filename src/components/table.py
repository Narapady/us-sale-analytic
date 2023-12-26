import pandas as pd
from dash import Dash, dash_table, html
from components.color import BG_COLOR, FG_COLOR


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        [
            html.H3("US Sales Dataset (First 20 Rows)", style={"color": FG_COLOR}),
            dash_table.DataTable(
                data.head(20).to_dict("records"),
                [{"name": i, "id": i} for i in data.columns],
                style_table={
                    "overflowX": "auto",
                    "color": FG_COLOR,
                },
                style_as_list_view=True,
                style_cell={"padding": "10px"},
                style_header={"backgroundColor": BG_COLOR, "fontWeight": "bold"},
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": BG_COLOR},
                    {"if": {"row_index": "even"}, "backgroundColor": BG_COLOR},
                ],
            ),
        ],
        className="app-table",
    )
