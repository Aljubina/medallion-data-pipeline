# Medallion Architecture Pipeline with Explicit Data Quality Remediation

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-orange)
![SQL](https://img.shields.io/badge/SQL-Data%20Modelling-green)
![GitHub](https://img.shields.io/badge/Version%20Control-Git-black)

## Project Overview

This project implements a complete **Medallion Architecture** (Bronze → Silver → Gold) data pipeline that transforms raw, messy sales data into a clean, reliable, and analytics-ready **Single Source of Truth**.

The primary focus is on **explicit data quality remediation** in the Silver layer to handle real-world data issues such as null values, duplicates, inconsistent formats, and invalid records.

---

## Project Objective

To design and build an end-to-end batch data pipeline using Medallion Architecture that:

- Ingests raw sales data (Bronze)
- Applies comprehensive data quality rules and standardization (Silver)
- Creates a business-ready dimensional model (Gold)
- Enables trustworthy analytics and reporting

---

## Business Problem

Raw data from source systems is often poor in quality. Common issues include:

- Missing / null values
- Duplicate records
- Inconsistent formatting (e.g., "USA", "US", "United States")
- Invalid values (negative sales/quantity, future dates, etc.)

These problems lead to inaccurate reports and poor business decisions.  
This project solves the problem by creating a structured, high-quality data pipeline.

---

## Architecture

The pipeline follows the **Medallion Architecture**:

| Layer   | Purpose                              | Key Activities                              |
|---------|--------------------------------------|---------------------------------------------|
| Bronze  | Raw data landing zone                | Ingest data as-is + add metadata           |
| Silver  | Cleaned & standardized data          | Data quality remediation + transformation   |
| Gold    | Business-ready analytics layer       | Dimensional modelling (Star Schema)         |

---

## Tech Stack

- **Language**: Python (pandas)
- **Storage**: Local files (CSV / Parquet) + Optional AWS S3
- **Query Engine**: SQL (SQLite / PostgreSQL / Amazon Athena)
- **Version Control**: Git + GitHub
- **Optional**: Power BI / Tableau Public for visualization

---

## Key Features

- Full Medallion Architecture implementation
- Explicit data quality rules in Silver layer
- Handling of nulls, duplicates, inconsistencies, and invalid values
- Star Schema dimensional modelling in Gold layer
- Modular and reproducible pipeline
- Clear documentation and data quality reporting

---

## Project Structure
medallion-data-quality-pipeline/
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── scripts/
│   ├── bronze/
│   │   └── 01_load_bronze.py
│   ├── silver/
│   │   └── 02_clean_silver.py
│   └── gold/
│       └── 03_load_gold.py
├── sql/
│   ├── bronze/
│   ├── silver/
│   │   └── data_quality_checks.sql
│   └── gold/
│       ├── create_dim_customer.sql
│       ├── create_dim_product.sql
│       ├── create_dim_location.sql
│       ├── create_dim_date.sql
│       ├── create_fact_sales.sql
│       └── analytical_queries.sql
├── README.md
└── requirements.txt

---

##  Pipeline Flow

1. **Bronze Layer**  
   - Extract raw CSV data  
   - Add metadata (`ingestion_timestamp`, `source_file_name`)  
   - Store as-is

2. **Silver Layer**  
   - Handle missing values  
   - Remove duplicates  
   - Standardize categorical fields  
   - Fix invalid records (negative values, bad dates)  
   - Correct data types  
   - Create derived columns  
   - Generate Data Quality Report

3. **Gold Layer**  
   - Design Star Schema  
   - Create Fact and Dimension tables  
   - Load analytics-ready data

---
## Data Quality Rules Applied (Silver Layer)

- Handled missing and null values
- Removed duplicate records
- Standardized categorical values (Ship Mode, Segment, Region, etc.)
- Corrected invalid values (e.g. negative sales)
- Fixed data types (dates, numerical columns)
- Created derived columns (Order Year, Order Month, etc.)

---

## Gold Layer – Star Schema

- **Fact Table**: `fact_sales`
- **Dimension Tables**:
  - `dim_customer`
  - `dim_product`
  - `dim_location`
  - `dim_date`

---
## How to Run the Project

### 1. Clone the Repository
```bash
git clone <repository-url>
cd medallion-data-quality-pipeline
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Prepare the Data
Place your raw dataset files inside the data/bronze/ directory before starting the pipeline.

4. Execute the Pipeline
Run the pipeline scripts sequentially:

```bash
# Step 1: Ingest raw data into Bronze layer
python scripts/bronze/01_load_bronze.py

# Step 2: Clean, validate, and write to Silver layer
python scripts/silver/02_clean_silver.py

# Step 3: Transform into Gold layer dimensional models
python scripts/gold/03_load_gold.py
```

5. Data Analysis & Queries
Use the SQL scripts located in the sql/ directory for schema creation, views, and downstream analytical queries:

```bash
# Executable via your database CLI or SQL client
sql/01_create_tables.sql
sql/02_analytical_queries.sql
```

## Deliverables

- Complete Bronze → Silver → Gold pipeline
- Modular Python scripts
- SQL scripts for quality checks and analytics
- Data Quality Report
- Well-documented GitHub repository
- (Optional) Dashboard on Gold layer


## Success Criteria

- Raw data successfully landed in Bronze layer
- Clear improvement in data quality in Silver layer
- Proper Star Schema implemented in Gold layer
- Analytical queries run successfully
- Project is fully reproducible from GitHub
- Architecture and design decisions can be clearly explained


## Scope
In Scope

- Batch ETL pipeline
- Explicit data quality remediation
- Dimensional modelling (Star Schema)
- Optional cloud storage (AWS S3)

Out of Scope

- Real-time streaming
- Advanced orchestration (Airflow, etc.)
- Machine Learning models
- Multiple complex source systems

## Key Learnings

- Understanding of Medallion Architecture
- Practical implementation of data quality rules
- Dimensional modelling using Star Schema
- Building a clean and reproducible data pipeline
- Combining Python and SQL for data engineering tasks

Author
Aljubina Gavit
