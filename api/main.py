from typing import List
from datetime import date

from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import database, schemas

app = FastAPI(title="Medical Business Insights API")

@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}

@app.get(
    "/api/reports/top-products",
    response_model=List[schemas.ProductCount],
    summary="Top mentioned products",
    description="Returns the most frequently mentioned product terms across all channels.",
)
def top_products(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of products to return."),
    db: Session = Depends(database.get_db),
):
    sql = text("SELECT message_text as product_name, count(*) as mention_count "
               "FROM analytics.fct_messages GROUP BY message_text "
               "ORDER BY mention_count DESC LIMIT :limit")
    return db.execute(sql, {"limit": limit}).fetchall()

@app.get(
    "/api/channels/{channel_name}/activity",
    response_model=List[schemas.ChannelActivity],
    summary="Channel activity over time",
    description="Returns posting activity by date for a specific channel.",
)
def channel_activity(
    channel_name: str = Path(..., min_length=1, description="Channel name to analyze."),
    db: Session = Depends(database.get_db),
):
    sql = text(
        "SELECT channel_name, date_key, count(*) as message_count "
        "FROM analytics.fct_messages m "
        "JOIN analytics.dim_channels c ON m.channel_key = c.channel_key "
        "WHERE c.channel_name = :channel_name "
        "GROUP BY channel_name, date_key "
        "ORDER BY date_key"
    )
    rows = db.execute(sql, {"channel_name": channel_name}).fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Channel not found or no activity.")
    return rows

@app.get(
    "/api/search/messages",
    response_model=List[schemas.MessageSearchResult],
    summary="Search messages",
    description="Searches messages for a keyword across all channels.",
)
def search_messages(
    query: str = Query(..., min_length=2, description="Keyword to search for."),
    limit: int = Query(20, ge=1, le=200, description="Maximum results to return."),
    db: Session = Depends(database.get_db),
):
    sql = text(
        "SELECT m.message_id, c.channel_name, m.message_date::text as message_date, m.message_text "
        "FROM analytics.stg_telegram_messages m "
        "JOIN analytics.dim_channels c ON m.channel_name = c.channel_name "
        "WHERE m.message_text ILIKE :q "
        "ORDER BY m.message_date DESC "
        "LIMIT :limit"
    )
    rows = db.execute(sql, {"q": f"%{query}%", "limit": limit}).fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="No messages found for query.")
    return rows

@app.get(
    "/api/reports/visual-content",
    response_model=List[schemas.VisualStats],
    summary="Visual content stats",
    description="Returns image usage statistics by channel and image category.",
)
def visual_stats(db: Session = Depends(database.get_db)):
    sql = text(
        "SELECT c.channel_name, d.image_category, count(*) as total_count "
        "FROM analytics.fct_image_detections d "
        "JOIN analytics.dim_channels c ON d.channel_key = c.channel_key "
        "GROUP BY c.channel_name, d.image_category"
    )
    return db.execute(sql).fetchall()