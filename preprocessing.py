from pathlib import Path

import pandas as pd
from google.cloud import bigquery


def preprocess(file_path: str):
    df = pd.read_csv(file_path)
    cols = []
    for col in df.columns:
        split_col = col.split(" ")
        if len(split_col) == 2:
            cols.append(f"{split_col[0].lower()}_{split_col[1].lower()}")
        else:
            cols.append(f"{split_col[0].lower()}")

    df.columns = cols
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["qty_ordered"] = df["qty_ordered"].astype("int64")
    df["customer_since"] = pd.to_datetime(df["customer_since"])
    df["zip"] = df["zip"].astype("str")
    df["age"] = df["age"].astype("int64")
    df["cust_id"] = df["cust_id"].astype("int64")

    df.to_csv("sales_preprocessed.csv", index=False)


def bigquery_client(cred_file: str):
    client = bigquery.Client.from_service_account_json(cred_file)
    return client


def create_table_bigquery(client: bigquery.Client, dataset_id: str, table_id: str):
    try:
        table_ref = client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref)
        return client.create_table(table)
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        return None


def load_to_bigquery(client: bigquery.Client, dataset_id: str, table_id: str):
    # Set the dataset and table where you want to upload the CSV file
    df = pd.read_csv("sales_preprocessed.csv")

    schema = [
        bigquery.SchemaField(col, "integer")
        if df[col].dtype == "int64"
        else bigquery.SchemaField(col, "float")
        if df[col].dtype == "float64"
        else bigquery.SchemaField(col, "string")
        if df[col].dtype == "object"
        else bigquery.SchemaField(col, "timestamp")
        if df[col].dtype == "datetime64"
        else None
        for col in df.columns
    ]
    # Create a job configuration
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
    )

    load_job = client.load_table_from_dataframe(
        df, f"{dataset_id}.{table_id}", job_config=job_config
    )
    load_job.result()


def main():
    service_account_key_path = Path.cwd() / "us-sale-cred.json"
    client = bigquery_client(service_account_key_path)
    dataset_id = "us_sale_dataset"
    table_id = "sales_processed"
    preprocess("sales.csv")
    if create_table_bigquery(client, dataset_id, table_id) is not None:
        load_to_bigquery(client, dataset_id, table_id)


if __name__ == "__main__":
    main()
