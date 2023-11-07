{{ config(
    materialized = 'table',
) }}

WITH dim_customer AS (

    SELECT
        customer_id,
        first_name,
        last_name,
        middle_initial,
        gender,
        age,
        email,
        customer_since,
        ssn,
        phone,
        county,
        city,
        state,
        zip,
        region,
        user_name,
        CURRENT_TIMESTAMP() AS created_at
    FROM
        {{ ref('stg_sales_processed') }}
),
unique_rows AS (
    SELECT
        *,
        ROW_NUMBER() over (
            PARTITION BY customer_id
            ORDER BY
                created_at DESC
        ) AS row_num
    FROM
        dim_customer
)
SELECT
    *
FROM
    unique_rows
WHERE
    row_num = 1
