import json
import os
import logging

from telegram_client import TelegramClient
from tiktok import download_video
from tiktok import strip_url_params
from tiktok import is_tiktok_url

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

telegram_client = TelegramClient(token=TELEGRAM_TOKEN)


def process_event(event):
    body = json.loads(event['body'])
    logging.info(body)

    if 'message' not in body:
        logging.info("No message in update")
        return

    chat_id = body['message']['chat']['id']

    if 'text' not in body['message']:
        telegram_client.send_message(chat_id, "Please send valid TikTok url")
        return

    text = body['message']['text']

    if text == "/start":
        telegram_client.send_message(chat_id, "Hi! Send me a TikTok link")
        return

    if not is_tiktok_url(text):
        telegram_client.send_message(chat_id, "Please send valid TikTok url")
        return

    url = strip_url_params(text)
    logger.info("Downloading video from %s", url)

    telegram_client.send_message(chat_id, "Downloading your TikTok, please wait a moment")
    video_file = download_video(url)
    telegram_client.send_file(chat_id, video_file)


def lambda_handler(event, context):
    process_event(event)
    return {
        'statusCode': 200
    }
