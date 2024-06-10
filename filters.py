from pyrogram import filters
from pyrogram.types import Message
from pyrogram.client import Client
from pyrogram.filters import create
from db import getSignupFormById


def signupStage(data: int):
    async def func(_, __, update: Message):
        bot_user = getSignupFormById(update.from_user.id)
        if bot_user:
            return bot_user["signup_stage"] == data
        return False

    return filters.create(func, data=data)
