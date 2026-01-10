select
  md5(cast(coalesce(cast(product_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as product_key,
  product_id,
  sku,
  product_name,
  brand,
  category,
  cost,
  active_flag
from RETAIL_DW.STAGING_STAGING.stg_products