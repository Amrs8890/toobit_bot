import os
import time
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# -------------------- تنظیمات --------------------

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = str(os.getenv("ADMIN_CHAT_ID", "0"))

if not TOKEN:
    raise ValueError("BOT_TOKEN پیدا نشد")

# -------------------- دکوراتور --------------------

# -------------------- دستورات --------------------

def start(update, context):
    user = update.effective_user

    text = f"""سلام {user.first_name} 👋
ربات آماده استفاده است ✅
"""

    keyboard = [
        [InlineKeyboardButton("🚀 شروع ربات", callback_data="start_trading")]
    ]

    if str(user.id) == ADMIN_CHAT_ID:
        keyboard.append(
            [InlineKeyboardButton("🛠 پنل ادمین", callback_data="admin")]
        )

    update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_callback(update, context):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "start_trading":
        start_trading(query, context)

    elif data == "admin" and str(query.from_user.id) == ADMIN_CHAT_ID:
        keyboard = [
            [InlineKeyboardButton("🎫 کد ۳۰ روزه", callback_data="gen30")],
            [InlineKeyboardButton("🎫 کد ۹۰ روزه", callback_data="gen90")],
            [InlineKeyboardButton("♾ کد دائمی", callback_data="genperm")],
        ]
        query.message.reply_text(
            "پنل ادمین",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

  
        query.message.reply_text(f"کد ساخته شد:\n{code}")

def activate_cmd(update, context):
    if not context.args:
        update.message.reply_text("استفاده:\n/activate CODE")
        return

    code = context.args[0]
    ok, msg = activate_license(update.effective_user.id, code)
    update.message.reply_text(msg)

def my_status(update, context):
    user_id = update.effective_user.id
    if not check_user_access(user_id):
        update.message.reply_text("❌ اشتراک فعال نیست")
        return

    db = load_db()
    exp = db["users"][str(user_id)]["expire"]
    update.message.reply_text(f"✔ فعال تا:\n{time.ctime(exp)}")

def start_trading(update, context):
    if hasattr(update, "message") and update.message:
        update.message.reply_text("🚀 ربات شروع شد!")
    else:
        update.message.reply_text("🚀 ربات شروع شد!")

def admin_list_users(update, context):
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        update.message.reply_text("⛔ دسترسی نداری")
        return

    db = load_db()
    text = "👥 کاربران:\n\n"
    for uid, info in db.get("users", {}).items():
        text += f"{uid} → {time.ctime(info['expire'])}\n"

    update.message.reply_text(text)

# -------------------- اجرای ربات --------------------

def main():
    print("🤖 Bot is running...")
   
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("activate", activate_cmd))
    application.add_handler(CommandHandler("my_status", my_status))
    application.add_handler(CommandHandler("admin_list_users", admin_list_users))
    application.add_handler(CallbackQueryHandler(button_callback))

   
if __name__ == "__main__":
    main()






