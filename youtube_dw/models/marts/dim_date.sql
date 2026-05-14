select distinct
    fetched_at::date                    as date_day,
    extract(year from fetched_at)       as year,
    extract(month from fetched_at)      as month,
    extract(day from fetched_at)        as day,
    to_char(fetched_at, 'Day')          as day_name,
    to_char(fetched_at, 'Month')        as month_name
from {{ ref('stg_youtube_trending') }}