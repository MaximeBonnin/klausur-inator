from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from analyze_modules import find_my_data, get_mod_data, get_doz_data
import os

MAIN_PATH = os.path.dirname( __file__ )
DATA_PATH = os.path.join(MAIN_PATH, "module_data.csv")
DF_RAW = pd.read_csv(DATA_PATH, index_col=0)
app = Flask(__name__)


def handle_data_request(request):
    print(request.form)
    fak = request.form["fak"]
    bach = request.form["bach"]
    sk = request.form["sk"]
    srch = request.form["srch"]

    if len(srch) > 0:
        return redirect(url_for("searched_data", fak=fak, bach=bach, sk=sk, srch=srch))

    return redirect(url_for("data", fak=fak, bach=bach, sk=sk))



@app.route("/", methods=['GET', "POST"])
def index():
    if request.method == "POST":
        return handle_data_request(request)

    return render_template("index.html")


@app.route("/<fak>/<bach>/<sk>", methods=["GET", "POST"])
def data(fak, bach, sk):
    if request.method == "POST":
        return handle_data_request(request)

    if sk == "1":
        sk = True
    else:
        sk = False

    my_data = find_my_data(df=DF_RAW, my_fak=[fak], my_bachelor=[bach], include_sk=sk)
    return render_template("data.html", my_fak=fak, my_bachelor=bach, my_sk=sk, data=my_data)


@app.route("/<fak>/<bach>/<sk>/<srch>", methods=["GET", "POST"])
def searched_data(fak, bach, sk, srch):
    if request.method == "POST":
        return handle_data_request(request)

    if sk == "1":
        sk = True
    else:
        sk = False

    my_data = find_my_data(df=DF_RAW, my_fak=[fak], my_bachelor=[bach], include_sk=sk)
    if len(srch) > 0:
        my_data = my_data[my_data["Studienmodul"].str.match(srch, case=False)]
    return render_template("data.html", my_fak=fak, my_bachelor=bach, my_sk=sk, srch=srch, data=my_data)


@app.route("/modul/<mod>", methods=["GET", "POST"])
def modul(mod):
    if request.method == "POST":
        return handle_data_request(request)

    else:
        my_data = get_mod_data(df=DF_RAW, mod_name=mod, agg=False)
        my_data_agg = get_mod_data(df=DF_RAW, mod_name=mod, agg=True)
        return render_template("modul.html", mod=mod, data=my_data, agg_data=my_data_agg)


@app.route("/dozierend/<doz>", methods=["GET", "POST"])
def dozierend(doz):
    if request.method == "POST":
        return handle_data_request(request)

    else:
        my_data = get_doz_data(df=DF_RAW, doz_name=doz, agg=False)
        my_data_agg = get_doz_data(df=DF_RAW, doz_name=doz, agg=True)
        return render_template("dozierend.html", doz=doz, data=my_data, agg_data=my_data_agg)


if __name__ == "__main__":
    print(f"Starting...")
    app.run(debug=True)