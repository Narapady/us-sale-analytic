{{ config(
    materialized = 'table'
) }}

SELECT
    s.sale_id,
    o.order_id,
    o.order_date,
    o.order_status,
    o.payment_method,
    p.product_id,
    p.category,
    p.sku,
    d.date_id,
    d.year,
    d.month,
    d.year_week,
    d.year_day,
    d.fiscal_year,
    d.fiscal_qtr,
    d.month_name,
    d.week_day,
    d.day_name,
    d.day_is_weekday,
    c.customer_id,
    s.quantity,
    s.unit_price,
    s.value,
    s.total_amount,
    s.discount_amount,
    s.discount_percent,
    c.first_name,
    c.last_name,
    c.gender,
    c.age,
    c.email,
    c.customer_since,
    c.phone,
    c.county,
    c.city,
    c.state,
    c.zip,
    c.region,
    CURRENT_TIMESTAMP() as updated_at
FROM {{ ref("fct_sales")}} s
    JOIN {{ ref("dim_customer")}} c ON s.customer_id = c.customer_id
    JOIN {{ ref("dim_order")}}  o ON s.order_id = o.order_id
    JOIN {{ ref ("dim_product")}} p ON s.product_id = p.product_id
    JOIN {{ ref("dim_date")}} d on s.date_id = d.date_id
