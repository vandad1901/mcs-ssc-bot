from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
from pyrogram.emoji import (
    CHECK_MARK_BUTTON,
    CROSS_MARK,
    FOLDED_HANDS,
    KEYCAP_DIGIT_ZERO,
)
from db import (
    getAvailableClasses,
    getCompletedFormById,
    getSignedUpCount,
    getClassById,
    moveToCompletedForms,
    updateCompletedForm,
    updateSignupForm,
)
from strings import (
    askForMoneyText,
    chooseClassText,
    classConfirmText,
    askForNumberText,
    paymentAcceptedAdminText,
    paymentAcceptedText,
    paymentRejectedAdminText,
    paymentRejectedText,
    uniInfoSelectionText,
    askForStudentIdText,
    askForNameText,
    uni_status_enum,
    paymentReceivedText,
)
from filters import signupStage
from variables import adminId


@Client.on_callback_query(filters.regex(r"^signup$"))  # type: ignore
async def signupOptions(_: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    # Updating info
    try:
        updateSignupForm(user_id, {"selected_class": None})  # DB call
        classes = getAvailableClasses()
    except Exception as e:
        print(e)
        await callback_query.message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    KEYCAP_DIGIT_ZERO.replace("0", str(i + 1)),
                    callback_data=f"signup:{class_['id']}",
                )
                for i, class_ in enumerate(classes)  # DB call
            ][::-1]
        ]
        + [[InlineKeyboardButton("بازگشت", "start")]]
    )
    await callback_query.message.edit(
        chooseClassText(classes), reply_markup=reply_markup
    )


@Client.on_callback_query(filters.regex(r"^signup:((\d)+)$"))  # type: ignore
async def classConfirm(
    _: Client, callback_query: CallbackQuery
):  # Show a message asking the user to confirm their class
    # Sending reply
    classIndex = int(callback_query.matches[0].group(1))
    try:
        class_ = getClassById(classIndex)  # DB call
        signed_up = getSignedUpCount(classIndex)
        isFull = signed_up >= class_["limit"]
    except Exception as e:
        print(e)
        await callback_query.message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return
    reply_markup = InlineKeyboardMarkup(
        [
            (
                [
                    InlineKeyboardButton("بله", f"signup:confirm:{classIndex}"),
                    InlineKeyboardButton("خیر", "signup"),
                ]
                if not isFull
                else [InlineKeyboardButton("بازگشت", "signup")]
            )
        ]
    )

    await callback_query.message.edit(
        classConfirmText(class_, signed_up >= class_["limit"]),
        reply_markup=reply_markup,
    )


@Client.on_callback_query(filters.regex(r"^signup:confirm:((\d)+)$"))  # type: ignore
async def askForGroupInfo(
    _: Client, callback_query: CallbackQuery
):  # Show a message asking which group the student is in
    user_id = callback_query.from_user.id
    class_id = callback_query.matches[0].group(1)

    # Updating info
    try:
        updateSignupForm(user_id, {"selected_class": class_id})  # DB call
        class_ = getClassById(class_id)  # DB call
    except Exception as e:
        print(e)
        await callback_query.message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # sending reply
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(uni_status_enum[i], f"signup:uni:{i}")]
            for i in range(2)
        ]
        + [
            [InlineKeyboardButton("بازگشت", f"signup")],
        ]
    )

    await callback_query.message.edit(
        uniInfoSelectionText(class_), reply_markup=reply_markup
    )


