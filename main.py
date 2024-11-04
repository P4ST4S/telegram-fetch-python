import os
import json
from telethon import TelegramClient
from telethon.sessions import StringSession
from getpass import getpass
from functions.fetch_messages import fetch_messages
from functions.parse_articles import parse_articles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API credentials from environment variables
api_id = int(os.environ.get("TELEGRAM_API_ID"))
api_hash = os.environ.get("TELEGRAM_API_HASH")

# Channel username
channel_username = "@nytimes"

# Output file names
file_name = "out/output.json"
parse_file_name = "out/parsed_articles.json"


async def main():
    # Ensure output directory exists
    os.makedirs("out", exist_ok=True)

    # Read session string from file or initialize a new one
    session_path = "session.txt"
    session_string = open(session_path).read(
    ) if os.path.exists(session_path) else ""
    string_session = StringSession(session_string)
    client = TelegramClient(string_session, api_id, api_hash)

    try:
        if not session_string:
            await client.start(
                phone=lambda: input("Please enter your number: "),
                password=lambda: getpass("Please enter your password: "),
                code_callback=lambda: input(
                    "Please enter the code you received: "),
            )
            print("You are now connected!")
            print("Your session string:", client.session.save())

            # Save session string to a file for future use
            with open(session_path, "w") as session_file:
                session_file.write(client.session.save())
        else:
            await client.connect()

        # Fetch and parse messages
        await fetch_messages(client, channel_username, file_name)
        parse_articles(file_name, parse_file_name)

    except Exception as error:
        if "TIMEOUT" in str(error):
            print("Connection timed out. Retrying...")
        else:
            print("An error occurred:", error)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
