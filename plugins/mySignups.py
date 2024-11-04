from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.emoji import (
    CHECK_MARK_BUTTON,
    CROSS_MARK,
    SMILING_FACE_WITH_SMILING_EYES,
    RADIO_BUTTON,
)
from db import (
    getCompletedFormsByTelegramId,
)


@Client.on_callback_query(filters.regex(r"^forms$"))  # type: ignore
async def formsCallback(_: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    # Getting the form
    completedForms = getCompletedFormsByTelegramId(user_id)

    if len(completedForms) == 0:
        await callback_query.message.edit(
            f"شما هنوز ثبت نامی نکرده‌اید. جهت ثبت‌نام در برنامه‌ها بر روی دکمه بازگشت کلیک کنید. {SMILING_FACE_WITH_SMILING_EYES}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("بازگشت", callback_data="start")]]
            ),
        )
        return

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("بازگشت", callback_data="start")]]
    )
    str = "ثبت نام های شما تا به الآن:\n"
    for form in completedForms:
        match form["verified"]:
            case 1:
                str += CHECK_MARK_BUTTON
            case 0:
                str += RADIO_BUTTON
            case -1:
                str += CROSS_MARK

        str += f" {form['selected_class']['name']} - {form['full_name']}\n"
    str += "\n\n"
    str += f"{CHECK_MARK_BUTTON} به معنای تایید شدن ثبت نام است.\n{RADIO_BUTTON} به معنای در انتظار تایید بودن است.\n{CROSS_MARK} به معنای رد شدن ثبت نام است.\n"
    str += f"برای پیگیری، از طریق آی‌دی @MCS_SSC_Admin، با ما در ارتباط باشید. {SMILING_FACE_WITH_SMILING_EYES}"
    await callback_query.message.edit(str, reply_markup=reply_markup)
