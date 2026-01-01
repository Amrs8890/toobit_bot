from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os 
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# فایل مدیریت اشتراک
from license_manager import (
    generate_license,
    activate_license,
    check_user_access,
    load_db,
    save_db,
)

# ------------------------------------------------
#  بخش A: تنظیمات اولیه
# ------------------------------------------------

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN در .env پیدا نشد!")

# دکوراتور برای چک کردن اشتراک
def requires_license(func):
     def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return  func(update, context)
    return wrapper

# ------------------------------------------------
#  بخش B: دستورات ربات
# ------------------------------------------------

def start(update, context):
    user = update.effective_user

    text = f"""سلام {user.first_name} 👋
ربات آماده استفاده است ✅
"""

    keyboard = [
        [InlineKeyboardButton("🚀 شروع ربات", callback_data="start_trading")],
    ]

    if str(user.id) == str(ADMIN_CHAT_ID):
        keyboard.append(
            [InlineKeyboardButton("🛠 پنل ادمین", callback_data="admin")]
        )

     update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

 def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
     query.answer()
    data = query.data

    # فعال‌سازی
    if data == "activate":
         query.message.reply_text("کد اشتراک را بفرست:\n\n/activate <CODE>")

    # وضعیت اشتراک
    elif data == "status":
        uid = query.from_user.id
        ok = check_user_access(uid)
        if ok:
            db = load_db()
            exp = db["users"][str(uid)]["expire"]
             query.message.reply_text(f"✔ فعال تا:\n{time.ctime(exp)}")
        else:
             query.message.reply_text("❌ اشتراک فعال نیست.")

    # پنل ادمین
    elif data == "admin" and str(query.from_user.id) == str(ADMIN_CHAT_ID):
        kb = [
            [InlineKeyboardButton("🎫 ساخت کد ۳۰ روزه", callback_data="gen30")],
            [InlineKeyboardButton("🎫 ساخت کد ۹۰ روزه", callback_data="gen90")],
            [InlineKeyboardButton("♾ ساخت کد دائمی", callback_data="genperm")],
        ]
        await query.message.reply_text(
            "🔧 پنل ادمین", reply_markup=InlineKeyboardMarkup(kb)
        )

    # ساخت کد توسط ادمین
    elif data.startswith("gen") and str(query.from_user.id) == str(ADMIN_CHAT_ID):
        if data == "gen30":
            code = generate_license(30)
        elif data == "gen90":
            code = generate_license(90)
        elif data == "genperm":
            code = generate_license(99999)

         query.message.reply_text(f"کد ساخته شد:\n`{code}`", parse_mode="Markdown")

    else:
         query.message.reply_text("❌ دستور نامعتبر.")


# فرمان فعال‌سازی
 def activate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
         update.message.reply_text("استفاده:\n/activate CODE")
        return

    code = context.args[0].strip()
    user_id = update.effective_user.id

    ok, msg = activate_license(user_id, code)
     update.message.reply_text(msg)


# وضعیت اشتراک
 def my_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ok = check_user_access(user_id)

    if not ok:
         update.message.reply_text("❌ اشتراک فعال نیست.")
        return

    db = load_db()
    exp = db["users"][str(user_id)]["expire"]
     update.message.reply_text(f"✔ اشتراک فعال تا:\n{time.ctime(exp)}")


# مثال یک دستور محافظت‌شده
@requires_license
 def start_trading(update: Update, context: ContextTypes.DEFAULT_TYPE):
     update.message.reply_text("🚀 استراتژی معاملاتی شروع شد!")


# ------------------------------------------------
#  بخش C: اجرای ربات
# ------------------------------------------------

# ------------------------------------------------
#  بخش C: اجرای ربات (نسخه صحیح)
# ------------------------------------------------

 def admin_list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_CHAT_ID):
         update.message.reply_text("فقط ادمین اجازه دارد.")
        return
    db = load_db()
    text = "👥 لیست کاربران:\n\n"
    for uid, info in db.get("users", {}).items():
        text += f"• {uid}  →  exp: {time.ctime(info['expire'])}\n"
     update.message.reply_text(text if text else "چیزی یافت نشد.")


# ------------------------------------------------
# اجرای ربات (نسخه صحیح)
# ------------------------------------------------

def main():
    print("🤖 Bot is running...")

    application = Application.builder().token(TOKEN).build()

    # ثبت هندلرها
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate_cmd))
    dp.add_handler(CommandHandler("my_status", my_status))
    dp.add_handler(CommandHandler("start_trading", start_trading))
    dp.add_handler(CommandHandler("admin_list_users", admin_list_users))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":

    main()
