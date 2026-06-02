# Goldoni Project API

این پروژه بک‌اند یک اپلیکیشن فروش گل است که با Django و Django REST Framework توسعه داده شده و به یک اپلیکیشن Flutter متصل می‌شود. هدف اصلی، پیاده‌سازی یک API ساختاریافته برای مدیریت کاربران، محصولات و سفارش‌ها بوده است.

## اپلیکیشن 
لینک ریپازیتوری اپلیکیشن ساخته شده توسط همکارم :
https://github.com/FarzinNs83/goldooni.git

## تکنولوژی‌ها
- Python
- Django 5
- Django REST Framework
- SimpleJWT (احراز هویت JWT)
- drf-yasg (Swagger / ReDoc)
- SQLite (پیش‌فرض)

## امکانات اصلی
- ثبت‌نام و ورود با OTP
- مدیریت پروفایل کاربر و آدرس‌ها
- لیست محصولات، دسته‌بندی‌ها، جستجو، لایک محصول و لایک/دیس‌لایک کامنت
- مدیریت سبد خرید و ثبت سفارش
- لیست مقالات وبلاگ و لایک/دیس‌لایک مقاله
- FAQ برای چت‌بات
- مستندسازی API با Swagger و ReDoc

## ساختار پروژه
- `config/` تنظیمات اصلی پروژه، URLها و WSGI/ASGI
- `accounts/` احراز هویت، پروفایل، آدرس‌ها
- `products/` محصولات، دسته‌بندی، جستجو، لایک‌ها
- `cart/` سبد خرید، آیتم‌ها، سفارش‌ها
- `blog/` مقالات و لایک/دیس‌لایک مقاله
- `chatbot/` سوالات FAQ و پاسخ‌ها

## پیش‌نیازها
- Python 3.11+
- pip

## نصب و اجرا
1. کلون پروژه:

```bash
git clone https://github.com/elicipher/Goldoni-Shop.git
cd Goldoni-Shop
```

2. ساخت و فعال‌سازی محیط مجازی:

```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

3. نصب وابستگی‌ها:

```bash
pip install -r requirements.txt
```

4. اعمال مایگریشن:

```bash
python manage.py migrate
```

5. اجرای سرور:

```bash
python manage.py runserver
```

## آدرس‌های مهم
- Swagger UI: `http://127.0.0.1:8000/`
- Swagger UI (Alternative): `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`
- Admin: `http://127.0.0.1:8000/api/admin/`

## احراز هویت (JWT)
این پروژه از JWT استفاده می‌کند. برای endpointهای محافظت‌شده، هدر زیر را ارسال کنید:

```http
Authorization: Bearer <access_token>
```

توکن‌ها در جریان OTP/ثبت‌نام برمی‌گردند و refresh هم از مسیر زیر قابل استفاده است:
- `POST /api/account/api/token/refresh/`

## API Endpoints

### Accounts (`/api/account/`)
- `POST send-otp-code/`
- `POST verify_otp_code/`
- `POST register/`
- `GET/PATCH profile/`
- `POST api/token/refresh/`
- `GET api/check/access_token/`
- `POST logout/`
- `my-addresses/` (router):
  - `GET / POST /api/account/my-addresses/`
  - `GET / PATCH / DELETE /api/account/my-addresses/<id>/`

### Products (`/api/products/`)
- `GET slider/`
- `GET index/`
- `GET categories/`
- `GET categories/<category_id>/`
- `GET amazing/`
- `GET top/`
- `GET new/`
- `GET retrieve/<pk>/`
- `POST like/<product_id>/`
- `POST comment/<comment_id>/like/`
- `GET favorite_list/`
- `GET search/?q=<keyword>`
- `GET search_category/?q=<keyword>`

### Cart & Orders (`/api/cart/`)
- `POST add_item/`
- `GET/PATCH/DELETE rud_item/<pk>/`
- `GET list_items/`
- `POST order/`
- `GET order/shipping/`
- `GET order/delivered/`
- `GET order/returned/`
- `GET order/all/`
- `GET/PATCH/DELETE order/retrieve/<order_id>/`

### Blog (`/api/blog/`)
- `GET list_article/`
- `GET detail_article/<id>/`
- `POST like_article/<article_id>/`

### Chatbot (`/api/chat_box/`)
- `GET questions/`
- `GET answer/<pk>/`

## نکات توسعه
- دیتابیس پیش‌فرض: `db.sqlite3`
- فایل‌های رسانه‌ای در `media/` ذخیره می‌شوند.
- در وضعیت فعلی پروژه:
  - `DEBUG = True`
  - `ALLOWED_HOSTS = ['*']`
  - `CORS_ALLOW_ALL_ORIGINS = True`

برای محیط Production حتما این مقادیر را ایمن‌سازی کنید.


