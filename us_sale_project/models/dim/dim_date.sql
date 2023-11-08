{{ config(
    materialized='table'
)}}

SELECT
    CAST(FORMAT_DATE('%F', d) AS DATE) AS date_id,
    CAST(FORMAT_DATE('%F', d) AS DATE) AS date,
    EXTRACT(YEAR FROM d) AS year,
    EXTRACT(MONTH FROM d) AS month,
    EXTRACT(WEEK FROM d) AS year_week,
    EXTRACT(DAY FROM d) AS year_day,
    EXTRACT(YEAR FROM d) AS fiscal_year,
    FORMAT_DATE('%Q', d) AS fiscal_qtr,
    FORMAT_DATE('%B', d) AS month_name,
    FORMAT_DATE('%w', d) AS week_day,
    FORMAT_DATE('%A', d) AS day_name,
    (CASE WHEN FORMAT_DATE('%A', d) IN ('Sunday', 'Satuaday') THEN 0 ELSE 1 END) AS day_is_weekday,
FROM
  (SELECT * FROM UNNEST(GENERATE_DATE_ARRAY('2020-01-01','2050-01-01', INTERVAL 1 DAY)) AS d)