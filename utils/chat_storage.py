import json
import os
from datetime import datetime

FILE_PATH = "data/chat_history.json"


def load_chat_history():

    if not os.path.exists(FILE_PATH):

        os.makedirs("data", exist_ok=True)

        with open(FILE_PATH, "w") as file:
            json.dump([], file)

    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_chat(user_message, ai_response):

    chats = load_chat_history()

    chats.append(
        {
            "user": user_message,
            "assistant": ai_response,
            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    )

    with open(FILE_PATH, "w") as file:
        json.dump(
            chats,
            file,
            indent=4
        )