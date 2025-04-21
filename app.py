from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Placeholder routes for future meditation pages
@app.route("/mindfulness")
def mindfulness():
    return render_template("mindfullness.html")

@app.route("/visualization")
def visualization():
    return render_template("visualization.html")

@app.route("/focus")
def focus():
    return render_template("mantra.html")

@app.route("/kindness")
def kindness():
    return render_template("kindness.html")

if __name__ == "__main__":
    app.run(debug=True)
