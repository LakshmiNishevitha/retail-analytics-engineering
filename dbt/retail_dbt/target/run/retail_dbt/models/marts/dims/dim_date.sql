
  
    

        create or replace transient table RETAIL_DW.STAGING_ANALYTICS.dim_date
         as
        (with dates as (
  select dateadd(day, seq4(), '2025-01-01'::date) as date_day
  from table(generator(rowcount => 3650))
)
select
  date_day as date_key,
  year(date_day) as year,
  month(date_day) as month,
  day(date_day) as day,
  dayofweek(date_day) as day_of_week,
  weekofyear(date_day) as week_of_year
from dates
        );
      
  