import pandas as pd


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

def load_to_bigquery():
    pass

def main():
    preprocess("sales.csv")


if __name__ == "__main__":
    main()
