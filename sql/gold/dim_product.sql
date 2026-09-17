
-- DIM_PRODUCT TABLE

CREATE TABLE IF NOT EXISTS dim_product (
	product_key INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50)
);
