import os
import json
import logging
from datetime import datetime
from pathlib import Path
import sys

from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

load_dotenv()


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

CHANNELS = [
    "lobelia4cosmetics",
    'tikvahpharma',
    "CheMed123"
    
]

BASE_DATA_PATH = Path("data/raw")
MESSAGE_PATH = BASE_DATA_PATH / "telegram_messages"
IMAGE_PATH = BASE_DATA_PATH / "images"
LOG_PATH = Path("logs")

MESSAGE_PATH.mkdir(parents=True, exist_ok=True)
IMAGE_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)


logging.basicConfig(
    filename=LOG_PATH / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def scrape_channel(channel_name):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    channel_dir = MESSAGE_PATH / today
    channel_dir.mkdir(parents=True, exist_ok=True)

    messages_data = []

    logging.info(f"Starting scrape for channel: {channel_name}")

    async for message in tqdm(client.iter_messages(channel_name, limit=500), total=500):
        msg_dict = {
            "message_id": message.id,
            "channel_name": channel_name,
            "message_date": message.date.isoformat() if message.date else None,
            "message_text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
            "image_path": None
        }

        if isinstance(message.media, MessageMediaPhoto):
            channel_image_dir = IMAGE_PATH / channel_name
            channel_image_dir.mkdir(parents=True, exist_ok=True)

            image_file = channel_image_dir / f"{message.id}.jpg"
            await message.download_media(file=image_file)

            msg_dict["image_path"] = str(image_file)

        messages_data.append(msg_dict)

    json_file = channel_dir / f"{channel_name}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=2)

    logging.info(f"Finished scrape for channel: {channel_name}")
    logging.info(f"Saved {len(messages_data)} messages")


async def main():
    await client.start()
    for channel in CHANNELS:
        try:
            await scrape_channel(channel)
        except Exception as e:
            logging.error(f"Error scraping {channel}: {e}")

    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
