from bq_etl import bigquery_client
from components.layout import create_layout
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
from data.data_loader import us_sale_df


def main():
    cred_filepath = "/Users/narapadychhuoy/Repos/us_sale/us-sale-cred.json"
    client = bigquery_client(cred_filepath)
    data = us_sale_df(client)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "US Sales Dashboard"
    app.layout = create_layout(app, data)
    app.run()


if __name__ == "__main__":
    main()