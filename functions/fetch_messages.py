import json
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageEntityTextUrl


async def fetch_messages(client, channel_username, file_name):
    try:
        channel = await client.get_entity(channel_username)
        history = await client.get_messages(channel, limit=10)

        messages = []

        for message in history:
            if message.message:
                media_info = None
                urls = []

                if message.media:
                    if isinstance(message.media, MessageMediaPhoto):
                        media_info = {
                            "type": "photo",
                            # Adjust based on needs
                            "url": str(message.media.photo.id)
                        }
                    elif isinstance(message.media, MessageMediaDocument):
                        if message.media.document.mime_type.startswith("video/"):
                            media_info = {
                                "type": "video",
                                # Adjust as needed
                                "url": str(message.media.document.id)
                            }

                if message.entities:
                    for entity in message.entities:
                        if isinstance(entity, MessageEntityTextUrl):
                            urls.append(entity.url)

                messages.append({
                    "id": message.id,
                    "date": message.date.isoformat(),
                    "message": message.message,
                    "media": media_info,
                    "sender_id": message.from_id.user_id if message.from_id else None,
                    "urls": urls
                })

        with open(file_name, 'w') as file:
            json.dump(messages, file, indent=2)
        print("Messages fetched and saved to output.json file.")

    except Exception as error:
        print("Error fetching messages:", error)
