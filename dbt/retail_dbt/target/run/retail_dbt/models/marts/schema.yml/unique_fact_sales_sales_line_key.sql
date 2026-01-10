select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    sales_line_key as unique_field,
    count(*) as n_records

from RETAIL_DW.STAGING_ANALYTICS.fact_sales
where sales_line_key is not null
group by sales_line_key
having count(*) > 1



      
    ) dbt_internal_test