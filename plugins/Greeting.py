from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from variables import bot_id
from strings import greetingText
from db import resetSignupForm


def getGreetingKeyboard():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ثبت نام کلاس های جمع‌بندی", callback_data="signup")],
            [InlineKeyboardButton("ثبت نام های من", callback_data="forms")],
            [InlineKeyboardButton("ارتباط با ما", url="https://t.me/MCS_SSC_Admin")],
        ]
    )


@Client.on_message(filters.command(["start", f"start@{bot_id}"]))  # type: ignore
async def greet(_: Client, message: Message):
    # reset bot_user
    resetResult = resetSignupForm(message.from_user.id)
    msg = greetingText()
    if len(resetResult.data) != 0:
        msg = "فرم ثبت نام شما با موفقیت پاک شد.\n\n" + msg
    await message.reply_text(
        msg,
        reply_to_message_id=message.id,
        quote=True,
        reply_markup=getGreetingKeyboard(),
    )


@Client.on_callback_query(filters.regex(r"^start$"))  # type: ignore
async def greetCallback(_: Client, callback_query: CallbackQuery):
    # reset bot_user
    resetResult = resetSignupForm(callback_query.from_user.id)
    msg = greetingText()
    if len(resetResult.data) != 0:
        msg = "فرم ثبت نام شما با موفقیت پاک شد.\n\n" + msg
    await callback_query.message.edit(msg, reply_markup=getGreetingKeyboard())
