
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select store_key
from RETAIL_DW.STAGING_ANALYTICS.dim_store
where store_key is null



  
  
      
    ) dbt_internal_test