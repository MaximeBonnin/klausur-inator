# Der Klausur-inator

## Die Idee

Obwohl die Klausurdaten der Uni Göttingen für Studierende in FlexNow einsehbar sind,
ist es nicht leicht dort mehr mit ihnen zu arbeiten. Daher möchte ich eine Möglichkeit
bieten die Klausurdaten zu manipulieren um z.B. herauszufinden welche Klausuren
am leichtesten/schwersten sind oder welche Dozierenden bessere Noten vergeben.

## Umsetzung

### Daten sammeln

Der Server der Uni kann mit einfachen GET und POST requests aufgefordert werden 
alle in FlexNow einsehbaren Daten zu schicken. Dazu nutze ich die Module ``requests``, 
``urllib`` und ``json``. Darüber lässt sich ein relativ kompletter Datensatz erstellen. 

Dabei muss für jedes von ca. 10.000 Modulen eine POST request geschickt werden, 
woraus die Daten für einzelne Klausurtermine (Ich habe nur Daten für die letzten 10 
Semester gesammelt) gefunden werden können. Anschließend können die Daten dann mit 
``pandas`` in Tabellenform gespeichert werden. Zur manipulation verwende ich zudem ``numpy``

Um Anderen etwas Arbeit zu ersparen werde ich meine eigene Version von API Dokumentation 
in diesem Repository hinzufügen, wenn ich dazu komme.

### Daten manipulieren

### App hosten