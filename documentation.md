# Georg-August Universität Göttingen Studierendendaten API documentation
No authentication is needed so this data is accessible to anyone.

## Getting module IDs
The server uses internal module IDs that are not connected to module numbers
as far as I could tell. To get the module numbers I used the GET request
sent when using the dropdown menu in FlexNow.

``https://pruefungsverwaltung.uni-goettingen.de/statistikportal/api/dropdownvalues?type=STUDIENMODUL&forQueryId=215&path=``

For the ``path=`` parameter you can add the code for the following departments:

|  Department |  Code |
|---|---|
| Social Science  |  FAK%253D13 |
| Chemistry  | FAK%253D7  |
| Agriculture  |  FAK%253D11 |
|  Biology / Psychology | FAK%253D9  |
| Forestry  | FAK%253D10  |
|  Geology | FAK%253D8  |
|  Maths |  FAK%253D5 |
| Physics  | FAK%253D6  |
| Law  | FAK%253D2  |
|  Medicine |  FAK%253D3 |
| Philosophy  | FAK%253D4  |
|  Theology | FAK%253D1  |
|  Non-specific | FAK%253D17  |
|  Economics / Business | FAK%253D12  |

This endpoint gives responses in json format:

**Sample response:**

    [
        {
            "value": "1",
            "label: "Module Name"
        },
        {
            "value": "2",
            "label: "Module 2 Name"
        }
    ]
    
## Getting module data
Now I had the list of Module IDs so I could use POST requests to get more data.

``https://pruefungsverwaltung.uni-goettingen.de/statistikportal/api/queryexecution/results``

You can find a sample request in the directory named ``sample_data.json``. There
you can see the general structure of what the post request should look like.
In order to get data for different modules the only things that need to be changed
are:
1. ``/data/parameters/0/associatedFields/0/lastValue`` for the semester (75 is Summer 22)
2. ``/data/parameters/1/associatedFields/1/lastValue`` using the module number


Besides that, headers need to include ``"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"`` 
in order to work properly.

I did not experiment much further with different types of queries besides number 
``215`` which returns module data like this:


**Sample response:**

    [
        {
            "2_3": "15.0",
            "Studienmodul": "Seminar zur Rechnungslegung und Wirtschaftspr\u00fcfung",
            "Nicht bestanden": "2",
            "Ohne Note": "",
            "Notenschnitt (nur Bestanden)": "2.167",
            "1_0": "5.0",
            "1_7": "15.0",
            "2_7": "10.0",
            "3_7": "5.0",
            "5_0": "10.0",
            "4_0": "",
            "Klausurtermin": "20.05.2022",
            "3_0": "5.0",
            "Bestanden": "18",
            "Pr\u00fcfer": "Hitz",
            "2_0": "20.0",
            "Semester": "SoSe22",
            "Notenschnitt": "2.450",
            "3_3": "5.0",
            "Anzahl": 20.0,
            "1_3": "10.0"
        }
    ]