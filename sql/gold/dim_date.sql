
-- DIM_DATE TABLE

CREATE TABLE IF NOT EXISTS dim_date (
	date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    day INT,
    day_name VARCHAR(20)
);
