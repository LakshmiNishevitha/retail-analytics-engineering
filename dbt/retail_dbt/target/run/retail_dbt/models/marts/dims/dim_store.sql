
  
    

        create or replace transient table RETAIL_DW.STAGING_ANALYTICS.dim_store
         as
        (select
  md5(cast(coalesce(cast(store_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as store_key,
  store_id,
  store_name,
  city,
  state,
  region
from RETAIL_DW.STAGING_STAGING.stg_stores
        );
      
  