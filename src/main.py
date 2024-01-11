from elt.bigquery import BigqueryClient
from components.layout import create_layout
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from data.data_loader import us_sale_df


def main():
    # NOTE: load data from BigQuery
    cred_filepath = "/Users/narapadychhuoy/Repos/us_sale/us-sale-cred.json"
    bigquery = BigqueryClient(cred_filepath)
    client = bigquery.client()

    data = us_sale_df(client)

    # # NOTE: Load data from local file
    # data = load_us_sale_data("./src/data/obt.csv")

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "US SALE DASBOARD"
    app.layout = create_layout(app, data)
    app.run(debug=True)


if __name__ == "__main__":
    main()
