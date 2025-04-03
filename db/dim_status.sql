DROP TABLE IF EXISTS dim_status CASCADE;

CREATE TABLE dim_status (
    id UUID PRIMARY KEY DEFAULT get_random_uuid(),
    status_code CHAR(10) NOT NULL,
    status_name VARCHAR(50) NOT NULL,
    status_description TEXT,
    is_active BOOLEAN DEFAULT true,
    product_id VARCHAR(25) REFERENCES fact_product(product_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 