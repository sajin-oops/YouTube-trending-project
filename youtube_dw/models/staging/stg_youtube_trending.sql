with source as (
    select * from raw.youtube_trending
),

cleaned as (
    select
        video_id,
        title,
        channel_id,
        channel_title,
        category_id::integer     as category_id,
        published_at::timestamp  as published_at,
        view_count,
        like_count,
        comment_count,
        duration,
        fetched_at::timestamp    as fetched_at,
        region_code
    from source
)

select * from cleaned