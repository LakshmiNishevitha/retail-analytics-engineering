select
  store_id,
  store_name,
  city,
  state,
  region,
  updated_at::timestamp_ntz as updated_at,
  ingested_at
from {{ source('raw', 'STORES_RAW') }}
