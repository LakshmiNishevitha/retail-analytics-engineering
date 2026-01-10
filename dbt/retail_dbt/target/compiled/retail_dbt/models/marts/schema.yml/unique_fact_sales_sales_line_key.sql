
    
    

select
    sales_line_key as unique_field,
    count(*) as n_records

from RETAIL_DW.STAGING_ANALYTICS.fact_sales
where sales_line_key is not null
group by sales_line_key
having count(*) > 1


