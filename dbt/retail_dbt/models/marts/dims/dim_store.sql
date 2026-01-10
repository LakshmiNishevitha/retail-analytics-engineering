select
  {{ dbt_utils.generate_surrogate_key(['store_id']) }} as store_key,
  store_id,
  store_name,
  city,
  state,
  region
from {{ ref('stg_stores') }}
