{{ config(
    materialized = 'table',
) }}

WITH dim_product AS (

    SELECT
        ref_num AS product_id,
        category,
        sku,
        CURRENT_TIMESTAMP() AS created_at
    FROM
        {{ ref('stg_sales_processed') }}
),
unique_rows AS (
    SELECT
        *,
        ROW_NUMBER() over (
            PARTITION BY product_id
            ORDER BY
                created_at DESC
        ) AS row_num
    FROM
        dim_product
)
SELECT
    *
FROM
    unique_rows
WHERE
    row_num = 1
