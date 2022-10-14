from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from analyze_modules import find_my_data
import os

MAIN_PATH = os.path.dirname( __file__ )
DATA_PATH = os.path.join(MAIN_PATH, "module_data.csv")
DF_RAW = pd.read_csv(DATA_PATH, index_col=0)
app = Flask(__name__)


@app.route("/", methods=['GET', "POST"])
def index():
    if request.method == "POST":
        # print(request.form)
        fak = request.form["fak"]
        bach = request.form["bach"]
        sk = request.form["sk"]

        return redirect(url_for("data", fak=fak, bach=bach, sk=sk))

    else:
        fak_options = ["Wiwi", "Sowi", "Philo"]
        bach_options = ["B", "M"]

        return render_template("index.html", fak_options=fak_options, bach_options=bach_options)


@app.route("/<fak>/<bach>/<sk>", methods=["GET", "POST"])
def data(fak, bach, sk):
    if request.method == "POST":
        fak = request.form["fak"]
        bach = request.form["bach"]
        sk = request.form["sk"]
        return redirect(url_for("data", fak=fak, bach=bach, sk=sk))

    if sk == "1":
        sk = True
    else:
        sk = False
    # print("This happened")
    my_data = find_my_data(df=DF_RAW, my_fak=[fak], my_bachelor=[bach], include_sk=sk)
    return render_template("data.html", my_fak=fak, my_bachelor=bach, my_sk=sk, tables=[my_data.to_html(classes='data')], titles=my_data.columns.values)


if __name__ == "__main__":
    print(f"Starting...")
    app.run(debug=True)