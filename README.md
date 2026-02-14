# AsrarPayeshKoshan

پروژه وب‌سایت شرکتی با Flask + SQLAlchemy.

## قابلیت‌های پیاده‌سازی‌شده
- صفحه اصلی، درباره ما، معرفی تیم
- **صفحه جزئیات خبر** (`/news/<id>`)
- **صفحه جزئیات خدمت** (`/services/<id>`)
- **صفحه تماس با ما** (`/contact`) با ثبت پیام در دیتابیس
- **پنل مدیریت محتوا** برای یک ادمین (`/admin`)
  - ورود/خروج ادمین
  - مدیریت خبرها و خدمات
  - مدیریت اطلاعات about
  - افزودن داده‌های اصلی صفحه (اسلایدر، بنر، تیم، لینک، شعب، آمار)
  - مشاهده و حذف پیام‌های تماس

## پیش‌نیازها
- Python 3.11+
- pip

## اجرای محلی
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
export SECRET_KEY='change-me'
export DATABASE_URL='sqlite:///site.db'
export ADMIN_USERNAME='admin'
export ADMIN_PASSWORD='admin123'
flask shell -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"
python app.py
```

## اجرای داکر (Ubuntu Server)
```bash
docker compose up --build -d
```

سپس:
- سایت: `http://SERVER_IP:5000`
- پنل ادمین: `http://SERVER_IP:5000/admin/login`

## متغیرهای محیطی
- `DATABASE_URL` (پیش‌فرض: sqlite)
- `SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

## نکته
اگر بخواهید به MySQL لوکال خودتان متصل شوید:
```bash
export DATABASE_URL='mysql+pymysql://user:pass@host/dbname'
```
