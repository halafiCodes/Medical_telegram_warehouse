select
    m.message_id,
    c.channel_key,
    to_char(m.message_date, 'YYYYMMDD')::int as date_key,
    m.view_count,
    m.forward_count
from {{ ref('stg_telegram_messages') }} m
join {{ ref('dim_channels') }} c on m.channel_name = c.channel_name
join {{ ref('dim_dates') }} d on to_char(m.message_date, 'YYYYMMDD')::int = d.date_key