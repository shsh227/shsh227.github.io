import sqlite3
from flask import render_template, Flask, jsonify

app = Flask(__name__)

@app.route("/api/news")
def news_api():
    conn = sqlite3.connect("goodnews.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, url,  date FROM news ORDER BY date DESC LIMIT 5")
    rows = cursor.fetchall()
    articles = []
    for row in rows:
        article = {"title": row[0],
                    "url": row[1],
                    "date": row[2]}
        articles.append(article)
    conn.close()
    return jsonify(articles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)