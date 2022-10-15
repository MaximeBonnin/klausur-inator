from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from analyze_modules import find_my_data, get_mod_data, get_doz_data
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
    return render_template("data.html", my_fak=fak, my_bachelor=bach, my_sk=sk, data=my_data)


@app.route("/modul/<mod>", methods=["GET", "POST"])
def modul(mod):
    if request.method == "POST":
        fak = request.form["fak"]
        bach = request.form["bach"]
        sk = request.form["sk"]
        return redirect(url_for("data", fak=fak, bach=bach, sk=sk))

    else:
        my_data = get_mod_data(df=DF_RAW, mod_name=mod, agg=False)
        my_data_agg = get_mod_data(df=DF_RAW, mod_name=mod, agg=True)
        return render_template("modul.html", mod=mod, data=my_data, agg_data=my_data_agg)


@app.route("/dozierend/<doz>", methods=["GET", "POST"])
def dozierend(doz):
    if request.method == "POST":
        fak = request.form["fak"]
        bach = request.form["bach"]
        sk = request.form["sk"]
        return redirect(url_for("data", fak=fak, bach=bach, sk=sk))

    else:
        my_data = get_doz_data(df=DF_RAW, doz_name=doz, agg=False)
        my_data_agg = get_doz_data(df=DF_RAW, doz_name=doz, agg=True)
        return render_template("dozierend.html", doz=doz, data=my_data, agg_data=my_data_agg)


if __name__ == "__main__":
    print(f"Starting...")
    app.run(debug=True)