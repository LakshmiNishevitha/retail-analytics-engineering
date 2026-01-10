select
  snapshot_date as date_key,
  {{ dbt_utils.generate_surrogate_key(['store_id']) }} as store_key,
  {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_key,
  store_id,
  product_id,
  on_hand_qty
from {{ ref('stg_inventory_snapshots') }}
