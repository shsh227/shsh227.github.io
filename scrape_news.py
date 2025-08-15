# Import modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sqlite3
import datetime

def scrape_and_store():
    # Configure chrome options
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Set up ChromeDriver Service
    chrome_service = ChromeService("./chromedriver.exe")
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)

    # Extract news headlines from goodnews
    driver.get("https://goodnews.eu/en/")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "rp-medium-two")))
    html = driver.page_source

    # Create database
    conn = sqlite3.connect("goodnews.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, url TEXT NOT NULL, date TEXT NOT NULL)")
    conn.commit()

    # Parse the HTML content
    today = datetime.date.today()
    weekstart = today - timedelta(days=today.weekday())

    content = BeautifulSoup(html, "html.parser")
    articles = content.find_all("article", class_="rp-medium-two")
    for article in articles:
        title = article.find("h3", class_="entry-title")
        url = article.find("a")["href"]
        raw_time = article.find("h4", class_="entry-subtitle").text.strip()
        time = datetime.datetime.strptime(raw_time, "%d %B %Y")
        if weekstart <= time.date() <= today:
            cursor.execute("INSERT INTO news (title, url, date) VALUES (?, ?, ?)", (title.text.strip(), url,  time.date()))
            conn.commit()
    # Close database    
    conn.close()
    driver.quit()

if __name__ == "__main__":
    scrape_and_store()   