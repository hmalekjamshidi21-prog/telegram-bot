# -*- coding: utf-8 -*-

import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error

TOKEN = os.environ["TELEGRAM_TOKEN"]
API = "https://api.telegram.org/bot" + TOKEN + "/"


def telegram_request(method, data=None):
    if data is None:
        data = {}

    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(API + method, data=encoded)

    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def send_message(chat_id, text):
    return telegram_request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text
        }
    )


def prepare_bot():
    # اگر قبلاً Webhook روی ربات تنظیم شده باشد، حذفش می‌کنیم
    try:
        telegram_request(
            "deleteWebhook",
            {
                "drop_pending_updates": "true"
            }
        )
        print("Webhook cleared.")
    except Exception as e:
        print("Webhook cleanup warning:", e)

    # بررسی اعتبار توکن
    try:
        info = telegram_request("getMe")
        username = info.get("result", {}).get("username", "unknown")
        print("Connected to Telegram as @" + username)
    except Exception as e:
        print("Telegram connection error:", e)
        raise


def main():
    print("Diamond Yaragh Bot started...")
    prepare_bot()

    offset = 0

    while True:
        try:
            result = telegram_request(
                "getUpdates",
                {
                    "timeout": 30,
                    "offset": offset,
                    "allowed_updates": json.dumps(["message"])
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

        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
            except Exception:
                body = ""

            print("HTTP ERROR:", e.code, body)

            if e.code == 409:
                print(
                    "409 Conflict: احتمالاً یک نسخه دیگر از همین ربات "
                    "هم‌زمان در حال getUpdates است."
                )

            time.sleep(8)

        except Exception as e:
            print("ERROR:", repr(e))
            time.sleep(5)


if __name__ == "__main__":
    main()
