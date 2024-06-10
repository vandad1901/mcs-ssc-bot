from __future__ import annotations

import asyncio
import sys

from pyrogram.client import Client
from pyrogram.sync import idle

from variables import api_hash, api_id, bot_token
import db

if sys.platform in ("win32", "cygwin", "cli"):
    from winloop import install  # type: ignore
else:
    from uvloop import install


async def main():
    proxy = dict(scheme="socks5", hostname="127.0.0.1", port=2080)
    apps = [
        Client(
            "anjoman",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            plugins=dict(root="plugins"),
            proxy=proxy,
        ),
    ]

    for app in apps:
        await app.start()
    print("Starting")

    await idle()

    print("Stopping")
    for app in apps:
        await app.stop()


install()
asyncio.run(main())
