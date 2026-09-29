#!/bin/bash

# Digital Ocean Setup Script برای Telegram Bot
# این فایل رو SSH میں اجرا کنید

echo "🔧 Digital Ocean Setup شروع..."
echo ""

# Update system
echo "1️⃣ System update..."
sudo apt update
sudo apt upgrade -y
echo "✅ System updated"
echo ""

# Install Python
echo "2️⃣ Installing Python..."
sudo apt install -y python3 python3-pip python3-venv
echo "✅ Python installed"
echo ""

# Create app directory
echo "3️⃣ Creating directory..."
mkdir -p ~/telegram-bot
cd ~/telegram-bot
echo "✅ Directory created: ~/telegram-bot"
echo ""

# Create virtual environment
echo "4️⃣ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "✅ Virtual environment created"
echo ""

# Install requirements
echo "5️⃣ Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Packages installed"
echo ""

# Create .env file
echo "6️⃣ Creating .env file..."
cat > .env << EOF
TELEGRAM_TOKEN=YOUR_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
CLAUDE_API_KEY=YOUR_CLAUDE_KEY_HERE
EOF
echo "✅ .env file created"
echo "   👉 باید .env را تغییر بدید!"
echo ""

# Create systemd service
echo "7️⃣ Creating systemd service..."
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null << EOF
[Unit]
Description=Telegram AI Report Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/telegram-bot
Environment="PATH=$HOME/telegram-bot/venv/bin"
EnvironmentFile=$HOME/telegram-bot/.env
ExecStart=$HOME/telegram-bot/venv/bin/python3 $HOME/telegram-bot/do_ai_report_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable telegram-bot.service
echo "✅ Service created"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup کامل شد!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔑 اگر اطلاعات (Token, Chat ID, API Key) دارید:"
echo ""
echo "nano ~/.env"
echo ""
echo "سپس:"
echo ""
echo "sudo systemctl start telegram-bot"
echo "sudo systemctl status telegram-bot"
echo ""
echo "🔍 Logs:"
echo "sudo journalctl -u telegram-bot -f"
