select
    video_id,
    title,
    channel_id,
    category_id,
    fetched_at::date    as date_day,
    view_count,
    like_count,
    comment_count,
    region_code
from {{ ref('stg_youtube_trending') }}