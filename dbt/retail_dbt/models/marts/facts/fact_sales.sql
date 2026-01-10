with oi as (
  select * from {{ ref('stg_order_items') }}
),
o as (
  select * from {{ ref('stg_orders') }}
),
j as (
  select
    oi.order_id,
    oi.product_id,
    o.customer_id,
    o.store_id,
    o.order_ts,
    o.status,
    oi.qty,
    oi.unit_price,
    oi.discount_pct,
    (oi.qty * oi.unit_price) as gross_sales,
    (oi.qty * oi.unit_price) * (oi.discount_pct/100.0) as discount_amount,
    (oi.qty * oi.unit_price) - ((oi.qty * oi.unit_price) * (oi.discount_pct/100.0)) as net_sales
  from oi
  join o using (order_id)
),

dim as (
  select
    customer_key,
    customer_id,
    dbt_valid_from,
    dbt_valid_to,
    is_current
  from {{ ref('dim_customer') }}
),

unknown as (
  select customer_key
  from {{ ref('dim_customer') }}
  where customer_id = 'UNKNOWN'
  qualify row_number() over (order by customer_key) = 1
)

select
  {{ dbt_utils.generate_surrogate_key(['j.order_id','j.product_id']) }} as sales_line_key,
  cast(j.order_ts as date) as date_key,

  {{ dbt_utils.generate_surrogate_key(['j.store_id']) }} as store_key,
  {{ dbt_utils.generate_surrogate_key(['j.product_id']) }} as product_key,

  coalesce(c_hist.customer_key, c_curr.customer_key, u.customer_key) as customer_key,

  j.order_id,
  j.product_id,
  j.customer_id,
  j.store_id,
  j.status,

  j.qty,
  j.unit_price,
  j.discount_pct,
  j.gross_sales,
  j.discount_amount,
  j.net_sales
from j

-- 1) Best match: as-of join to the correct SCD2 version
left join dim c_hist
  on j.customer_id = c_hist.customer_id
 and cast(j.order_ts as date) >= cast(c_hist.dbt_valid_from as date)
 and (
      cast(j.order_ts as date) < cast(c_hist.dbt_valid_to as date)
      or c_hist.dbt_valid_to is null
 )
 and c_hist.customer_id <> 'UNKNOWN'

-- 2) Fallback: current version if as-of didn't match
left join dim c_curr
  on j.customer_id = c_curr.customer_id
 and c_curr.is_current = true
 and c_curr.customer_id <> 'UNKNOWN'

-- 3) Final fallback: UNKNOWN row (ensures NOT NULL)
cross join unknown u
