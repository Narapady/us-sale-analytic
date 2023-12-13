CREATE TABLE us_sale_obt (
    sale_id INTEGER,
    order_id INTEGER,
    order_date DATE,
    order_status VARCHAR(20),
    payment_method VARCHAR(20),
    product_id INTEGER,
    category VARCHAR(50),
    sku VARCHAR(255),
    date_id DATE,
    year INTEGER,
    month INTEGER,
    year_week INTEGER,
    year_day INTEGER,
    fiscal_year INTEGER,
    fiscal_qtr INTEGER,
    month_name VARCHAR(20),
    week_day VARCHAR(20),
    day_name VARCHAR(20),
    day_is_weekday BOOLEAN,
    customer_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(10, 2),
    value NUMERIC(10, 2),
    total_amount NUMERIC(10, 2),
    discount_amount NUMERIC(10, 2),
    discount_percent NUMERIC(5, 2),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender CHAR(1),
    age INTEGER,
    email VARCHAR(100),
    customer_since DATE,
    phone VARCHAR(20),
    county VARCHAR(50),
    city VARCHAR(50),
    state CHAR(2),
    zip VARCHAR(10),
    region VARCHAR(20),
    updated_at TIMESTAMP
);
