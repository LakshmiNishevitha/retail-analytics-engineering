{% snapshot snap_customers %}

{{
  config(
    target_schema='ANALYTICS',
    unique_key='customer_id',
    strategy='timestamp',
    updated_at='updated_at'
  )
}}

select
  customer_id,
  full_name,
  email,
  phone,
  address_line1,
  city,
  state,
  zip,
  updated_at
from {{ ref('stg_customers') }}

{% endsnapshot %}
