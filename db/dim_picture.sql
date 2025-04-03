DROP TABLE IF EXISTS dim_picture CASCADE;

CREATE TABLE dim_picture (
    id UUID PRIMARY KEY DEFAULT get_random_uuid(),
    product_id VARCHAR(25) REFERENCES fact_product(product_id),
    picture_code VARCHAR(50) NOT NULL,
    url TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 