select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select sales_line_key
from RETAIL_DW.STAGING_ANALYTICS.fact_sales
where sales_line_key is null



      
    ) dbt_internal_test