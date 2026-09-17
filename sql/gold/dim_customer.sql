
-- DIM_CUSTOMER TABLE 

CREATE TABLE IF NOT EXISTS dim_customer (
	customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    segment VARCHAR(50)
);
