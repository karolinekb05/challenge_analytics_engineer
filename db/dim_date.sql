DROP TABLE IF EXISTS dim_date CASCADE;

CREATE TABLE dim_date (
    id UUID PRIMARY KEY DEFAULT get_random_uuid(),
    date_created TIMESTAMP NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL,
    day_of_week INT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 