{% snapshot snapshot_sales_processed %}
    {{ config(
        target_database = 'us-sale-project',
        target_schema = 'us_sale_dataset',
        unique_key = 'item_id',
        strategy = 'timestamp',
        updated_at = 'updated_at',
        invalidate_hard_deletes = true
    ) }}

    SELECT
        *
    FROM
        {{ ref('stg_sales_processed') }}
{% endsnapshot %}
