DROP TABLE IF EXISTS fact_product CASCADE;

CREATE TABLE fact_product (
    id UUID PRIMARY KEY DEFAULT get_random_uuid(),
    product_id VARCHAR(50) NOT NULL UNIQUE,
    date_id UUID REFERENCES dim_date(id),
    catalog_product_id VARCHAR(50),
    status_id UUID REFERENCES dim_status(id),
    domain_id UUID REFERENCES dim_domain(id),
    name TEXT NOT NULL,
    children_ids TEXT[],
    quality_type VARCHAR(50),
    priority VARCHAR(50),
    type VARCHAR(50),
    site_id VARCHAR(50),
    keywords TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
