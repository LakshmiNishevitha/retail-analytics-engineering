select
  order_id,
  customer_id,
  store_id,
  order_ts::timestamp_ntz as order_ts,
  status,
  ingested_at
from {{ source('raw', 'ORDERS_RAW') }}
