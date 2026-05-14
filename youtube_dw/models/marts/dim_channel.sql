select distinct
    channel_id,
    channel_title
from {{ ref('stg_youtube_trending') }}