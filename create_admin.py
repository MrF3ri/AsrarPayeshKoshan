#!/usr/bin/env python3
import sys
import os

# اضافه کردن مسیر پروژه به PATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Admin

def create_admin():
    app = create_app()
    with app.app_context():
        # چک کردن ادمین وجود دارد یا نه
        existing_admin = Admin.query.first()
        if existing_admin:
            print(f"⚠️  ادمین قبلاً وجود دارد: {existing_admin.username}")
            overwrite = input("آیا میخواهید رمز عبور را ریست کنید؟ (y/n): ")
            if overwrite.lower() == 'y':
                new_password = input("رمز عبور جدید را وارد کنید: ")
                existing_admin.set_password(new_password)
                db.session.commit()
                print("✅ رمز عبور با موفقیت تغییر کرد!")
            return
        
        # ایجاد ادمین جدید
        username = input("نام کاربری: ")
        password = input("رمز عبور: ")
        email = input("ایمیل: ")
        full_name = input("نام کامل: ")
        
        admin = Admin(
            username=username,
            email=email,
            full_name=full_name,
            is_active=True
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"✅ ادمین {username} با موفقیت ایجاد شد!")

if __name__ == "__main__":
    create_admin()