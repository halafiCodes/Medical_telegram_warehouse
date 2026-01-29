with source as (
    select * from {{ source('raw', 'telegram_messages') }}
)
select
    message_id::int as message_id,
    channel_name::text as channel_name,
    message_text::text as message_text,
    message_date::timestamp as message_date,
    coalesce(views, 0)::int as view_count,
    coalesce(forwards, 0)::int as forward_count,
    length(message_text) as message_length,
    coalesce(has_media, false)::boolean as has_image,
    image_path::text as image_path,
    source_channel::text as source_channel
from source
where message_id is not null
    and channel_name is not null
    and message_date is not null