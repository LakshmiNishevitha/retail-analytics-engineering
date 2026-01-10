
  create or replace   view RETAIL_DW.STAGING_STAGING.stg_products
  
   as (
    select
  product_id,
  sku,
  product_name,
  brand,
  category,
  cost::number(10,2) as cost,
  active_flag,
  updated_at::timestamp_ntz as updated_at,
  ingested_at
from RETAIL_DW.RAW.PRODUCTS_RAW
  );

