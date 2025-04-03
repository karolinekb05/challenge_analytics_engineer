DROP TABLE IF EXISTS dim_setting CASCADE;

CREATE TABLE dim_setting (
    id UUID PRIMARY KEY DEFAULT get_random_uuid(),
    product_id VARCHAR(25) REFERENCES fact_product(product_id),
    listing_strategy_code VARCHAR(50) NOT NULL,
    listing_strategy_name VARCHAR(100) NOT NULL,
    exclusive BOOLEAN NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 