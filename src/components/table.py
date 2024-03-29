import pandas as pd
from dash import Dash, dash_table, html
from src.components.color import BG_COLOR, COMPONENT_COLOR, FG_COLOR


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        [
            html.H3(
                "US Sales Dataset (First 10 Rows)", style={"color": COMPONENT_COLOR}
            ),
            dash_table.DataTable(
                data=data.head(10).to_dict("records"),
                columns=[{"name": i, "id": i} for i in data.columns],
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
    )
