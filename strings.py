from pyrogram.emoji import (
    SUNFLOWER,
    SMILING_FACE_WITH_SMILING_EYES,
    CHECK_MARK_BUTTON,
    IDENTIFICATION_CARD,
    MOBILE_PHONE,
    BUST_IN_SILHOUETTE,
    ORANGE_BOOK,
    SCHOOL,
    RED_EXCLAMATION_MARK,
    KEYCAP_DIGIT_ZERO,
    SPIRAL_CALENDAR,
)

uni_status_enum = [
    "دانشجوی دانشکده ریاضی و علوم کامپیوتر",
    "دانشجوی سایر دانشکده های دانشگاه امیرکبیر",
    "دانشجوی سایر دانشگاه ها",
]


def greetingText():
    txt = f"سلام، وقتتون به‌خیر. {SUNFLOWER}\n"
    txt += "جهت ثبت‌نام بر روی «ثبت‌نام برنامه ها» و جهت مشاهده وضعیت برنامه هایی که ثبت‌نام کردید بر روی «ثبت‌نام‌های من» کلیک کنید.\n"
    txt += f"در صورت برخورد به هرگونه مشکل و یا عدم پاسخ‌دهی ربات، از طریق دکمه «ارتباط با ما» و یا آی‌دی @MCS_SSC_Admin، به ما اطلاع دهید. {SMILING_FACE_WITH_SMILING_EYES}"

    return txt


def chooseClassText(classes: list[dict]):
    txt = "برنامه ای که قصد ثبت‌نام آن را دارید از طریق دکمه‌های زیر انتخاب کنید.\n"
    for i, class_ in enumerate(classes):
        txt += f"{KEYCAP_DIGIT_ZERO.replace('0', str(i + 1))} {class_['name']}\n"
        txt += f"{SPIRAL_CALENDAR} تاریخ: {class_['date']}\n\n"
    txt += f"در صورت تمایل به ثبت‌نام در چند برنامه، و یا ثبت‌نام چند نفر در یک برنامه، فرایند ثبت‌نام یک برنامه را کامل کنید و سپس با دستور /start به ثبت‌نام برنامه بعدی بپردازید. {SMILING_FACE_WITH_SMILING_EYES}"

    return txt


def classConfirmText(selectedClass: dict, classFull: bool):
    txt = f"{CHECK_MARK_BUTTON} برنامه مورد نظر شما: {selectedClass['name']}\n"
    txt += f"{SPIRAL_CALENDAR} تاریخ: {selectedClass['date']}\n\n"

    if(classFull):
        txt += "متاسفانه برنامه مورد نظر پر شده است."
    else:
        txt += "در صورت صحیح بودن برنامه، تایید کنید."

    return txt


def uniInfoSelectionText(selectedClass):
    txt = f"{CHECK_MARK_BUTTON} برنامه مورد نظر شما: {selectedClass['name']}\n"
    txt += f"{SPIRAL_CALENDAR} تاریخ: {selectedClass['date']}\n\n"

    txt += f"{RED_EXCLAMATION_MARK} توجه کنید که قبل از برگزاری برنامه، اطلاعات ثبت‌نام شما با کارت دانشجویی فرد شرکت‌کننده مطابقت داده می‌شود. بنابراین لطفاً اطلاعات را با دقت ارسال کنید.\n\n"

    if selectedClass["is_day_of"]:
        txt += f"{RED_EXCLAMATION_MARK} با توجه به نبود وقت کافی برای گرفتن مجوز، ثبت‌نام دانشجویان دانشگاه های دیگر بسته شده است.\n\n"
    txt += "در صورت تایید برنامه انتخابی، لطفاً وضعیت فرد شرکت‌کننده را انتخاب کنید."
    return txt


def askForStudentIdText(uni_status: int):
    if uni_status < 2:
        return f"{IDENTIFICATION_CARD} لطفاً شماره دانشجویی فرد شرکت‌کننده را در یک پیام ارسال کنید."
    else:
        txt = f"{IDENTIFICATION_CARD} کد ملی فرد شرکت کننده در برنامه را در یک پیام ارسال کنید.\n"
        txt += "جهت کسب مجوز ورود به دانشگاه برای افراد غیر از دانشجویان امیرکبیر، داشتن کد ملی الزامیست."

        return txt


def askForNumberText():
    return f"{MOBILE_PHONE} لطفاً شماره تماس فرد شرکت‌کننده را در یک پیام ارسال کنید."


def askForNameText():
    return f"{BUST_IN_SILHOUETTE} لطفاً نام و نام خانوادگی فرد شرکت‌کننده را در یک پیام ارسال کنید."


def askForMoneyText(form: dict, selectedClass: dict):
    txt = "اطلاعات شما:\n"
    txt += f"{ORANGE_BOOK} برنامه انتخابی: {selectedClass['name']}\n"
    txt += f"{BUST_IN_SILHOUETTE} نام و نام خانوادگی: {form['full_name']}\n"
    txt += f"{SCHOOL} وضعیت دانشجویی : {uni_status_enum[form['uni_status']]}\n"
    if form["uni_status"] < 2:
        txt += f"{IDENTIFICATION_CARD} شماره دانشجویی: {form['student_id']}\n"
    else:
        txt += f"{IDENTIFICATION_CARD} کد ملی: {form['student_id']}\n"
    txt += f"{MOBILE_PHONE} شماره تماس: {form['phone_number']}\n\n"
    money = selectedClass["prices"][form["uni_status"]]
    txt += f"در صورت صحت اطلاعات بالا، مبلغ {money} را به شماره کارت `{selectedClass['card_number']}` به نام {selectedClass['cardholder_name']} واریز کنید و **تصویر رسید آن را ارسال کنید**. برای نهایی شدن ثبت‌نام، تایید پرداخت توسط ادمین الزامیست.\n"
    txt += f"در غیر این صورت، دستور /start را دوباره اجرا کنید."

    return txt


def paymentReceivedText():
    txt = "پرداخت شما ثبت شد. دقت کنید که ثبت‌نام شما تا زمان تایید شدن پرداخت توسط ادمین نهایی نمی‌شود.\n"
    txt += f"لطفاً منتظر تایید ما باشید. در صورت برخورد به هرگونه مشکل، از طریق آی‌دی @MCS_SSC_Admin، به ما اطلاع دهید. {SUNFLOWER}"

    return txt


def paymentAcceptedText():
    txt = "پرداخت شما تایید و ثبت‌نام شما نهایی شد. برای مطلع شدن از جزییات در گروه زیر عضو شوید.\n"
    txt += "https://t.me/+O2nAdQIP4sw4OGVk\n\n"
    txt += "در صورت برخورد به هرگونه مشکل، می‌توانید از طریق آی‌دی @MCS_SSC_Admin با ما در ارتباط باشید.\n"
    txt += f"خوش‌حالیم که برنامه‌های ما را انتخاب کردید. {SMILING_FACE_WITH_SMILING_EYES}{SUNFLOWER}"

    return txt


def paymentAcceptedAdminText():
    return "پرداخت کاربر تایید شد."


def paymentRejectedText():
    txt = "پرداخت شما رد شد."
    txt += (
        f"لطفاً برای پیگیری از طریق آی‌دی @MCS_SSC_Admin به ادمین پیام بدهید. {SUNFLOWER}"
    )

    return txt


def paymentRejectedAdminText():
    return "پرداخت کاربر رد شد."


def exportCaptionText(class_: dict, total: int):
    txt = "ثبت‌نامی های برنامه\n"
    txt += f"{class_['name']}\n\n"
    txt += f"تعداد کل ثبت‌نام ها: {total}\n\n"
    return txt
