from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # return render_template("index.html")
    return render_template("index.html")


if __name__ == "__main__":
    print(f"Starting...")
    app.run(debug=True)