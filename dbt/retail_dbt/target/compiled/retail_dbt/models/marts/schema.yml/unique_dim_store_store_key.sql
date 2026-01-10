
    
    

select
    store_key as unique_field,
    count(*) as n_records

from RETAIL_DW.STAGING_ANALYTICS.dim_store
where store_key is not null
group by store_key
having count(*) > 1


