import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# 1. LOAD ENVIRONMENT VARIABLES

load_dotenv()

mysql_user = os.getenv("MYSQL_USER")
mysql_password = quote_plus(os.getenv("MYSQL_PASSWORD"))
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_database = os.getenv("MYSQL_DATABASE")

# 2. CREATE MYSQL CONNECTION

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

# ==============================================
# 3. READ BRONZE TABLE
# ==============================================

df = pd.read_sql(
    "SELECT * FROM bronze_sales",
    engine
)


# 4. VERIFY DATA

print("Bronze Data loaded successfully !!")

print("Rows:", len(df))

print("Columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nUnique values:")
print(df.nunique())

print("\nSales statistics:")
print(df["sales"].describe())


# ================================
# 5. Profiling Checks
