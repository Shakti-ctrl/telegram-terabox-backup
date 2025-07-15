import os
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterVideo
from terabox_uploader import upload_file

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
channel = os.environ['CHANNEL_USERNAME']
email = os.environ['TERABOX_EMAIL']
password = os.environ['TERABOX_PASSWORD']

client = TelegramClient('session', api_id, api_hash)
client.start()

def alpha_folder(filename):
    first = filename[0].upper()
    return first if 'A' <= first <= 'Z' else 'Others'

with client:
    for msg in client.iter_messages(channel, filter=InputMessagesFilterVideo):
        path = msg.download_media()
        if path:
            folder = alpha_folder(os.path.basename(path))
            os.makedirs(folder, exist_ok=True)
            new_path = os.path.join(folder, os.path.basename(path))
            os.rename(path, new_path)
            upload_file(new_path, f"Telegram_Backup/{folder}/{os.path.basename(path)}", email, password)
            os.remove(new_path)

    for msg in client.iter_messages(channel, filter=InputMessagesFilterDocument):
        path = msg.download_media()
        if path:
            folder = alpha_folder(os.path.basename(path))
            os.makedirs(folder, exist_ok=True)
            new_path = os.path.join(folder, os.path.basename(path))
            os.rename(path, new_path)
            upload_file(new_path, f"Telegram_Backup/{folder}/{os.path.basename(path)}", email, password)
            os.remove(new_path)
