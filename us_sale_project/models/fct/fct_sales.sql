{{ config(
    materialized = 'table',
) }}

WITH fct_sales AS (

    SELECT
        item_id AS order_id,
        ref_num AS product_id,
        date_id,
        customer_id,
        qty_ordered AS quantity,
        price AS unit_price,
        VALUE,
        total AS total_amount,
        discount_amount,
        discount_percent,
        CURRENT_TIMESTAMP() AS created_at
    FROM
        {{ ref('stg_sales_processed') }}
        s
        LEFT JOIN {{ ref('dim_date') }}
        d
        ON s.order_date = d.date_id
),
unique_rows AS (
    SELECT
        *,
        ROW_NUMBER() over (
            PARTITION BY order_id,
            product_id,
            customer_id,
            date_id
        ) AS row_num
    FROM
        fct_sales
)
SELECT
    ROW_NUMBER() over() AS sale_id,*
FROM
    unique_rows
WHERE
    row_num = 1
