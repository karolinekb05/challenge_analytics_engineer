DROP TABLE IF EXISTS dim_domain CASCADE;

CREATE TABLE dim_domain (
    id UUID PRIMARY KEY DEFAULT get_random_uuid(),
    domain_code VARCHAR(60) NOT NULL,
    domain_name VARCHAR(100) NOT NULL,
    domain_description TEXT,
    parent_domain_id UUID REFERENCES dim_domain(id),
    level INT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 