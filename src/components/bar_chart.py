import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    df = data.groupby("state")["total_amount"].sum().reset_index()
    fig = px.bar(df, x="state", y="total_amount", color="state")
    return html.Div(
        children=[
            html.H3("Top Total Sales By States"),
            dcc.Graph(id="sales-by-states", figure=fig),
        ],
    )
