# Silver Data Quality Report

`02_quality_report.ipynb` profiles the `bronze_sales` MySQL table before Silver-layer cleaning. It is a read-only quality audit: the notebook prints its findings and does not modify the database or create an output file.

## Purpose

The report helps identify issues that must be handled by the Silver transformation, including:

- Missing values and duplicate records
- Invalid order and shipping dates
- Shipping dates earlier than order dates
- Negative or zero sales values
- Unexpected category and geography values
- Leading or trailing whitespace in text fields
- Missing postal codes
- Duplicate or unexpected `row_id` values

## Prerequisites

1. Start MySQL and create the Bronze table using [`sql/bronze/init_bronze_table.sql`](../../sql/bronze/init_bronze_table.sql).
2. Load source data into `bronze_sales` with [`01_load_bronze.py`](../bronze/01_load_bronze.py).
3. Install the notebook dependencies:

   ```bash
   pip install pandas sqlalchemy pymysql python-dotenv jupyter
   ```

4. Create a `.env` file in the project root. Do not commit this file.

   ```env
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DATABASE=DataWarehouse
   ```

## Run the report

Open [`02_quality_report.ipynb`](02_quality_report.ipynb) in VS Code or Jupyter and run the cells from top to bottom.

The notebook:

1. Loads database settings from `.env`.
2. Creates and tests a SQLAlchemy MySQL connection.
3. Reads all rows from `bronze_sales`.
4. Prints a basic profile of the dataset.
5. Runs date, sales, category, whitespace, postal-code, and `row_id` checks.

From the project root, it can also be opened with:

```bash
jupyter notebook scripts/silver/02_quality_report.ipynb
```

## Quality Issue Remediation Matrix

| Rule ID | Quality Issue               | Evidence                                                     | Business Rule                                  | Remediation             | Validation                              |
| ------- | --------------------------- | ------------------------------------------------------------ | ---------------------------------------------- | ----------------------- | --------------------------------------- |
| DQ-001  | Missing postal codes        | 11 records (0.112%)                                          | Do not fabricate missing geographic data       | Preserve as `NULL`      | Missing count remains 11                |
| DQ-002  | Dates stored as strings     | `order_date` and `ship_date` are strings in Bronze           | Silver dates must use proper `DATE` type       | Convert to datetime     | No invalid dates after conversion       |
| DQ-003  | Duplicate full rows         | 0                                                            | Silver should not contain exact duplicates     | `drop_duplicates()`     | Duplicate count = 0                     |
| DQ-004  | Duplicate `row_id`          | 0                                                            | `row_id` must uniquely identify source records | No remediation required | `row_id.nunique() == len(df)`           |
| DQ-005  | Invalid dates               | 0                                                            | All dates must be valid                        | No remediation required | Invalid date count = 0                  |
| DQ-006  | Ship date before order date | 0                                                            | `ship_date >= order_date`                      | No remediation required | Violations = 0                          |
| DQ-007  | Invalid sales               | No negative/zero values                                      | Sales must be positive                         | No remediation required | `(sales <= 0).sum() == 0`               |
| DQ-008  | Text whitespace             | None                                                         | Text should be consistently formatted          | No remediation required | No whitespace issues                    |
| DQ-009  | Invalid categorical values  | None                                                         | Categories must use expected values            | No remediation required | All values belong to expected sets      |
| DQ-010  | Sales precision             | Values include 4 decimal places; Silver uses `DECIMAL(12,2)` | Monetary values should use 2-decimal precision | Round to 2 decimals     | `sales` conforms to 2-decimal precision |
| DQ-011  | Repeated `order_id`         | 4,878 repeated values                                        | Multiple product lines may belong to one order | **Do not remove**       | `row_id` remains unique                 |



## Expected Bronze columns

The report expects the columns created by the Bronze loader:

```text
row_id, order_id, order_date, ship_date, ship_mode,
customer_id, customer_name, segment, country, city, state,
postal_code, region, product_id, category, sub_category,
product_name, sales, ingestion_timestamp, source_file_name, load_id
```

## Interpreting results

- Invalid dates should be corrected or quarantined during Silver processing.
- A shipping date earlier than an order date is a date-logic failure.
- Negative sales values generally require investigation before analytics use.
- Missing postal codes may be acceptable for some records but should be documented.
- Duplicate `row_id` values should be investigated because `row_id` is expected to identify a source row.
- Category and geography counts should be compared with the source-system domain values.

## Relationship to the Silver layer

The Silver table definition is in [`sql/silver/init_silver_table.sql`](../../sql/silver/init_silver_table.sql). It stores parsed dates, standardized fields, derived date attributes, and a processing timestamp.

At present, this notebook reads `bronze_sales` directly. After the Silver cleaning script is implemented, the report should be extended or copied to validate `silver_sales` and compare Bronze-versus-Silver quality results.

## Troubleshooting

- **Connection error:** verify that MySQL is running and that the `.env` values match the local database.
- **Unknown table:** run the Bronze SQL initialization and ingestion steps first.
- **Missing column error:** confirm that the Bronze table uses the expected snake_case column names.
- **Notebook install issue:** select the Python interpreter or virtual environment where `pandas`, `sqlalchemy`, `pymysql`, and `python-dotenv` are installed.
