import pandas as pd
import numpy as np
import json
import requests


def add_fak():
    fakults = {
        "Sowi": "FAK%253D13",
        "Chemie": "FAK%253D7",
        "Agrar": "FAK%253D11",
        "Bio_Psycho": "FAK%253D9",
        "Forst": "FAK%253D10",
        "Geo": "FAK%253D8",
        "Mathe": "FAK%253D5",
        "Physik": "FAK%253D6",
        "Juri": "FAK%253D2",
        "Medi": "FAK%253D3",
        "Philo": "FAK%253D4",
        "Theo": "FAK%253D1",
        "Allgemein": "FAK%253D17",
        "Wiwi": "FAK%253D12"
    }
    base_url = "https://pruefungsverwaltung.uni-goettingen.de/statistikportal/api/dropdownvalues?type=STUDIENMODUL&forQueryId=215&path="

    dict_of_module_numbers = {
        "ID": [],
        "Fakultät": []
    }

    for key, fak in fakults.items():
        response = requests.get(base_url + fak)
        print(f"GET request for {key}: {response.status_code}")
        resp_json = json.loads(response.text)
        for m in resp_json:
            dict_of_module_numbers["ID"].append(m["value"])
            dict_of_module_numbers["Fakultät"].append(key)

    df = pd.DataFrame.from_dict(dict_of_module_numbers)
    df["ID"] = df["ID"].astype("int64")
    return df


def add_module_nr():
    df = pd.read_csv("module_and_fak.csv")
    fakults = {
        "Sowi": "FAK%253D13",
        "Chemie": "FAK%253D7",
        "Agrar": "FAK%253D11",
        "Bio_Psycho": "FAK%253D9",
        "Forst": "FAK%253D10",
        "Geo": "FAK%253D8",
        "Mathe": "FAK%253D5",
        "Physik": "FAK%253D6",
        "Juri": "FAK%253D2",
        "Medi": "FAK%253D3",
        "Philo": "FAK%253D4",
        "Theo": "FAK%253D1",
        "Allgemein": "FAK%253D17",
        "Wiwi": "FAK%253D12"
    }
    base_url = "https://pruefungsverwaltung.uni-goettingen.de/statistikportal/api/dropdownvalues?type=STUDIENMODUL&forQueryId=215&path="

    dict_of_module_numbers = {
        "ID": [],
        "Modul_Nr": []
    }

    for key, fak in fakults.items():
        response = requests.get(base_url + fak)
        print(f"GET request for {key}: {response.status_code}")
        resp_json = json.loads(response.text)
        for m in resp_json:
            #TODO change hrer
            dict_of_module_numbers["ID"].append(m["value"])
            mod_nr, mod_name = m["label"].split(" ", 1)
            # print(f"{mod_nr} -> {mod_name}")
            dict_of_module_numbers["Modul_Nr"].append(mod_nr)

    df_mod_nr = pd.DataFrame.from_dict(dict_of_module_numbers)
    df_mod_nr["ID"] = df_mod_nr["ID"].astype("int64")

    df_output = pd.merge(df, df_mod_nr, on="ID", how="right")
    print(df_output.head())

    df_output.to_csv("module_data.csv")


def split_module_nr():
    df = pd.read_csv("module_data.csv")

    split_num = df["Modul_Nr"].str.split(".", n=2, expand=True)
    df["Modul_Nr_1"] = split_num[0]
    df["Modul_Nr_2"] = split_num[1]
    df["Modul_Nr_3"] = split_num[2]
    print(df)
    df.to_csv("module_data.csv")


def clean_dataset(data):
    df_raw = data.replace("-", np.nan)

    for c in ["1_0", "1_3", "1_7", "2_0", "2_3", "2_7", "3_0",
              "3_3", "3_7", "4_0", "5_0", "Nicht bestanden", "Bestanden", "Anzahl", "Ohne Note"]:
        df_raw[c] = df_raw[c].fillna(0)

    dtypes = {
        "ID": "int64",
        "Studienmodul": "string",
        "Nicht bestanden": "int64",
        "Ohne Note": "float64",
        "Notenschnitt (nur Bestanden)": "float64",
        "Klausurtermin": "string",
        "Bestanden": "float64",
        "Pr\u00fcfer": "string",
        "Semester": "string",
        "Notenschnitt": "float64",
        "Anzahl": "int64",
        "1_0": "float64",
        "1_3": "float64",
        "1_7": "float64",
        "2_0": "float64",
        "2_3": "float64",
        "2_7": "float64",
        "3_0": "float64",
        "3_3": "float64",
        "3_7": "float64",
        "4_0": "float64",
        "5_0": "float64",
    }
    df_no_na = df_raw.astype(dtypes)

    df_fak = add_fak()

    df_output = pd.merge(df_no_na, df_fak, on="ID", how="right")
    df_output.to_csv("module_and_fak.csv")


def find_my_data(df, my_fak=[], my_bachelor=[], include_sk=False):
    df.dropna(inplace=True)

    if my_fak == ["Alle"]:
        my_fak = ["Sowi", "Chemie", "Agrar", "Bio_Psycho", "Forst", "Geo", "Mathe", "Physik",
                  "Juri", "Medi", "Philo", "Theo", "Allgemein", "Wiwi"]

    if my_bachelor == ["Alle"]:
        my_bachelor = ["B", "M", "Mag", "S"]

    if include_sk:
        my_bachelor.append("SK")
        my_fak.append("Allgemein")

    output = df.query(f"Fakultät.isin(@my_fak) and Modul_Nr_1 == @my_bachelor")

    df_mean_per_doz = find_correct_mean(output).sort_values("Schnitt").reset_index(drop=True)
    df_mean_per_doz["Schnitt"] = df_mean_per_doz["Schnitt"].round(2)
    return df_mean_per_doz


def find_correct_mean(df):
    # per module do: mean * number -> sum all -> divide by total number
    df = df.assign(sum_mean=df["Anzahl"]*df["Notenschnitt"])
    df = df.groupby(["Studienmodul", "Prüfer"], as_index=False).agg({
        "sum_mean": "sum",
        "Anzahl": "sum"
    })

    df = df.assign(Schnitt=df["sum_mean"] / df["Anzahl"])
    df.drop(columns=["sum_mean", "Anzahl"], inplace=True)

    return df


def analyze_main():
    df_raw = pd.read_csv("module_data.csv", index_col=0)
    # print(df_raw.head())
    my_data = find_my_data(df=df_raw, my_fak=["Wiwi"], my_bachelor=["B"], include_sk=False)
    print("Done!")
    return my_data


def get_mod_data(df, mod_name, agg):
    df.dropna(inplace=True)
    subset = df.query("Studienmodul == @mod_name")
    subset = subset[["Studienmodul", "Prüfer", "Notenschnitt", "Anzahl", "Semester"]]

    if not agg:
        subset["Notenschnitt"] = subset["Notenschnitt"].round(2)
        return subset

    output = find_correct_mean(subset)
    output["Schnitt"] = output["Schnitt"].round(2)
    return output


def get_doz_data(df, doz_name, agg):
    df.dropna(inplace=True)
    subset = df.query("Prüfer == @doz_name")
    subset = subset[["Studienmodul", "Prüfer", "Notenschnitt", "Anzahl", "Semester"]]

    if not agg:
        subset["Notenschnitt"] = subset["Notenschnitt"].round(2)
        return subset

    output = find_correct_mean(subset)
    output["Schnitt"] = output["Schnitt"].round(2)
    return output


if __name__ == '__main__':
    analyze_main()

