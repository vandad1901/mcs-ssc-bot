import datetime
import pytz

import io
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.emoji import (
    CHECK_MARK_BUTTON,
    RADIO_BUTTON,
)
from db import (
    getAllClasses,
    getClassById,
    getCompletedFormsByClassId,
)
from strings import exportCaptionText


@Client.on_callback_query(filters.regex(r"^export:((\d)+)"))  # type: ignore
async def exportSelection(_: Client, callback_query: CallbackQuery):
    page = int(callback_query.matches[0].group(1))
    classes = getAllClasses()

    thisPageClasses = classes[(page - 1) * 5 : page * 5]
    buttons = [
        [
            InlineKeyboardButton(
                f"{RADIO_BUTTON if c['upcoming'] else CHECK_MARK_BUTTON} {c['name']}",
                callback_data=f"exportClass:{c['id']}",
            )
        ]
        for c in thisPageClasses
    ]
    if page > 1:
        buttons.append(
            [
                InlineKeyboardButton(
                    "صفحه قبل",
                    callback_data=f"export:{page-1}",
                )
            ]
        )
    if page < len(classes) // 5:
        buttons.append(
            [
                InlineKeyboardButton(
                    "صفحه بعد",
                    callback_data=f"export:{page+1}",
                )
            ]
        )

    markup = InlineKeyboardMarkup(buttons)

    await callback_query.message.edit(
        "لطفا یک برنامه را انتخاب کنید:", reply_markup=markup
    )


@Client.on_callback_query(filters.regex(r"^exportClass:((\d)+)"))  # type: ignore
async def exportSelectedClass(_: Client, callback_query: CallbackQuery):
    classId = int(callback_query.matches[0].group(1))
    class_ = getClassById(classId)
    forms = getCompletedFormsByClassId(classId)
    with io.BytesIO() as f:

        f.write(
            b"created_at, uni_status, phone_number, full_name, student_id, verified\n"
        )
        for form in forms:
            f.write(
                f"{form['created_at']}, {form['uni_status']}, {form['phone_number']}, {form['full_name']}, {form['student_id']}, {form['verified']}\n".encode()
            )

        f.seek(0)

        await callback_query.message.reply_document(
            document=f,
            file_name=f"export_{datetime.datetime.now(tz=pytz.timezone('Iran')).strftime('%Y-%m-%d_%H-%M-%S')}.csv",
            caption=exportCaptionText(class_, len(forms)),
        )