@Client.on_callback_query(filters.regex(r"^signup:uni:((\d)+)$"))  # type: ignore
async def askForStudentId(_: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    uni_status = int(callback_query.matches[0].group(1))

    # Updating info
    try:
        updateSignupForm(
            user_id, {"uni_status": uni_status, "signup_stage": 0}
        )  # DB call
    except Exception as e:
        print(e)
        await callback_query.message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    msg = askForStudentIdText(uni_status)
    await callback_query.message.edit(msg)
    print(f"user {user_id} is now entering student number")


@Client.on_message(signupStage(0) & ~filters.command("start"))  # type: ignore
async def askForNumber(_: Client, message: Message):
    user_id = message.from_user.id
    student_id = message.text
    if student_id.isnumeric() == False:
        await message.reply("لطفا فقط عدد انگلیسی وارد کنید.")
        return

    # Updating info
    try:
        updateSignupForm(
            user_id, {"signup_stage": 1, "student_id": int(student_id)}
        )  # DB call
    except Exception as e:
        print(e)
        await message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    await message.reply(askForNumberText())
    print(f"user {user_id} is now entering phone number")


@Client.on_message(signupStage(1) & ~filters.command("start"))  # type: ignore
async def askForName(_: Client, message: Message):
    user_id = message.from_user.id
    phone_number = message.text
    if phone_number.isnumeric() == False:
        await message.reply("لطفا فقط عدد انگلیسی وارد کنید.")
        return

    # Updating info
    try:
        updateSignupForm(
            user_id, {"signup_stage": 2, "phone_number": int(phone_number)}
        )  # DB call
    except Exception as e:
        print(e)
        await message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    await message.reply(askForNameText())
    print(f"user {user_id} is now entering full name")


@Client.on_message(signupStage(2) & ~filters.command("start"))  # type: ignore
async def askForMoney(_: Client, message: Message):
    user_id = message.from_user.id
    full_name = message.text
    # Updating info
    try:
        form = updateSignupForm(
            user_id, {"signup_stage": 3, "full_name": full_name}
        )  # DB call
        selectedClass = getClassById(form["selected_class"])  # DB call
    except Exception as e:
        print(e)
        await message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    await message.reply(askForMoneyText(form, selectedClass))
    print(f"user {user_id} is now sending receipt photo")


@Client.on_message(signupStage(3) & ~filters.command("start"))  # type: ignore
async def askForFinalConfirmation(client: Client, message: Message):
    user_id = message.from_user.id
    if not message.photo:
        await message.reply("لطفا عکس از رسید پرداخت خود بفرستید.")
        return
    receipt_photo_id = message.photo.file_id

    # Updating info
    try:
        updateSignupForm(
            user_id,
            {
                "signup_stage": 4,
                "receipt_photo_id": receipt_photo_id,
                "receipt_message_id": message.id,
            },
        )  # DB call
        completedForm = moveToCompletedForms(user_id)  # DB call
        if completedForm == None:
            raise Exception("Form not found")
        selectedClass = getClassById(completedForm["selected_class"])  # DB call
    except Exception as e:
        print(e)
        await message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    await message.reply(paymentReceivedText())
    await client.send_photo(
        adminId,
        photo=receipt_photo_id,
        caption=f"پرداخت مبلغ {selectedClass['prices'][completedForm['uni_status']]} تومان برای برنامه {selectedClass['name']} توسط {completedForm['full_name']} تایید می‌شود؟",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{CHECK_MARK_BUTTON} تایید",
                        f"confirm_payment:{user_id}:{completedForm['id']}",
                    ),
                    InlineKeyboardButton(
                        f"{CROSS_MARK} رد",
                        f"reject_payment:{user_id}:{completedForm['id']}",
                    ),
                ]
            ]
        ),
    )
    print(f"user {user_id} sent receipt photo")


@Client.on_callback_query(filters.regex(r"^confirm_payment:((\d)+):((\d)+)$"))  # type: ignore
async def confirmPayment(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    form_id = int(callback_query.matches[0].group(3))
    try:
        form = getCompletedFormById(form_id)  # DB call
        if form == None:
            raise Exception("Form not found")
        # Updating info
        updateCompletedForm(form_id, {"verified": 1})  # DB call
    except Exception as e:
        print(e)
        await callback_query.message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    await client.send_message(
        user_id, paymentAcceptedText(), reply_to_message_id=form["receipt_message_id"]
    )
    await callback_query.message.edit(paymentAcceptedAdminText())


@Client.on_callback_query(filters.regex(r"^reject_payment:((\d)+):((\d)+)$"))  # type: ignore
async def rejectPayment(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.matches[0].group(1))
    form_id = int(callback_query.matches[0].group(3))
    try:
        form = getCompletedFormById(form_id)
        if form == None:
            raise Exception("Form not found")

        # Updating info
        updateCompletedForm(form_id, {"verified": -1})
    except Exception as e:
        print(e)
        await callback_query.message.reply_text(
            f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
        )
        return

    # Sending reply
    await client.send_message(
        user_id,
        paymentRejectedText(),
        reply_to_message_id=form["receipt_message_id"],
    )
    await callback_query.message.edit(paymentRejectedAdminText())
