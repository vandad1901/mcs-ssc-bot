from supabase import create_client, Client
from variables import db_url, db_key
from pyrogram.emoji import FOLDED_HANDS


supabase: Client = create_client(db_url, db_key)


def dbCall(func):
    async def wrapper(replyFunc, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            await replyFunc(
                f"در هنگام پردازش درخواست شما خطایی رخ داد. لطفا کمی صبر کنید و دوباره تلاش کنید {FOLDED_HANDS}."
            )
            raise e

    return wrapper


# Classes
def getAllClasses():
    return supabase.table("classes").select("*").order("id", desc=True).execute().data


def getAvailableClasses():
    return (
        supabase.table("classes")
        .select("*")
        .order("id")
        .eq("upcoming", "true")
        .execute()
        .data
    )


def getClassById(classId: int):
    return supabase.table("classes").select("*").eq("id", classId).execute().data[0]


def getSignedUpCount(classId: int):
    # return just the number of complete_forms that have the same selected_class as classId
    return (
        supabase.table("completed_forms")
        .select("count")
        .eq("selected_class", classId)
        .execute()
        .data[0]["count"]
    )


# Signup forms
def getSignupFormById(telegramId: int):
    res = (
        supabase.table("signup_forms")
        .select("*")
        .eq("telegram_id", telegramId)
        .execute()
        .data
    )
    return res[0] if len(res) > 0 else None


def updateSignupForm(telegramId: int, data: dict):
    data["telegram_id"] = telegramId
    return supabase.table("signup_forms").upsert(data).execute().data[0]


def resetSignupForm(telegramId: int):
    return (
        supabase.table("signup_forms")
        .delete()
        .eq("telegram_id", telegramId)
        .lt("signup_stage", 4)
        .execute()
    )


def moveToCompletedForms(telegramId: int):
    form = getSignupFormById(telegramId)
    if form == None:
        raise Exception("Form not found")
    neededKeys = [
        "telegram_id",
        "uni_status",
        "student_id",
        "phone_number",
        "full_name",
        "receipt_photo_id",
        "selected_class",
        "receipt_message_id",
    ]
    completedForm = {key: form[key] for key in neededKeys}
    res = supabase.table("completed_forms").insert(completedForm).execute().data
    supabase.table("signup_forms").delete().eq("telegram_id", telegramId).execute()
    return res[0]


# Completed Forms
def getCompletedFormsByTelegramId(user_id: int):
    return (
        supabase.table("completed_forms")
        .select("*, selected_class(*)")
        .eq("telegram_id", user_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )


def getCompletedFormById(form_id: int):
    res = (
        supabase.table("completed_forms")
        .select("*, selected_class(*)")
        .eq("id", form_id)
        .execute()
        .data
    )
    return res[0] if len(res) > 0 else None


def getCompletedFormsByClassId(class_id: int):
    return (
        supabase.table("completed_forms")
        .select("*")
        .eq("selected_class", class_id)
        .execute()
        .data
    )


def updateCompletedForm(form_id: int, data: dict):
    data["id"] = form_id
    return supabase.table("completed_forms").upsert(data).execute()
