with scd as (
  select
    {{ dbt_utils.generate_surrogate_key(['customer_id','dbt_valid_from']) }} as customer_key,
    customer_id,
    full_name,
    email,
    phone,
    address_line1,
    city,
    state,
    zip,
    dbt_valid_from,
    dbt_valid_to,
    case when dbt_valid_to is null then true else false end as is_current
  from {{ ref('snap_customers') }}
),

unknown as (
  select
    {{ dbt_utils.generate_surrogate_key(["'UNKNOWN'","'1900-01-01'"]) }} as customer_key,
    'UNKNOWN' as customer_id,
    'Unknown Customer' as full_name,
    null as email,
    null as phone,
    null as address_line1,
    null as city,
    null as state,
    null as zip,
    '1900-01-01'::timestamp_ntz as dbt_valid_from,
    null::timestamp_ntz as dbt_valid_to,
    true as is_current
)

select * from scd
union all
select * from unknown
