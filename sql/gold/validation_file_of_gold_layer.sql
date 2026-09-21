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


-- ============= VALIDATE CUSTOMER ================== --

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_customer_ids
FROM dim_customer;

-- total_rows = unique_customer_ids -- 

-- Check Nulls --
SELECT *
FROM dim_customer
WHERE customer_id IS NULL
   OR customer_name IS NULL
   OR segment IS NULL;

-- ================ VALIDATE PRODUCT ===================== --

SELECT
    COUNT(*) AS total_product_records,
    COUNT(DISTINCT product_id) AS unique_product_ids,
    COUNT(DISTINCT product_name) AS unique_product_names
FROM dim_product;
	
    
-- product id present more than 1's    -- 
SELECT
    product_id,
    COUNT(DISTINCT product_name) AS product_name_count
FROM dim_product
GROUP BY product_id
HAVING COUNT(DISTINCT product_name) > 1;

-- check null -- 
SELECT *
FROM dim_product
WHERE product_id IS NULL
   OR product_name IS NULL
   OR category IS NULL
   OR sub_category IS NULL;

   
   
-- ========== VALIDATE LOCATION ========= --

SELECT
    COUNT(*) AS total_locations,
    COUNT(DISTINCT CONCAT_WS('|',
        country,
        city,
        state,
        postal_code,
        region
    )) AS unique_locations
FROM dim_location;

-- CHECK NULL -- 
SELECT *
FROM dim_location
WHERE country IS NULL
   OR city IS NULL
   OR state IS NULL
   OR region IS NULL;
   
-- MISSING POSTAL CODES -- 
SELECT COUNT(*) AS missing_postal_codes
FROM dim_location
WHERE postal_code IS NULL;

