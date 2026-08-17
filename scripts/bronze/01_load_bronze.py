
# Import libraries

import os
import pandas as pd  # Read and work with CSV/DataFrame
import uuid   #generates unique load_id
import time
from datetime import datetime  # Generate ingestion timestamp
from dotenv import load_dotenv
from sqlalchemy import create_engine # connect python to mysql
from urllib.parse import quote_plus
from pathlib import Path

# ===================================================================
print("-----------------------------------------------------")
print("START ETL")
print("-----------------------------------------------------")

etl_start = time.perf_counter()

print("READING CSV : ")
start = time.perf_counter()
# path
csv_path = "../../data/bronze/train.csv"

#  read csv
try:
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded CSV: {csv_path}")

except FileNotFoundError:
    print(f"Error: CSV file not found: {csv_path}")

except Exception as e:
    print(f"Error while reading csv file: {e}")

end = time.perf_counter()

print(f"CSV Read Time: {end - start: .2f} seconds")

# ====================================================================
# useful checks 
# print(df.head())
# print(df.shape)
# print(df.columns)
# print(df.info())

# print(df.isnull().sum())

# ======================================================================
# ADD METADATA 

''' 
MYSQL TABLE HAS
    - ingestion_timestamp  : Generate the timestamp when the pipeline runs.
    - source_file_name 
    - load_id 
'''

start = time.perf_counter()

# 1. Ingestion timestamp
ingestion_timestamp = datetime.now()
df["ingestion_timestamp"] = ingestion_timestamp

# testing 
# print(df[["ingestion_timestamp"]].tail())
# df.info()

# 2. Source file name
source_file_name = Path(csv_path).name
df["source_file_name"] = source_file_name

# testing
# print(df[["source_file_name"]].tail())

#  3. Load Id
load_id = str(uuid.uuid4())
df["load_id"] = load_id

#  testing metadata
# print(df[[
#     "ingestion_timestamp",
#     "source_file_name",
#     "load_id"
# ]].head())

end = time.perf_counter()

print(f"Metadata Processing time: {end - start: .2f} seconds")

# renaming
df = df.rename(columns={
    "Row ID": "row_id",
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Ship Date": "ship_date",
    "Ship Mode": "ship_mode",
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Segment": "segment",
    "Country": "country",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "Region": "region",
    "Product ID": "product_id",
    "Category": "category",
    "Sub-Category": "sub_category",
    "Product Name": "product_name",
    "Sales": "sales"
})

# print(df.columns)


# print("DataFrame columns:")
# print(df.columns.tolist())

# ===================================================================

# SQLAlchemy CONNECTION 

start = time.perf_counter()

load_dotenv()

mysql_user = os.getenv("MYSQL_USER")
mysql_password = quote_plus(os.getenv("MYSQL_PASSWORD"))
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_database = os.getenv("MYSQL_DATABASE")


try:
    engine = create_engine(
        f"mysql+pymysql://{mysql_user}:{mysql_password}@"
        f"{mysql_host}:{mysql_port}/{mysql_database}"
    )

    # Test Connection
    with engine.connect() as connection:
        print("Successfully connected to MYSQL !")

except Exception as e:
    print(f"ERROR: Could not connect to MYSQL: {e}")

# Load DataFrame into DataWarehouse-> bronze_sales table

try:
    df.to_sql(
        name = "bronze_sales",
        con = engine,
        if_exists="append",
        index = False
    )
    print(f"Successfully loaded {len(df)} rows into bronze_sales")

except Exception as e:
    print(f"ERROR while loading data into bronze_sales: {e}")

end = time.perf_counter()

print(f"MYSQL Load time: {end - start:.2f} seconds")

# =========================================================
# TOTAL ETL
# =======================================================
etl_end = time.perf_counter()

print(f"Total ETL Time: {etl_end - etl_start:.2f} seconds")

print("-----------------------------------------------------")
print("END ETL")
print("-----------------------------------------------------")