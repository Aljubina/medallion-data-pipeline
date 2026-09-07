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

| Quality Issue                  | Evidence                                                                                                            | Business Rule                                                                                            | Remediation                                                                                                                       | Validation                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Missing values                 | The notebook prints null counts for every column.                                                                   | Required business fields must not be null.                                                               | Fill values using an approved default where appropriate; otherwise quarantine the record for review.                              | Re-run the null-count check and confirm that required fields have zero nulls.               |
| Duplicate records              | The notebook prints the number of duplicate full rows.                                                              | Each source transaction should be represented once.                                                      | Remove exact duplicate rows while preserving the original source record and load metadata.                                        | Confirm that `df.duplicated().sum()` returns zero.                                          |
| Duplicate `row_id` values      | The notebook prints duplicate `row_id` count and the identifier range.                                              | `row_id` should uniquely identify a source row.                                                          | Investigate conflicting records and retain the valid record or assign a controlled surrogate key.                                 | Confirm that duplicate `row_id` values are resolved and the identifier range is documented. |
| Invalid order dates            | The notebook prints the number of `order_date` values that fail date parsing.                                       | Every valid order must have a parseable order date.                                                      | Parse the source date using the expected day-first format; quarantine values that cannot be converted.                            | Confirm that the invalid order-date count is zero in the cleaned dataset.                   |
| Invalid ship dates             | The notebook prints the number of `ship_date` values that fail date parsing.                                        | Every shipped order must have a parseable ship date.                                                     | Parse the source date using the expected day-first format; quarantine values that cannot be converted.                            | Confirm that the invalid ship-date count is zero in the cleaned dataset.                    |
| Invalid date sequence          | The notebook counts rows where `ship_date` is earlier than `order_date`.                                            | A shipment cannot occur before its order.                                                                | Correct the dates from the source when possible; otherwise quarantine the record.                                                 | Confirm that `ship_date >= order_date` for all retained records.                            |
| Negative sales                 | The notebook prints the count of negative `sales` values.                                                           | Sales amounts must not be negative unless an approved return or credit process exists.                   | Investigate the source transaction and correct, reclassify, or quarantine the value.                                              | Confirm that no unauthorized negative sales remain.                                         |
| Zero sales                     | The notebook prints the count of `sales` values equal to zero.                                                      | A sales transaction should have a positive amount unless zero-value transactions are explicitly allowed. | Confirm whether the row is a valid free item, cancelled order, or source error; then retain or quarantine it according to policy. | Confirm that remaining zero-sales rows are documented and approved.                         |
| Leading or trailing whitespace | The notebook checks every text column for values that change after `strip()`.                                       | Text attributes must be normalized for reliable joins, grouping, and filtering.                          | Trim leading and trailing whitespace from string columns.                                                                         | Re-run the whitespace check and confirm no unapproved whitespace remains.                   |
| Missing postal codes           | The notebook prints all rows with a null `postal_code`.                                                             | Postal code should be populated when available, but missing geography must not be fabricated.            | Preserve the null or use a verified source value; do not infer an unsupported postal code.                                        | Confirm missing postal-code rows are counted and documented.                                |
| Unexpected categorical values  | The notebook prints distributions for ship mode, segment, region, category, sub-category, country, city, and state. | Categorical values must match the approved source-system domain.                                         | Standardize spelling and casing, map known aliases, and quarantine values outside the approved domain.                            | Compare distinct cleaned values with the approved domain lists.                             |
| Incorrect data types           | The notebook prints source data types, while Bronze stores dates as text.                                           | Silver dates and measures must use analytics-ready data types.                                           | Convert dates to `DATE` and sales to a numeric decimal type in the Silver layer.                                                  | Confirm Silver schema types and verify that conversion errors are zero.                     |

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
