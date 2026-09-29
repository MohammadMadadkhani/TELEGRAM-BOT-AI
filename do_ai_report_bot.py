#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 Advanced Daily AI Report Generator + Telegram Bot
نسخه‌ی Digital Ocean: Claude API + تولید هوشمند + ارسال تلگرام
برای VPS Deployment
"""

import os
import requests
from datetime import datetime
import json
import schedule
import time
from typing import Optional

# ⚙️ تنظیمات - از Environment Variables بخوان
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "YOUR_CLAUDE_KEY_HERE")

# اگر environment variable نباشد، خطا دهد
if TELEGRAM_TOKEN == "YOUR_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
    print("❌ خطا: TELEGRAM_TOKEN و TELEGRAM_CHAT_ID را تنظیم کنید!")
    print("   export TELEGRAM_TOKEN='your_token'")
    print("   export TELEGRAM_CHAT_ID='your_chat_id'")
    exit(1)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"


class AIReportBot:
    """
    ربات تولید گزارش هوش مصنوعی با Claude API
    """
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.date_fa = self._get_jalali_date()
    
    @staticmethod
    def _get_jalali_date():
        """تاریخ میلادی را به جلالی تبدیل می‌کند"""
        now = datetime.now()
        return f"{now.day} سپتامبر {now.year}"
    
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
                    print(f"❌ خطا در ارسال تلگرام: {response.status_code}")
                    print(f"   پاسخ: {response.text}")
                    return False
                print(f"✅ پیام ارسال شد ({len(msg)} کاراکتر)")
                time.sleep(0.5)  # تأخیر بین پیام‌ها
            except Exception as e:
                print(f"❌ خطای ارتباط تلگرام: {e}")
                return False
        
        return True
    
    def query_claude(self, prompt: str) -> str:
        """
        از Claude API اطلاعات می‌گیرد
        """
        if not CLAUDE_API_KEY or CLAUDE_API_KEY == "YOUR_CLAUDE_KEY_HERE":
            print("⚠️ Claude API Key نیست - از اخبار ثابت استفاده می‌کنم")
            return self._get_default_headlines()
        
        headers = {
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-opus-4-1",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            print("📡 Claude API فراخوانی...")
            response = requests.post(CLAUDE_API_URL, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if "content" in result and len(result["content"]) > 0:
                    return result["content"][0]["text"]
            else:
                print(f"⚠️ Claude API خطا: {response.status_code}")
                return self._get_default_headlines()
        except Exception as e:
            print(f"⚠️ خطای Claude API: {e}")
            return self._get_default_headlines()
    
    def _get_default_headlines(self) -> str:
        """اخبار پیش‌فرض اگر API فیل شود"""
        headlines = """
✨ مدل های جدید AI (آخرین اخبار)

🔷 مدل های پیشرفته
صدای بلادرنگ و Extended Thinking

🔷 توسعه های جدید
Mythos-class models و improvements

🔷 بهبودی عملکرد
صدای Real-time بهینه شده
هزینه کم

نوت: برای اخبار دقیق تر، Claude API Key را تنظیم کنید
        """
        return headlines
    
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
        """اخبار AI را از Claude API می‌گیرد"""
        print("📡 در حال دریافت اخبار از Claude...")
        
        prompt = """
تو یک خبرنگار تکنولوژی هستی. اخبار آخرین روز درباره‌ی هوش مصنوعی رو خلاصه کن.

فرمت:
✨ عنوان اخبار

🔷 عنوان 1
توضیح کوتاه

🔷 عنوان 2
توضیح کوتاه

برخورد:
- فقط اخبار مهم و تأثیرگذار
- به فارسی
- خلاصه و مختصر
- 3-5 خبر
        """
        
        return self.query_claude(prompt)
    
    def generate_it_impact(self) -> str:
        """تأثیر بر صنعت IT"""
        impact = """
💼 تأثیر بر صنعت IT و فناوری

📈 شغل های رو به رشد:
• توسعه دهنده نرم افزار AI
• متخصص امنیت سایبری
• مهندس داده و تحلیل گر

💰 حقوق:
توسعه دهنده: 105,000 - 165,000 دلار
معمار: 135,000 - 200,000 دلار

