DROP TABLE IF EXISTS dim_attribute CASCADE;

CREATE TABLE dim_attribute (
    id UUID PRIMARY KEY DEFAULT get_random_uuid(),
    product_id VARCHAR(25) REFERENCES fact_product(product_id),
    attribute_code VARCHAR(50) NOT NULL,
    attribute_name VARCHAR(100) NOT NULL,
    value_id VARCHAR(50),
    value_name TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 