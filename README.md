# ecommerce-price-tracker
A Python application that monitors product prices on e-commerce websites (Amazon, eBay, Walmart) and sends price-drop alerts via email/SMS.
## ⚙️ Features
Real-time price scraping from Amazon, eBay, Walmart

Email/SMS notifications when prices drop below target

Price history tracking with SQLite database

User-friendly web interface (Flask)
## 🚀 Quick Start
## 1. Clone & Install
bash
git clone https://github.com/yourusername/ecommerce-price-tracker.git
cd ecommerce-price-tracker
pip install -r requirements.txt
## 2. Configure
Create .env file:

env
# Email (SendGrid)
SENDGRID_API_KEY=your_api_key
# SMS (Twilio)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

## 3. Run
bash
python run.py
Access at: http://localhost:5000

## 📦 Tech Stack
Backend: Python + Flask

Scraping: BeautifulSoup, Selenium

Database: SQLAlchemy (SQLite)

Notifications: Twilio (SMS), SendGrid (Email)

Scheduler: APScheduler

## 📝 How It Works
User submits product URL and target price

Scraper checks prices hourly

If price ≤ target, sends:

✉️ Email via SendGrid

📱 SMS via Twilio

📜 License
MIT



🎨 Recommended Additions
Add actual screenshots of the web interface

Include a demo video/GIF

Add setup.py if packaging as a PyPI module

Would you like me to expand any section (e.g., API setup, deployment)?

