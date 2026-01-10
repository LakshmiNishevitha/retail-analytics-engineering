select
  {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_key,
  product_id,
  sku,
  product_name,
  brand,
  category,
  cost,
  active_flag
from {{ ref('stg_products') }}
