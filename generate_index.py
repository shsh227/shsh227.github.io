import sqlite3
from jinja2 import Environment, FileSystemLoader

# Load template into template folder
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

# Load data from database
conn = sqlite3.connect('goodnews.db')
cursor = conn.cursor()
cursor.execute("SELECT title, summary, img, date FROM news ORDER BY date DESC LIMIT 10")
rows = cursor.fetchall()
conn.close()

articles = []
for row in rows:
    article = {"title": row[0],
                    "summary": row[1],
                    "img": row[2],
                    "date": row[3]}
    articles.append(article)

# Render html
output = template.render(articles = articles)

# Save to static html file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print("Static index.html generated")