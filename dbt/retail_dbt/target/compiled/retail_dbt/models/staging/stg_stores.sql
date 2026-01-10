select
  store_id,
  store_name,
  city,
  state,
  region,
  updated_at::timestamp_ntz as updated_at,
  ingested_at
from RETAIL_DW.RAW.STORES_RAW