
# Import libraries

import pandas as pd  # Read and work with CSV/DataFrame
from datetime import datetime  # Generate ingestion timestamp
import uuid   #generates unique load_id
from sqlalchemy import create_engine # connect python to mysql
from pathlib import Path

# path
csv_path = "../../data/bronze/train.csv"

#  read csv
df = pd.read_csv(csv_path)

print(df)


# useful checks 
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())

print(df.isnull().sum())

# add metadata 

''' 
MYSQL TABLE HAS
    - ingestion_timestamp  : Generate the timestamp when the pipeline runs.
    - source_file_name 
    - load_id 
'''

# 1. Ingestion timestamp
ingestion_timestamp = datetime.now()
df["ingestion_timestamp"] = ingestion_timestamp

# testing 
print(df[["ingestion_timestamp"]].tail())
df.info()

# 2. Source file name
source_file_name = Path(csv_path).name
df["source_file_name"] = source_file_name

# testing
print(df[["source_file_name"]].tail())

#  3. Load Id
load_id = str(uuid.uuid4())
df["load_id"] = load_id

#  testing metadata
print(df[[
    "ingestion_timestamp",
    "source_file_name",
    "load_id"
]].head())


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

print(df.columns)


print("DataFrame columns:")
print(df.columns.tolist())