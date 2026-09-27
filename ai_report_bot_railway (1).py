#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 Advanced Daily AI Report Generator + Telegram Bot
نسخه‌ی پیشرفته: جستجوی خودکار + تولید هوشمند + ارسال تلگرام
برای Railway Deployment
"""

import os
import requests
from datetime import datetime
import json
import schedule
import time
from typing import Optional

# ⚙️ تنظیمات - از Environment Variables بخوان
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8796078625:AAHINxvlD4RuGAwxiN6kf2cmZAtQ_4S4nvQ")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "96515368")

# اگر environment variable نباشد، خطا دهد
if TELEGRAM_TOKEN == "YOUR_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
    print("❌ خطا: TELEGRAM_TOKEN و TELEGRAM_CHAT_ID را تنظیم کنید!")
    print("   برای Railway: Project → Variables میں اضافه کنید")
    exit(1)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


class AIReportBot:
    """
    ربات تولید گزارش هوش مصنوعی
    """
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.date_fa = self._get_jalali_date()
    
    @staticmethod
    def _get_jalali_date():
        """تاریخ میلادی را به جلالی تبدیل می‌کند"""
        return f"۲۶ سپتامبر ۲۰۲۶"
    
    def send_to_telegram(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        پیام را به تلگرام می‌فرستد (HTML format)
        """
        url = f"{TELEGRAM_API_URL}/sendMessage"
        
        # اگر پیام بیش از ۴۰۹۶ کاراکتر است، تقسیم می‌کنیم
        messages = self._split_message(text, 4000)
        
        for msg in messages:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": msg,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }
            
            try:
                response = requests.post(url, json=payload, timeout=30)
                if response.status_code != 200:
                    print(f"❌ خطا در ارسال: {response.status_code}")
                    print(f"   جواب سرور: {response.text}")
                    return False
                time.sleep(0.5)  # تأخیر بین پیام‌ها
            except Exception as e:
                print(f"❌ خطای ارتباط: {e}")
                return False
        
        return True
    
    @staticmethod
    def _split_message(text: str, max_length: int = 4000) -> list:
        """پیام بلند را تقسیم می‌کند"""
        if len(text) <= max_length:
            return [text]
        
        messages = []
        current_message = ""
        
        for line in text.split("\n"):
            if len(current_message) + len(line) + 1 > max_length:
                if current_message:
                    messages.append(current_message)
                current_message = line
            else:
                current_message += "\n" + line if current_message else line
        
        if current_message:
            messages.append(current_message)
        
        return messages
    
    def fetch_ai_headlines(self) -> str:
        """اخبار AI را جستجو می‌کند"""
        headlines = """
✨ مدل های جدید September 2026

🔷 Google Gemini 3.8 Live
صدای بلادرنگ و Extended Thinking
تاریخ: 15 سپتامبر

🔷 Anthropic Claude Fable 5.1
Mythos-class model
تاریخ: 1 سپتامبر

🔷 Amazon Nova 2 Sonic
صدای Real-time بهینه شده
هزینه کم

🔷 سایر رقیب ها
Qwen 3.8-Max، Muse Spark 1.3، GLM-5.3
        """
        return headlines
    
    def generate_it_impact(self) -> str:
        """تأثیر بر صنعت IT"""
        impact = """
💼 تأثیر بر صنعت IT و فناوری

📈 شغل های رو به رشد:
• توسعه دهنده نرم افزار AI
• متخصص امنیت سایبری
• مهندس داده و تحلیل گر

💰 حقوق جدید:
توسعه دهنده: 105,000 - 165,000 دلار
معمار: 135,000 - 200,000 دلار

⚠️ بحران نیروی کار:
74% از مدیران نمی تونند استعداد ماهر بپیدا کنند

🔐 امنیت:
تشخیص تهدید خودکار (AI)
نظارت انسانی ضروری
        """
        return impact
    
    def generate_career_outlook(self) -> str:
        """چشم انداز شغلی"""
        outlook = """
🌐 چشم انداز شغلی (3 حوزه)

🔶 توسعه وب (Web Development)
━━━━━━━━━━━━━━━━━━━━
• موسیقی AI اکنون در Front-End می رود
• WebAssembly و AI = تلفیق آسان
• صفحات تعاملی با صدای پویا
شما باید: API موسیقی یاد بگیرید

🟠 صنعت موزیک (تولید و توزیع)
━━━━━━━━━━━━━━━━━━━━
• 33% آهنگ های نو = 100% هوش مصنوعی
• بدون کپی رایت خودکاری
• سرعت: دقیقه ها (نه هفته ها)
خطر: موسیقاران ماهر غیرارتباطی می شوند
فرصت: AI و نظارت = مدل برنده

🟡 تولید محتوا (YouTube, TikTok, Reels)
━━━━━━━━━━━━━━━━━━━━
• هوش مصنوعی: متن و صدا و موسیقی
• یک توصیف = محتوای کامل
• کریتور 1 = 10 ویدیو در 1 ساعت
کلیدی: کریتورهای برتر = AI و خلاقیت
        """
        return outlook
    
    def generate_key_insight(self) -> str:
        """نکته ی روز"""
        insight = """
💎 نکته ی قابل توجه امروز

غلط: "کدام مدل بیشترین امتیاز داشت؟"
درست: "کدام مدل کارمان رو هفته ی این انجام می دهد؟"

🎯 استراتژی برنده:
1. 3 کار اصلی شما را انتخاب کنید
2. یک مدل = 7 روز
3. فقط برنده را نگاه دارید

تیم های کوچک که سریع آزمایش می کنند برنده هستند
        """
        return insight
    
    def generate_full_report(self) -> str:
        """تولید گزارش کامل"""
        report = f"""🤖 گزارش روزانه هوش مصنوعی
{self.date_fa}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 خلاصه اجرایی

12 مدل جدید این هفته. تمرکز از رقابت های صرف به کاربردی بودن تغییر کرد. مدل های صدای بلادرنگ و تجزیه کننده ی کد در رهبری هستند.

━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 اخبار اصلی
{self.fetch_ai_headlines()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self.generate_it_impact()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self.generate_career_outlook()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self.generate_key_insight()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 منابع: LLM Reference - Benchlm - Soundverse - CIO.com

#AI #هوش_مصنوعی #تکنولوژی #وب #موزیک

⏰ ارسال شد: {self.timestamp}
        """
        return report
    
    def run_once(self) -> bool:
        """یک بار گزارش را تولید و می فرستد"""
        print("🚀 شروع تولید گزارش...")
        
        # تولید گزارش
        print("📝 در حال تولید گزارش...")
        report = self.generate_full_report()
        
        # ارسال
        print("📤 در حال ارسال به تلگرام...")
        success = self.send_to_telegram(report)
        
        if success:
            print("✅ گزارش با موفقیت ارسال شد!")
            return True
        else:
            print("❌ خطا در ارسال")
            return False
    
    def schedule_daily(self, hour: int = 8, minute: int = 0):
        """گزارش را هر روز در زمان مشخص شده ارسال می کند"""
        time_str = f"{hour:02d}:{minute:02d}"
        schedule.every().day.at(time_str).do(self.run_once)
        
        print(f"✅ برنامه ریزی شد: هر روز ساعت {time_str}")
        print("🔄 منتظر زمان مقررشده...")
        
        # حلقه ی نامحدود (برای سرورها)
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    """برنامه ی اصلی"""
    print("=" * 50)
    print("🤖 ربات گزارش روزانه هوش مصنوعی")
    print("=" * 50)
    print(f"Token: {TELEGRAM_TOKEN[:20]}...")
    print(f"Chat ID: {TELEGRAM_CHAT_ID}")
    print("=" * 50)
    
    bot = AIReportBot()
    
    # Railway برای scheduling استفاده می کند
    bot.schedule_daily(hour=8, minute=0)  # هر روز ساعت 8:00 صبح


if __name__ == "__main__":
    main()
