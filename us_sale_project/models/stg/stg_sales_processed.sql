WITH source AS (
    SELECT
        *
    FROM
        {{ source(
            'us_sale',
            'sales_processed'
        ) }}
),
renamed AS (
    SELECT
        {{ adapter.quote("order_id") }},
        CAST({{ adapter.quote("order_date") }} AS DATE) AS {{ adapter.quote("order_date") }},
        {{ adapter.quote("status") }},
        CAST({{ adapter.quote("item_id") }} AS INTEGER) AS {{ adapter.quote("item_id") }},
        {{ adapter.quote("sku") }},
        {{ adapter.quote("qty_ordered") }},
        {{ adapter.quote("price") }},
        {{ adapter.quote("value") }},
        {{ adapter.quote("discount_amount") }},
        {{ adapter.quote("total") }},
        {{ adapter.quote("category") }},
        {{ adapter.quote("payment_method") }},
        {{ adapter.quote("bi_st") }},
        {{ adapter.quote("cust_id") }} AS {{ adapter.quote("customer_id") }},
        {{ adapter.quote("year") }},
        SUBSTR({{ adapter.quote("month") }}, 1, 3) AS {{ adapter.quote("month") }},
        {{ adapter.quote("ref_num") }},
        {{ adapter.quote("name_prefix") }},
        {{ adapter.quote("first_name") }},
        {{ adapter.quote("middle_initial") }},
        {{ adapter.quote("last_name") }},
        {{ adapter.quote("gender") }},
        {{ adapter.quote("age") }},
        {{ adapter.quote("full_name") }},
        {{ adapter.quote("e_mail") }} AS {{ adapter.quote("email") }},
        CAST({{ adapter.quote("customer_since") }} AS DATE) AS {{ adapter.quote("customer_since") }},
        {{ adapter.quote("ssn") }},
        {{ adapter.quote("phone") }},
        {{ adapter.quote("place_name") }},
        {{ adapter.quote("county") }},
        {{ adapter.quote("city") }},
        {{ adapter.quote("state") }},
        {{ adapter.quote("zip") }},
        {{ adapter.quote("region") }},
        {{ adapter.quote("user_name") }},
        {{ adapter.quote("discount_percent") }},
        CURRENT_TIMESTAMP() {{ adapter.quote("updated_at")}}
    FROM
        source
)
SELECT
    *
FROM
    renamed
