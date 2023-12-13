import pandas as pd
from google.cloud import bigquery


def us_sale_df(client: bigquery.Client) -> pd.DataFrame:
    query = """
    --sql
    SELECT * 
    FROM `us-sale-project.us_sale_dataset.obt`;
    """
    return client.query(query).result().to_dataframe()


def load_us_sale_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, engine="pyarrow")
