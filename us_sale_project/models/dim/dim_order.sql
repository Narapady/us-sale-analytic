{{ config(
    materialized = 'table',
) }}

WITH dim_order AS (

    SELECT
        order_id,
        order_date,
        status AS order_status,
        item_id,
        payment_method,
        CURRENT_TIMESTAMP() AS created_at
    FROM
        {{ ref('stg_sales_processed') }}
),
unique_rows AS (
    SELECT
        *,
        ROW_NUMBER() over (
            PARTITION BY order_id,
            order_date,
            order_status,
            item_id,
            payment_method
            ORDER BY
                created_at DESC
        ) AS row_num
    FROM
        dim_order
)
SELECT
    *
FROM
    unique_rows
WHERE
    row_num = 1
