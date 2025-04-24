from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mindfulness")
def mindfulness():
    return render_template("mindfullness.html")

@app.route("/visualization")
def visualization():
    return render_template("visualization.html")

@app.route("/kindness")
def kindness():
    return render_template("kindness.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Needed for platforms like Render
    app.run(host="0.0.0.0", port=port, debug=True)
