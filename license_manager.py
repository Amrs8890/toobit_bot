import os
import time
from dotenv import load_dotenv

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)

# -------------------------------
# تنظیمات اولیه
# -------------------------------

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

if not TOKEN:
    raise ValueError("BOT_TOKEN پیدا نشد")

# -------------------------------
# دستورات
# -------------------------------

def start(update: Update, context: CallbackContext):
    user = update.effective_user

    text = f"""سلام {user.first_name} 👋
ربات آماده استفاده است ✅
"""

    keyboard = [
        [InlineKeyboardButton("🚀 شروع ربات", callback_data="start_trading")],
    ]

    if user.id == ADMIN_CHAT_ID:
        keyboard.append(
            [InlineKeyboardButton("🛠 پنل ادمین", callback_data="admin")]
        )

    update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data

    if data == "start_trading":
        query.message.reply_text("🚀 ربات شروع به کار کرد")

    elif data == "admin" and query.from_user.id == ADMIN_CHAT_ID:
        query.message.reply_text("🛠 پنل ادمین فعال شد")

    else:
        query.message.reply_text("❌ دستور نامعتبر")
