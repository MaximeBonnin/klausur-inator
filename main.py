import requests
from pprintpp import pprint
import json
import urllib
import pandas as pd


# class for individual exam dates
class Termin:
    def __init__(self, t_data, termin_num=0):
        self.all_data = t_data[termin_num]
        self.datum = self.all_data["Klausurtermin"]
        self.dozierend = self.all_data["Pr\u00fcfer"]
        # print(f"-> Added {self.dozierend}: {self.datum}")


# class for modules that contains info about multiple exam dates
class Modul:
    def __init__(self, num, name):
        self.num = num
        self.name = name
        print(f"[{self.num}] {self.name}")
        self.termine = []
        self.find_termine()

    def find_termine(self, n_semester=10):
        # print(f"Finding Exams for [{self.num}] {self.name} | {n_semester} Semesters")
        for sem in range(n_semester):
            data = get_data(modul=self.num, semester=75 - sem)

            for t_num in range(len(data)):
                termin_new = Termin(data, termin_num=t_num)
                self.termine.append(termin_new)


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
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
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

    all_modules = []
    for key, val in all_module_numbers.items():
        print(f"{len(all_modules)+1}/{len(all_module_numbers)} [{round(((len(all_modules)+1)/len(all_module_numbers))*100, 2)} %]")
        data = get_data(modul=key)
        new_module = Modul(num=key, name=val)
        all_modules.append(new_module)

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
    main()
