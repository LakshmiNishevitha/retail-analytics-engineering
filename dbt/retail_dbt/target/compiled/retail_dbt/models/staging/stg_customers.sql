select
  customer_id,
  full_name,
  email,
  phone,
  address_line1,
  city,
  state,
  zip,
  updated_at::timestamp_ntz as updated_at,
  ingested_at
from RETAIL_DW.RAW.CUSTOMERS_RAW