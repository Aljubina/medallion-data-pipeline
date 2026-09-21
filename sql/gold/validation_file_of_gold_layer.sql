-- Gold Layer Validation --

USE DataWarehouse;

SELECT 'dim_customer' AS table_name, COUNT(*) AS row_count
FROM dim_customer

UNION ALL

SELECT 'dim_product', COUNT(*)
FROM dim_product

UNION ALL

SELECT 'dim_location', COUNT(*)
FROM dim_location

UNION ALL

SELECT 'dim_date', COUNT(*)
FROM dim_date

UNION ALL

SELECT 'fact_sales', COUNT(*)
FROM fact_sales;


/* RESULT
dim_customer 793
dim_product	1893
dim_location	628
dim_date	1230
fact_sales	9800
*/

