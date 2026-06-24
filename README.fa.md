<p align="center">
  <a href="./README.md">🇺🇸 English</a> |
  <a href="./README.fa.md">🇮🇷 فارسی</a>
</p>

<p align="center">
  <img src="https://abrehamrahi.ir/o/public/rNf0ej8l/" alt="aiodot logo" width="200">
</p>

<h1 align="center">aiodot 🚀</h1>

<p align="center">
  <b>کتابخانه Async پایتون برای MyDot</b><br>
  ساخت ربات، سلف‌کلاینت، ابزارهای اتوماسیون و یکپارچه‌سازی با MyDot
</p>

---

## درباره پروژه

**aiodot** یک کتابخانه غیررسمی و کاملاً Async برای پلتفرم **MyDot** است.

MyDot یک شبکه اجتماعی میکروبلاگینگ مشابه **X (توییتر سابق)** است که کاربران در آن می‌توانند محتوا منتشر کنند، با دیگران تعامل داشته باشند و جریان محتوای مورد علاقه خود را دنبال کنند.

این کتابخانه با استفاده از **aiohttp** توسعه داده شده و امکان ارتباط آسان با APIهای MyDot را فراهم می‌کند. هدف آن ساده‌سازی ساخت ربات‌ها، سلف‌کلاینت‌ها، ابزارهای مدیریتی و سیستم‌های اتوماسیون است.

---

## ویژگی‌ها

* ⚡ معماری کاملاً Async
* 🔑 ورود با نام کاربری و رمز عبور
* 💾 ذخیره خودکار نشست (Session)
* 🔄 تمدید خودکار توکن
* 📦 پشتیبانی از بیش از ۶۰ Endpoint
* 🖼️ آپلود و مدیریت آواتار
* 💰 مدیریت کیف پول
* 🧵 مدیریت Thread ها
* 🤖 مناسب برای ساخت ربات و سلف
* 🎯 دارای Type Hint کامل

---

## نصب

```bash
pip install aiodot
```

---

## شروع سریع

```python
import asyncio
from aiodot import MyDotClient

async def main():
    async with MyDotClient(session_file="session.json") as client:
        await client.login("username", "password")

        me = await client.get_me()
        print(f"@{me.username}")

        dot = await client.create_dot("سلام از MyDot 🚀")
        print(dot.url)

asyncio.run(main())
```

---

## چرا aiodot؟

* استفاده آسان
* طراحی Async محور
* مدیریت Session داخلی
* پوشش بخش بزرگی از APIهای MyDot
* مناسب برای پروژه‌های اتوماسیون

---

## کاربردها

* 🤖 ساخت ربات برای MyDot
* 👤 ساخت Self Client
* 📊 ابزارهای تحلیل داده
* 📰 انتشار زمان‌بندی‌شده محتوا
* 🔔 مانیتورینگ اعلان‌ها
* 🧪 توسعه افزونه و ابزارهای جانبی

---

## جامعه کاربران

* تلگرام: @aiodotlib
* بله: ble.ir/aiodot
* مستندات: aiodot Docs
* وب‌سایت: karbaladev.ir

---

## سلب مسئولیت

این پروژه یک کتابخانه غیررسمی است و هیچ ارتباطی با تیم رسمی MyDot ندارد.

استفاده از این کتابخانه باید مطابق قوانین و شرایط استفاده MyDot انجام شود.

---

## مجوز

MIT License
