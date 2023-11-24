import pandas as pd
from google.cloud import bigquery


def us_sale_df(client: bigquery.Client) -> pd.DataFrame:
    query = """
    SELECT * FROM `us-sale-project.us_sale_dataset.obt` LIMIT 100
    """
    return client.query(query).result().to_dataframe()
