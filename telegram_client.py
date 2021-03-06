import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class TelegramClient:
    def __init__(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot{}/".format(token)

    def send_message(self, chat_id, text):
        params = {
            "text": text,
            "chat_id": chat_id,
            "parse_mode": "MarkdownV2"
        }
        requests.get(self.url + "sendMessage", params=params)

    def send_file(self, chat_id, path):
        params = {
            "chat_id": chat_id
        }
        files = {
            "document": open(path, "rb"),
        }
        response = requests.post(
            self.url + "sendDocument",
            files=files,
            params=params
        )
        if response.status_code == 200:
            logger.info("Uploaded file")
        else:
            logger.error("Failed to upload file")
        logger.debug(response)
