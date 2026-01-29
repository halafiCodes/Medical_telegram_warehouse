with yolo as (
    select *
    from {{ ref('stg_yolo') }}
),

messages as (
    select message_id, channel_key, date_key
    from {{ ref('fct_messages') }}
)

select
    m.message_id,
    m.channel_key,
    m.date_key,
    y.detected_class,
    y.confidence_score,
    y.image_category
from yolo y
join messages m
    on y.message_id = m.message_id
where m.message_id is not null
  and y.detected_class is not null