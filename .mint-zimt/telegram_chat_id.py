#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx"]
# ///

from __future__ import annotations

import os
import sys
import time

import httpx

WAIT_MINUTES = 10
LONG_POLL_SECONDS = 30


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        print(
            "Error: TELEGRAM_BOT_TOKEN environment variable not set.", file=sys.stderr
        )
        sys.exit(1)

    base = f"https://api.telegram.org/bot{token}"

    print(
        f"Send any message to your bot now. Waiting up to {WAIT_MINUTES} minutes...",
        file=sys.stderr,
    )

    deadline = time.monotonic() + (WAIT_MINUTES * 60)
    while time.monotonic() < deadline:
        resp = httpx.get(
            f"{base}/getUpdates",
            params={"timeout": LONG_POLL_SECONDS},
            timeout=LONG_POLL_SECONDS + 5,
        )
        if not resp.is_success or not resp.json().get("ok"):
            print(
                "Could not reach the Telegram API. Check your bot token and try again.",
                file=sys.stderr,
            )
            sys.exit(1)
        for update in resp.json().get("result", []):
            msg = update.get("message", {})
            if msg.get("text"):
                print(msg["chat"]["id"])
                return

    print(
        f"No message received within {WAIT_MINUTES} minutes. Send a message to your bot and try again.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
