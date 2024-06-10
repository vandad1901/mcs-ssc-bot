from dotenv import load_dotenv
from os import environ

load_dotenv()

bot_token = environ.get("BOT_TOKEN", "")
api_id = environ.get("API_ID", "")
api_hash = environ.get("API_HASH", "")
bot_id = environ.get("BOT_ID", "")
adminId = environ.get("ADMIN_ID", "")

db_url = environ.get("SUPABASE_URL", "")
db_key = environ.get("SUPABASE_KEY", "")
