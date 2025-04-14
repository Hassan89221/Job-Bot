# 💼 Job Scraper Bot

This Python-based **Job Scraper Bot** automates the process of scraping job listings from [ActuaryList.com](https://www.actuarylist.com), saves the data in a structured CSV file, and sends an email notification with the file attached. It's designed to run on a schedule via Windows Task Scheduler, using robust path handling and logging to ensure reliability.

---

## 🚀 Features

- Scrapes job title, company, location, posted time, and job link
- Handles multiple pages with pagination
- Stores raw HTML for each job to avoid redundant scraping
- Extracts data using BeautifulSoup
- Saves results in `data.csv`
- Sends an email notification with CSV attachment
- Logs all activities and errors into `scraper.log`

---

## 🛠️ Technologies Used

- Python
- Selenium
- BeautifulSoup (bs4)
- pandas
- smtplib (for email)
- dotenv (for managing credentials)
- Windows Task Scheduler (for automation)

---

## 📁 Project Structure

job_scraper_bot/ │ ├── data/ # Stores raw job HTML files ├── .env # Environment variables (Email, Password, etc.) ├── scraper.log # Log file for scraping events/errors ├── data.csv # Final scraped data └── job_scraper.py # Main script

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following:

Email=your_email@gmail.com Password=your_email_password_or_app_password Receiver_mail=receiver_email@example.com

---

## ⚙️ How to Run

1. **Install Dependencies**

pip install selenium beautifulsoup4 pandas python-dotenv lxml
Download ChromeDriver
Make sure ChromeDriver is installed and matches your Chrome version.
Download: https://sites.google.com/a/chromium.org/chromedriver/

Run the Script

python job_scraper.py
Schedule with Task Scheduler (Optional)
Use Windows Task Scheduler to run this script at specific intervals.

📬 Email Report
After successful execution:

You’ll receive an email at the receiver address

The email contains:

A brief summary (number of jobs scraped)

Attached CSV with complete job data

📌 Notes
Make sure "Allow less secure apps" is enabled for Gmail or use an App Password for enhanced security.

The scraper is currently configured to scrape the first 5 pages from actuarylist.com. You can change this in the range(1, 6) loop.

All job HTML files are saved in the /data folder for future parsing.

✅ Sample Output

Page 1: 10 jobs found
Page 2: 9 jobs found
...
Total jobs scraped: 45
Email notification sent
🧠 Author Comments (Inline in Code)
The code is fully documented with inline comments in Urdu and English to help beginners understand each step, especially when automating via Task Scheduler.

📞 Contact
If you face any issues or want to collaborate, feel free to reach out via GitHub Issues or email.

📄 License
MIT License

---

Let me know if you’d like to include screenshots, a video demo link, or GitHub
