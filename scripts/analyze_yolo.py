import os
from sqlalchemy import create_engine, text

DB_URL = os.environ.get(
    "MEDICAL_DW_URL",
    "postgresql://postgres:1234@localhost:5434/medical_dw",
)
engine = create_engine(DB_URL)

with engine.connect() as conn:
    q1 = text(
        """
        select d.image_category,
               count(*) as n,
               avg(m.view_count) as avg_views
        from analytics.fct_image_detections d
        join analytics.fct_messages m
          on m.message_id = d.message_id
        group by d.image_category
        order by n desc
        """
    )
    print("avg_views_by_category")
    for row in conn.execute(q1).fetchall():
        print(row)

    q2 = text(
        """
        select channel_name,
               count(*) as total_msgs,
               sum(case when has_image then 1 else 0 end) as image_msgs,
               round(100.0 * sum(case when has_image then 1 else 0 end) / count(*), 2) as pct_with_image
        from analytics.stg_telegram_messages
        group by channel_name
        order by pct_with_image desc, total_msgs desc
        """
    )
    print("image_usage_by_channel")
    for row in conn.execute(q2).fetchall():
        print(row)
