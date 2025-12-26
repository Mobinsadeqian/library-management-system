# 1. از یک تصویر پایتون آماده و سبک استفاده کن
FROM python:3.13-slim

# 2. متغیرهای محیطی برای جلوگیری از ساخت فایل‌های اضافی پایتون
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. پوشه کاری داخل کانتینر رو بساز
WORKDIR /app

# 4. اول فایل نیازمندی‌ها رو کپی کن و نصب کن (برای کش شدن لایه‌ها)
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. حالا کل کد پروژه رو کپی کن داخل کانتینر
COPY . /app/

# 6. پورت 8000 رو باز کن
EXPOSE 8000

# 7. دستور اجرا شدن برنامه
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]