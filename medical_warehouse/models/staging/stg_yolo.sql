with raw as (
    select *
    from {{ source('raw', 'yolo_detections_raw') }}
)

select
    message_id::int as message_id,
    detected_class::text as detected_class,
    confidence_score::float as confidence_score,
    image_category::text as image_category,
    image_name::text as image_name
from raw
where message_id is not null
  and detected_class is not null
    and confidence_score is not null
