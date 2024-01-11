from google.cloud import bigquery
import pandas as pd


class BigqueryClient:
    def __init__(self, service_account: str, data: pd.DataFrame) -> None:
        self.service_account = service_account
        self.data = data

    def client(self) -> bigquery.Client:
        """
        creates a BigQuery client from a service account JSON file.

        Parameters:
        cred_file (str): The path to the service account JSON file.

        Returns:
        bigquery.Client: The BigQuery client.
        """
        return bigquery.Client.from_service_account_json(self.service_account)

    def create_table(self, dataset_id: str, table_id: str):
        """
        creates a new table in BigQuery.

        Parameters:
        client (bigquery.Client): The BigQuery client.
        dataset_id (str): The ID of the dataset where the table will be created.
        table_id (str): The ID of the table to be created.

        Returns:
        bigquery.Table: The created table.
        None: If an error occurred while creating the table.
        """

        try:
            table_ref = self.client().dataset(dataset_id).table(table_id)
            if not self.client().get_table(table_ref):
                table = bigquery.Table(table_ref)
                return self.client().create_table(table)
            else:
                print("Table already exists.")
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")
            return None

    def generate_schema(self, df: pd.DataFrame):
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

    def load(self, dataset_id: str, table_id: str):
        """
        loads a preprocessed CSV file to a BigQuery table.

        Parameters:
        client (bigquery.Client): The BigQuery client.
        dataset_id (str): The ID of the dataset where the table will be created.
        table_id (str): The ID of the table to be created.

        Returns:
        None
        """

        # Set the dataset and table where you want to upload the CSV file
        schema = self.generate_schema(self.data)

        # Create a job configuration
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
        )

        load_job = self.client().load_table_from_dataframe(
            self.data, f"{dataset_id}.{table_id}", job_config=job_config
        )
        load_job.result()

    def run(self, dataset_id: str, table_id: str):
        if self.create_table(dataset_id, table_id):
            self.load(dataset_id, table_id)
