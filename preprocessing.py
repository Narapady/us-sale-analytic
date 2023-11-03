from pathlib import Path

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


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


def authenticate_bigquery(cred_file: str):
    # Create credentials with the service account file and initialize a BigQuery client
    credentials = service_account.Credentials.from_service_account_file(cred_file)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client


def create_table_bigquery(client: bigquery.Client, dataset_id: str, table_id: str):
    ...


def load_to_bigquery(
    client: bigquery.Client, dataset_id: str, table_id: str, file_path: str
):
    # Set the dataset and table where you want to upload the CSV file

    # Create a job configuration
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )

    # Load the CSV file to BigQuery
    load_job = client.load_table_from_uri(
        file_path, f"{dataset_id}.{table_id}", job_config=job_config
    )

    load_job.result()  # Wait for the job to complete

    destination_table = client.get_table(f"{dataset_id}.{table_id}")
    print(f"Loaded {destination_table.num_rows} rows.")


def main():
    dataset_id = "us_sale_dataset"
    table_id = "sales_processed"
    preprocess("sales.csv")


if __name__ == "__main__":
    main()
