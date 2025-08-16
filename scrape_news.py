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
import re

def scrape_and_store():
    # Configure chrome options
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")

    # Set up ChromeDriver Service
    chrome_service = ChromeService("./chromedriver.exe")
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)

    # Extract news headlines from goodnews
    driver.get("https://goodnews.eu/en/")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "rp-medium-two")))
    html = driver.page_source
    content = BeautifulSoup(html, "html.parser")
    articles = content.find_all("article", class_="rp-medium-two")
    
    # Test run
    print(f"Page title: {driver.title}")
    print(f"Found {len(articles)} articles")

    # Set the date variables
    today = datetime.date.today()
    weekstart = today - datetime.timedelta(days=today.weekday())
    monthstart = today.replace(day=1)

    # Create database
    db = "goodnews.db"
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, url TEXT NOT NULL, img TEXT NOT NULL, date TEXT NOT NULL)")
    cursor.execute("DELETE FROM news")

    # Fill database
    for article in articles:
        title_tag = article.find("h3", class_="entry-title")
        if title_tag:
            title = title_tag.find("a").text.strip()
            print(f"Title: {title}")
        else:
            title = None

        link_tag = article.find("h3", class_="entry-title").find("a")
        if link_tag and link_tag["href"]:
            url = link_tag["href"]
            print(f"URL: {url}")
        else:
            url = None

        img_tag = article.find("div", class_="entry-thumb")
        if img_tag:
            img = img_tag.find("img")["src"]
            print(f"Image: {img}")
        else:
            img = None

        date_tag = article.find("h4", class_="entry-subtitle")
        if date_tag:
            raw_time = date_tag.get_text(strip=True)
            find_number = re.search(r'\d', raw_time)
            if find_number is None:
                only_raw_time = raw_time
            else:
                only_raw_time = raw_time[find_number.start():].strip()
            print(f"Date: {only_raw_time}")
        else:
            only_raw_time = None 

        if only_raw_time:
            time = datetime.datetime.strptime(only_raw_time, "%d %B %Y").date()
        else:
            time = None
        
        if title and url and time and img:
            if monthstart <= time <= today:
                cursor.execute("INSERT INTO news (title, url, img, date) VALUES (?, ?, ?, ?)", (title, url, img, str(time)))
                
    conn.commit()

    print("Database storage:")
    stored = cursor.execute("SELECT * FROM news")
    rows = stored.fetchall()
    for row in rows:
        print(row)
    
    # Close database    
    conn.close()
    driver.quit()

if __name__ == "__main__":
    scrape_and_store()   