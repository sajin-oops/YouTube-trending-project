select distinct
    category_id,
    region_code
from {{ ref('stg_youtube_trending') }}