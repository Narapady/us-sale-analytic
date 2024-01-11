from pathlib import Path
from etl.bigquery import BigqueryClient
from etl.ingest import preprocessed_data, load_to_postgres


def main():
    csv_file_path = Path.cwd() / "dataset/sales.csv"
    dataset_id = "us_sale_dataset"  # Define the dataset ID
    table_id = "sales_processed"  # Define the table ID

    data = preprocessed_data(csv_file_path)  # Preprocess the sales.csv file
    # load data to postgres
    load_to_postgres(data)

    # Define the path to the service account key
    service_account_key_path = Path.cwd() / "us-sale-cred.json"
    biquery = BigqueryClient(service_account_key_path, data)
    biquery.run(dataset_id, table_id)


if __name__ == "__main__":
    main()
