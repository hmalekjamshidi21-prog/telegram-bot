# -*- coding: utf-8 -*-

import os
import json
import time
import urllib.request
import urllib.parse

# توکن از Railway Variables خوانده می‌شود
TOKEN = os.environ["TELEGRAM_TOKEN"]

API = "https://api.telegram.org/bot" + TOKEN + "/"


def telegram_request(method, data=None):
    if data is None:
        data = {}

    data = urllib.parse.urlencode(data).encode("utf-8")

    request = urllib.request.Request(
        API + method,
        data=data
    )

    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode("utf-8"))


def send_message(chat_id, text):
    telegram_request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text
        }
    )


def main():
    print("Diamond Yaragh Bot started...")

    offset = 0

    while True:
        try:
            result = telegram_request(
                "getUpdates",
                {
                    "timeout": 30,
                    "offset": offset
                }
            )

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")

                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                print("Message:", text)

                if text == "/start":
                    send_message(
                        chat_id,
                        "سلام 👋\nبه ربات دیاموند یراق خوش آمدید."
                    )

                elif text:
                    send_message(
                        chat_id,
                        "پیامت دریافت شد ✅\n\n" + text
                    )

        except Exception as e:
            print("ERROR:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()