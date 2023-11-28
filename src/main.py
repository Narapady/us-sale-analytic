from dash import Dash
from dash.dependencies import Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP

from bq_etl import bigquery_client
from components.layout import create_layout
from data.data_loader import us_sale_df


def main():
    cred_filepath = "/Users/narapadychhuoy/Repos/us_sale/us-sale-cred.json"
    client = bigquery_client(cred_filepath)
    data = us_sale_df(client)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.layout = create_layout(app, data)
    app.run(debug=True)


if __name__ == "__main__":
    main()
