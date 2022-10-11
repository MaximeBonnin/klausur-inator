import requests
from pprintpp import pprint
import json
import urllib
import pandas as pd
from numpy import nan


# class for modules that contains info about multiple exam dates
class Modul:
    def __init__(self, num, name):
        self.num = num
        self.name = name
        print(f"[{self.num}] {self.name}")
        self.termine = []
        # self.find_termine()

    def find_termine(self, n_semester=10):
        # print(f"Finding Exams for [{self.num}] {self.name} | {n_semester} Semesters")
        termin_dict = {
            "ID": [],
            "Studienmodul": [],
            "Nicht bestanden": [],
            "Ohne Note": [],
            "Notenschnitt (nur Bestanden)": [],
            "1_0": [],
            "1_3": [],
            "1_7": [],
            "2_0": [],
            "2_3": [],
            "2_7": [],
            "3_0": [],
            "3_3": [],
            "3_7": [],
            "4_0": [],
            "5_0": [],
            "Klausurtermin": [],
            "Bestanden": [],
            "Pr\u00fcfer": [],
            "Semester": [],
            "Notenschnitt": [],
            "Anzahl": [],
        }

        for sem in range(n_semester):
            data = get_data(modul=self.num, semester=75 - sem)
            for t_data in data:
                termin_dict["ID"].append(self.num)
                for key in list(termin_dict.keys())[1:]:
                    termin_dict[key].append(t_data[key])

        if not termin_dict["ID"]:
            print(f"No exam dates found in {n_semester} semesters. Adding NaN.")
            termin_dict["ID"].append(self.num)
            for key in list(termin_dict.keys())[1:]:
                termin_dict[key].append(nan)

        termine_df = pd.DataFrame.from_dict(termin_dict)
        return termine_df


def create_request_body(semester, modul):
    with open("sample_data.json", "r") as f:
        sample_data = f.read()
    sample_data_dict = json.loads(sample_data)

    # edit the request body to fit data needed
    sample_data_dict["data"]["parameters"][0]["associatedFields"][0]["lastValue"] = f"{semester}"   # Semester (75 = SS22)
    sample_data_dict["data"]["parameters"][1]["associatedFields"][1]["lastValue"] = f"{modul}"      # Modul ("3565" = Stats I)

    return str(sample_data_dict["data"])


def get_data(semester="74", modul="3565"):
    url = "https://pruefungsverwaltung.uni-goettingen.de/statistikportal/api/queryexecution/results"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Connection": "Keep - Alive"
    }

    post_data = create_request_body(semester, modul)
    post_data = "data=" + urllib.parse.quote(post_data)
    post_data = post_data.replace("True", "true").replace("False", "false")

    req_body = requests.post(url=url, headers=headers, data=post_data)
    # print(f"{req_body.status_code=}")

    try:
        req_json = req_body.json()
        data = req_json["data"]["records"]
    except TypeError as e:
        print(f"TypeError: {e}")
        data = None

    return data


def save_data(data):
    print("Saving data...")

    print("NOPE")

    print("Data saved!")


def main():
    with open("list_of_module_numbers.json", "r") as f:
        all_module_numbers = json.loads(f.read())
    print(f"{len(all_module_numbers)} modules found.")

    df_so_far = pd.DataFrame(columns=["ID", "Studienmodul", "Nicht bestanden", "Ohne Note", "Notenschnitt (nur Bestanden)",
                                     "1_0", "1_3", "1_7", "2_0", "2_3", "2_7", "3_0", "3_3", "3_7", "4_0", "5_0",
                                     "Klausurtermin", "Bestanden", "Pr\u00fcfer", "Semester", "Notenschnitt", "Anzahl"])

    #TODO if statement for when this doesnt exists yet
    df_so_far = pd.read_csv("module_data.csv")

    all_modules = []
    for key, val in all_module_numbers.items():
        s = set(df_so_far['ID'])
        l = sorted([int(x) for x in list(s)])
        if int(key) in l:
            print("Duplicate module entry. Skipping... ")
            all_modules.append(None)
            continue
        #else:
            # print(f"{key} not in {l}")

        print(f"{len(all_modules)+1}/{len(all_module_numbers)} [{round(((len(all_modules)+1)/len(all_module_numbers))*100, 2)} %]")
        data = get_data(modul=key)
        new_module = Modul(num=key, name=val)
        termine_df = new_module.find_termine()
        df_so_far = df_so_far.append(termine_df)
        df_so_far.to_csv("module_data.csv", index=False)
        all_modules.append(new_module)          # basically just index
        df_so_far = df_so_far.drop_duplicates()
        print(f"Saved.")

    return False


def get_all_module_numbers():
    base_url = "https://pruefungsverwaltung.uni-goettingen.de/statistikportal/api/dropdownvalues?type=STUDIENMODUL&forQueryId=215&path="

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
        "Gemin": "FAK%253D17",
        "Wiwi": "FAK%253D12"
    }

    dict_of_module_numbers = {}
    for key, fak in fakults.items():
        response = requests.get(base_url + fak)
        print(f"GET request for {key}: {response.status_code}")
        resp_json = json.loads(response.text)
        for m in resp_json:
            dict_of_module_numbers[m["value"]] = m["label"]

    print(f"Saving {len(dict_of_module_numbers.keys())} modules found...")
    with open("list_of_module_numbers.json", "w") as f:
        f.write(json.dumps(dict_of_module_numbers, indent=4))
    print("Modules saved!")

    return True


if __name__ == '__main__':
    # get_all_module_numbers()
    run = True
    while run:
        try:
            print("Running main...")
            run = main()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")

    print("Done")