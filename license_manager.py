import json
import os
import time
import random
import string

DB_FILE = "db.json"

# بارگذاری دیتابیس
def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "licenses": {}}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ذخیره دیتابیس
def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# ساخت کد اشتراک
def generate_license(days):
    db = load_db()
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    expire_time = int(time.time()) + (days * 86400)

    db["licenses"][code] = {
        "days": days,
        "expire_time": expire_time,
        "used": False
    }

    save_db(db)
    return code

# فعال‌سازی کد اشتراک
def activate_license(user_id, code):
    db = load_db()

    if code not in db["licenses"]:
        return False, "❌ کد معتبر نیست!"

    lic = db["licenses"][code]

    if lic["used"]:
        return False, "❌ این کد قبلاً استفاده شده!"

    # ثبت اشتراک برای کاربر
    db["users"][str(user_id)] = {
        "expire": lic["expire_time"]
    }

    # علامت‌گذاری که استفاده شده
    lic["used"] = True
    save_db(db)

    return True, "✔ اشتراک شما فعال شد!"

# بررسی دسترسی
def check_user_access(user_id):
    db = load_db()
    user = db["users"].get(str(user_id))

    if not user:
        return False

    if time.time() > user["expire"]:
        return False

    return True