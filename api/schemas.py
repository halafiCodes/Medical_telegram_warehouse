from pydantic import BaseModel
from typing import Optional, List

class ProductCount(BaseModel):
    product_name: str
    mention_count: int

class VisualStats(BaseModel):
    channel_name: str
    image_category: str
    total_count: int

class ChannelActivity(BaseModel):
    channel_name: str
    date_key: int
    message_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_date: str
    message_text: str