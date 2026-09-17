
--  DIM_LOCATION TABLE

CREATE TABLE IF NOT EXISTS dim_location (
	location_key INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(50),
    region VARCHAR(50)
);
