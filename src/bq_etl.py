from pathlib import Path
import pandas as pd
import sqlalchemy
from google.cloud import bigquery


def preprocessed_data(file_path: str):
    """
    This function preprocesses the data from a given file path.
    It reads the data, modifies the column names, and changes
    the data types of certain columns. The preprocessed data is
    then saved to a new CSV file. then it return the dataframe

    Parameters:
    file_path (str): The path to the file to be preprocessed.

    Returns: DataFrame
    """

    def rename_columns(df: pd.DataFrame):
        cols: list[str] = []
        for col in df.columns:
            split_col = col.split(" ")
            if len(split_col) == 2:
                cols.append(f"{split_col[0].lower()}_{split_col[1].lower()}")
            else:
                cols.append(f"{split_col[0].lower()}")
        return cols

    df = pd.read_csv(file_path)
    df.columns = rename_columns(df)

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["qty_ordered"] = df["qty_ordered"].astype("int64")
    df["customer_since"] = pd.to_datetime(df["customer_since"])
    df["zip"] = df["zip"].astype("str")
    df["age"] = df["age"].astype("int64")
    df["cust_id"] = df["cust_id"].astype("int64")
    df.to_csv("sales_preprocessed.csv", index=False)


def bigquery_client(cred_file: str) -> bigquery.Client:
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

    def generate_schema(df: pd.DataFrame):
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


def load_to_postgres(df: pd.DataFrame):
    # Create an engine instance
    alchemy_engine = sqlalchemy.create_engine(
        "postgresql+psycopg2://narapadychhuoy@localhost/postgres", pool_recycle=3600
    )

    # Connect to PostgreSQL server
    db_connection = alchemy_engine.connect()

    # Create table (if it doesn't exist) and write DataFrame into PostgreSQL
    df.to_sql("us_sales", db_connection, if_exists="replace", index=False)

    # Close the database connection
    db_connection.close()


def main():
    csv_file_path = Path.cwd() / "dataset/sales.csv"
    dataset_id = "us_sale_dataset"  # Define the dataset ID
    table_id = "sales_processed"  # Define the table ID

    data = preprocessed_data(csv_file_path)  # Preprocess the sales.csv file
    # load data to postgres
    load_to_postgres(data)

    # Define the path to the service account key
    service_account_key_path = Path.cwd() / "us-sale-cred.json"

    # Create a BigQuery client using the service account key
    client = bigquery_client(service_account_key_path)

    # If the table is successfully created in BigQuery
    if create_table_bigquery(client, dataset_id, table_id):
        # Load the preprocessed data to the BigQuery table
        load_to_bigquery(client, dataset_id, table_id)


if __name__ == "__main__":
    main()
