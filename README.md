# Der Klausur-inator

## Die Idee

Obwohl die Klausurdaten der Uni Göttingen für Studierende in FlexNow einsehbar sind,
ist es nicht leicht dort mehr mit ihnen zu arbeiten. Daher möchte ich eine Möglichkeit
bieten, die Klausurdaten zu manipulieren um z. B. herauszufinden, welche Klausuren
am leichtesten/schwersten sind oder welche Dozierenden bessere Noten vergeben.

Funktionen die enthalten sein sollten sind:
1. Das Filtern nach Modulen, 
2. Das Filtern nach Dozierenden, 
3. Das Suchen nach bestimmen Modulen.

## Umsetzung

### Daten sammeln

Der Server der Uni kann mit einfachen GET und POST requests aufgefordert werden, 
alle in FlexNow einsehbaren Daten zu schicken. Dazu nutze ich die Module ``requests``, 
``urllib`` und ``json``. Darüber lässt sich ein relativ kompletter Datensatz erstellen. 

Dabei muss für jedes von ca. 10.000 Modulen eine POST request geschickt werden, 
woraus die Daten für einzelne Klausurtermine (Ich habe nur Daten für die letzten 10 
Semester gesammelt) gefunden werden können. Anschließend können die Daten dann mit 
``pandas`` in Tabellenform gespeichert werden. Zur Manipulation verwende ich zudem ``numpy``.

Um Anderen etwas Arbeit zu ersparen werde ich meine eigene mini Version von API Dokumentation 
in diesem Repository hinzufügen, wenn ich dazu komme. Zu finden als ``documentation.md``. Zudem ist
der Datensatz, welchen ich benutze als ``module_data.csv`` in diesem Repository zu finden.

### Daten manipulieren
Ich habe die Daten über mehrere Schritte mit ``pandas`` Funktionen verändert.
Im Nachhinein hätte ich es gerne in einem Jupyter Notebook gemacht, da dies übersichtlicher wäre.
Die Suche und Manipulation der Daten bei Nutzeranfragen werden über Funktionen in ``analyze_modules.py`` gehandhabt.

### App hosten
Hosting der APP läuft über das Modul ``gunicorn`` und Heroku. Zu finden ist die App [hier](klausur-inator.herokuapp.com).
