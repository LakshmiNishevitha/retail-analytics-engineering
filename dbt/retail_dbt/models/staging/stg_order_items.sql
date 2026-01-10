select
  order_id,
  product_id,
  qty::number as qty,
  unit_price::number(10,2) as unit_price,
  discount_pct::number(5,2) as discount_pct,
  ingested_at
from {{ source('raw', 'ORDER_ITEMS_RAW') }}
