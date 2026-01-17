from flask import Flask, request, redirect, render_template_string
import sqlite3
import string
import random

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS urls (short TEXT, original TEXT)")
    conn.commit()
    conn.close()

def generate_short():
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(6))

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>URL Shortener</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h1>🔗 Python URL Shortener</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter long URL" size="50" required>
        <br><br>
        <button type="submit">Shorten</button>
    </form>

    {% if short_url %}
        <p> Short URL:</p>
        <p><b>{{ short_url }}</b></p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    if request.method == "POST":
        original = request.form["url"]
        short = generate_short()

        conn = sqlite3.connect("urls.db")
        c = conn.cursor()
        c.execute("INSERT INTO urls VALUES (?, ?)", (short, original))
        conn.commit()
        conn.close()

        short_url = request.host_url + short

    return render_template_string(HTML, short_url=short_url)

@app.route("/<short>")
def redirect_url(short):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT original FROM urls WHERE short=?", (short,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return " URL not found"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
