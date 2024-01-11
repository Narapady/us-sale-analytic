import pandas as pd
import sqlalchemy


def preprocessed_data(file_path: str) -> pd.DataFrame:
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
    return df


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
