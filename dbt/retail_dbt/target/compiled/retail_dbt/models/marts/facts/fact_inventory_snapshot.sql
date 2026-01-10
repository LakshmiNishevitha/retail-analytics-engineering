select
  snapshot_date as date_key,
  md5(cast(coalesce(cast(store_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as store_key,
  md5(cast(coalesce(cast(product_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as product_key,
  store_id,
  product_id,
  on_hand_qty
from RETAIL_DW.STAGING_STAGING.stg_inventory_snapshots