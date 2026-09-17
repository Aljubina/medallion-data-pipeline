
-- FACT_SALES TABLE

CREATE TABLE IF NOT EXISTS fact_sales (
	sales_key INT AUTO_INCREMENT PRIMARY KEY,
    
    row_id INT,
    order_id INT,
    
    date_key INT,
    customer_key INT,
    product_key INT,
    location_key INT,
    
    ship_mode VARCHAR(50),
    ship_date DATE,
    
    sales DECIMAL(12,2)
);
