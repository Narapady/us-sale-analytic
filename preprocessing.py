from pathlib import Path

import pandas as pd
from google.cloud import bigquery


def rename_columns(df: pd.DataFrame):
    """
    This function renames the columns of a DataFrame.
    It  splits the column names by space and joins them with an underscore.
    If the column name is a single word, it is converted to lowercase.

    Parameters:
    df (pd.DataFrame): The DataFrame whose columns are to be renamed.

    Returns:
    list[str]: The list of renamed column names.
    """

    cols: list[str] = []
    for col in df.columns:
        split_col = col.split(" ")
        if len(split_col) == 2:
            cols.append(f"{split_col[1].lower()}_{split_col[1].lower()}")
        else:
            cols.append(f"{split_col[0].lower()}")
    return cols


def preprocess(file_path: str):
    """
    This function preprocesses the data from a given file path.
    It reads the data, modifies the column names, and changes
    the data types of certain columns. The preprocessed data is
    then saved to a new CSV file.

    Parameters:
    file_path (str): The path to the file to be preprocessed.

    Returns:
    None
    """
    df = pd.read_csv(file_path)
    df.columns = rename_columns(df)

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["qty_ordered"] = df["qty_ordered"].astype("int64")
    df["customer_since"] = pd.to_datetime(df["customer_since"])
    df["zip"] = df["zip"].astype("str")
    df["age"] = df["age"].astype("int64")
    df["cust_id"] = df["cust_id"].astype("int64")

    df.to_csv("sales_preprocessed.csv", index=False)


def bigquery_client(cred_file: str):
    """
    This function creates a BigQuery client from a service account JSON file.

    Parameters:
    cred_file (str): The path to the service account JSON file.

    Returns:
    bigquery.Client: The BigQuery client.
    """
    client = bigquery.Client.from_service_account_json(cred_file)
    return client


def create_table_bigquery(client: bigquery.Client, dataset_id: str, table_id: str):
    """
    This function creates a new table in BigQuery.

    Parameters:
    client (bigquery.Client): The BigQuery client.
    dataset_id (str): The ID of the dataset where the table will be created.
    table_id (str): The ID of the table to be created.

    Returns:
    bigquery.Table: The created table.
    None: If an error occurred while creating the table.
    """
    try:
        table_ref = client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref)
        return client.create_table(table)
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        return None


def generate_schema(df: pd.DataFrame) -> list:
    """
    This function generates a schema for a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame for which the schema is to be generated.

    Returns:
    list: The list of SchemaField objects.
    """
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
    return schema


def load_to_bigquery(client: bigquery.Client, dataset_id: str, table_id: str):
    """
    This function loads a preprocessed CSV file to a BigQuery table.

    Parameters:
    client (bigquery.Client): The BigQuery client.
    dataset_id (str): The ID of the dataset where the table will be created.
    table_id (str): The ID of the table to be created.

    Returns:
    None
    """
    # Set the dataset and table where you want to upload the CSV file
    df = pd.read_csv("sales_preprocessed.csv")
    schema = generate_schema(df)

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
    # Define the path to the service account key
    service_account_key_path = Path.cwd() / "us-sale-cred.json"
    # Create a BigQuery client using the service account key
    client = bigquery_client(service_account_key_path)
    dataset_id = "us_sale_dataset"  # Define the dataset ID
    table_id = "sales_processed"  # Define the table ID
    preprocess("sales.csv")  # Preprocess the sales.csv file
    # If the table is successfully created in BigQuery
    if create_table_bigquery(client, dataset_id, table_id) is not None:
        # Load the preprocessed data to the BigQuery table
        load_to_bigquery(client, dataset_id, table_id)


if __name__ == "__main__":
    main()
