from pyrogram.emoji import (
    SUNFLOWER,
    SMILING_FACE_WITH_SMILING_EYES,
    CHECK_MARK_BUTTON,
    IDENTIFICATION_CARD,
    MOBILE_PHONE,
    BUST_IN_SILHOUETTE,
    ORANGE_BOOK,
    SCHOOL,
)

uni_status_enum = [
    "دانشجوی دانشکده ریاضی و علوم کامپیوتر",
    "دانشجوی سایر دانشکده های دانشگاه امیرکبیر",
    "دانشجوی سایر دانشگاه ها",
]


def greetingString():
    str = f"سلام، وقتتون به‌خیر. {SUNFLOWER}\n"
    str += "جهت ثبت‌نام بر روی «ثبت‌نام کلاس‌های جمع‌بندی» و جهت مشاهده وضعیت کلاس‌هایی که ثبت‌نام کردید بر روی «ثبت‌نام‌های من» کلیک کنید.\n"
    str += f"در صورت برخورد به هرگونه مشکل و یا عدم پاسخ‌دهی ربات، از طریق دکمه «ارتباط با ما» و یا آی‌دی @MCS_SSC_Admin، به ما اطلاع دهید. {SMILING_FACE_WITH_SMILING_EYES}"

    return str


def chooseClassString():
    str = "کلاسی که قصد ثبت‌نام آن را دارید از طریق دکمه‌های زیر انتخاب کنید.\n"
    str += f"در صورت تمایل به ثبت‌نام در چند کلاس، و یا ثبت‌نام چند نفر در یک کلاس، فرایند ثبت‌نام یک کلاس را کامل کنید و سپس با دستور /start به ثبت‌نام کلاس بعدی بپردازید. {SMILING_FACE_WITH_SMILING_EYES}"

    return str


def classConfirmString(selectedClass: dict):
    str = f"{CHECK_MARK_BUTTON} کلاس مورد نظر شما: {selectedClass['name']}\n\n"
    str += "در صورت صحیح بودن کلاس، تایید کنید."

    return str


def uniInfoSelectionString(selectedClass):
    str = f"{CHECK_MARK_BUTTON} کلاس مورد نظر شما: {selectedClass['name']}\n\n"
    str += "در صورت تایید کلاس انتخابی، لطفاً وضعیت خود را انتخاب کنید."

    return str


def askForStudentIdString(uni_status: int):
    if uni_status < 2:
        return f"{IDENTIFICATION_CARD} لطفاً شماره دانشجویی فرد شرکت‌کننده را در یک پیام ارسال کنید."
    else:
        str = f"{IDENTIFICATION_CARD} کد ملی فرد شرکت کننده در کلاس را در یک پیام ارسال کنید.\n"
        str += "جهت کسب مجوز ورود به دانشگاه برای افراد غیر از دانشجویان امیرکبیر، داشتن کد ملی الزامیست."

        return str


def askForNumberString():
    return f"{MOBILE_PHONE} لطفاً شماره تماس فرد شرکت‌کننده را در یک پیام ارسال کنید."


def askForNameString():
    return f"{BUST_IN_SILHOUETTE} لطفاً نام و نام خانوادگی فرد شرکت‌کننده را در یک پیام ارسال کنید."


def askForMoneyString(form: dict, selectedClass: dict):
    str = "اطلاعات شما:\n"
    str += f"{ORANGE_BOOK} کلاس انتخابی: {selectedClass['name']}\n"
    str += f"{BUST_IN_SILHOUETTE} نام و نام خانوادگی: {form['full_name']}\n"
    str += f"{SCHOOL} وضعیت دانشجویی : {uni_status_enum[form['uni_status']]}\n"
    if form["uni_status"] < 2:
        str += f"{IDENTIFICATION_CARD} شماره دانشجویی: {form['student_id']}\n"
    else:
        str += f"{IDENTIFICATION_CARD} کد ملی: {form['student_id']}\n"
    str += f"{MOBILE_PHONE} شماره تماس: {form['phone_number']}\n\n"
    money = selectedClass["prices"][form["uni_status"]]
    str += f"در صورت صحت اطلاعات بالا، مبلغ {money} را به شماره کارت `{selectedClass['card_number']}` به نام {selectedClass['cardholder_name']} واریز کنید و **تصویر رسید آن را ارسال کنید**. برای نهایی شدن ثبت‌نام، تایید پرداخت توسط ادمین الزامیست.\n"
    str += f"در غیر این صورت، دستور /start را دوباره اجرا کنید."

    return str


def paymentReceivedString():
    str = "پرداخت شما ثبت شد. دقت کنید که ثبت‌نام شما تا زمان تایید شدن پرداخت توسط ادمین نهایی نمی‌شود.\n"
    str += f"لطفاً منتظر تایید ما باشید. در صورت برخورد به هرگونه مشکل، از طریق آی‌دی @MCS_SSC_Admin، به ما اطلاع دهید. {SUNFLOWER}"

    return str


def paymentAcceptedString():
    str = "پرداخت شما تایید و ثبت‌نام شما نهایی شد. مکان دقیق کلاس دقایقی قبل از شروع کلاس در کانال انجمن علمی ریاضی و علوم کامپیوتر (@MCS_SSC) اطلاع‌رسانی می‌شود.\n"
    str += "در صورت برخورد به هرگونه مشکل، می‌توانید از طریق آی‌دی @MCS_SSC_Admin با ما در ارتباط باشید.\n"
    str += f"خوش‌حالیم که کلاس‌های ما را انتخاب کردید. {SMILING_FACE_WITH_SMILING_EYES}{SUNFLOWER}"

    return str


def paymentAcceptedAdminString():
    return "پرداخت کاربر تایید شد."


def paymentRejectedString():
    str = "پرداخت شما رد شد."
    str += (
        f"لطفاً برای پیگیری از طریق آی‌دی @MCS_SSC_Admin به ادمین پیام بدهید. {SUNFLOWER}"
    )

    return str


def paymentRejectedAdminString():
    return "پرداخت کاربر رد شد."