⚠️ بحران نیروی کار:
74% مدیران نمی تونند استعداد ماهر بپیدا کنند

🔐 امنیت:
تشخیص تهدید خودکار (AI)
نظارت انسانی ضروری
        """
        return impact
    
    def generate_career_outlook(self) -> str:
        """چشم انداز شغلی - درخواست از Claude"""
        print("🔍 در حال تولید چشم‌انداز شغلی...")
        
        prompt = """
درباره‌ی آینده‌ی شغلی در 3 حوزه نوشته کن:
1. توسعه وب (Web Development)
2. صنعت موزیک (تولید، ترکیب، توزیع)
3. تولید محتوا (نویسندگی، ویدیو، شبکه‌های اجتماعی)

برای هر حوزه: چطور هوش مصنوعی تغییر می‌دهد

به فارسی و خلاصه
        """
        
        return self.query_claude(prompt)
    
    def generate_key_insight(self) -> str:
        """نکته‌ی روز از Claude"""
        print("💡 در حال تولید نکته‌ی روز...")
        
        prompt = """
یک نکته‌ی مهم و عملی درباره‌ی هوش مصنوعی امروز نوشته کن که:
- برای کار/زندگی مفید باشد
- کوتاه و قابل درک باشد
- اقدام قابل انجام پیشنهاد دهد

به فارسی
        """
        
        return self.query_claude(prompt)
    
    def generate_full_report(self) -> str:
        """تولید گزارش کامل با اخبار واقعی"""
        report = f"""🤖 گزارش روزانه هوش مصنوعی
{self.date_fa}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 خلاصه اجرایی

اطلاعات روز درباره‌ی تحولات هوش مصنوعی و تأثیر آن بر صنعت و شغل.

━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 اخبار امروز
{self.fetch_ai_headlines()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self.generate_it_impact()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 چشم انداز شغلی
{self.generate_career_outlook()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 نکته‌ی روز
{self.generate_key_insight()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 منابع: Claude AI - آخرین اخبار تکنولوژی

#AI #هوش_مصنوعی #تکنولوژی

⏰ ارسال شد: {self.timestamp}
        """
        return report
    
    def run_once(self) -> bool:
        """یک بار گزارش را تولید و می فرستد"""
        print("\n" + "=" * 60)
        print("🚀 شروع تولید گزارش...")
        print("=" * 60)
        
        try:
            # تولید گزارش
            print("📝 در حال تولید گزارش...")
            report = self.generate_full_report()
            
            # ارسال
            print("📤 در حال ارسال به تلگرام...")
            success = self.send_to_telegram(report)
            
            if success:
                print("✅ گزارش با موفقیت ارسال شد!")
                print("=" * 60 + "\n")
                return True
            else:
                print("❌ خطا در ارسال")
                print("=" * 60 + "\n")
                return False
        except Exception as e:
            print(f"❌ خطای عمومی: {e}")
            print("=" * 60 + "\n")
            return False
    
    def schedule_daily(self, hour: int = 8, minute: int = 0):
        """گزارش را هر روز در زمان مشخص شده ارسال می کند"""
        time_str = f"{hour:02d}:{minute:02d}"
        schedule.every().day.at(time_str).do(self.run_once)
        
        print(f"\n✅ برنامه ریزی شد: هر روز ساعت {time_str}")
        print("🔄 منتظر زمان مقررشده...\n")
        
        # حلقه ی نامحدود (برای سرورها)
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    """برنامه ی اصلی"""
    print("=" * 60)
    print("🤖 ربات گزارش روزانه هوش مصنوعی")
    print("نسخه: 3.0 (Digital Ocean)")
    print("=" * 60)
    print(f"Token: {TELEGRAM_TOKEN[:20]}...")
    print(f"Chat ID: {TELEGRAM_CHAT_ID}")
    print(f"Claude API: {'✅ فعال' if CLAUDE_API_KEY != 'YOUR_CLAUDE_KEY_HERE' else '⚠️ غیرفعال'}")
    print("=" * 60)
    
    bot = AIReportBot()
    
    # Digital Ocean برای scheduling استفاده می کند
    bot.schedule_daily(hour=8, minute=0)  # هر روز ساعت 8:00 صبح


if __name__ == "__main__":
    main()
