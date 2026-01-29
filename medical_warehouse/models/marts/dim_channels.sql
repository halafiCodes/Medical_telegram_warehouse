select
    md5(channel_name) as channel_key,
    channel_name,
    min(message_date) as first_post_date,
    max(message_date) as last_post_date,
    count(message_id) as total_posts
from {{ ref('stg_telegram_messages') }}
group by 1, 2