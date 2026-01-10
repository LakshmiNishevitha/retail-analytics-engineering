select
  order_id,
  customer_id,
  store_id,
  order_ts::timestamp_ntz as order_ts,
  status,
  ingested_at
from RETAIL_DW.RAW.ORDERS_RAW