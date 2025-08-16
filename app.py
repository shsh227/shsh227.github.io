import sqlite3
from flask import render_template, Flask

app = Flask(__name__)

@app.route("/")
def news_scanner():
    conn = sqlite3.connect("goodnews.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, url, img, date FROM news ORDER BY date DESC LIMIT 10")
    rows = cursor.fetchall()
    articles = []
    for row in rows:
        article = {"title": row[0],
                    "url": row[1],
                    "img": row[2],
                    "date": row[3]}
        articles.append(article)
    conn.close()
    return render_template("index.html", articles = articles)

if __name__ == "__main__":
    app.run(debug=True)