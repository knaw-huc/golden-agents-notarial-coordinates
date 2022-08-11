# Golden Agents - Coördinaten Personen/Locaties Notarieel Archief Amsterdam

## Introductie en achtergrond

### Licentie

## Data

Gebruikersinformatie is verwijderd door het `<users>` element uit de bestanden te halen. In dezelfde stap worden de bestanden ge-gzipt:
```bash
#!/bin/bash
for f in *.xml
do
    xmlstarlet ed -N mmm="https://maior.memorix.nl/XSI/3.0/" -d '//mmm:MMM/mmm:export/mmm:users' $f | gzip -9 > $f.gz
done
```

### Formaten

## Methode

### Personen

### Locaties

#### Mapping

```sparql
PREFIX roar: <https://data.goldenagents.org/ontology/roar/>
SELECT ?person_uuid ?deed WHERE {

    ?deed a roar:IndexDocument ;
          roar:mentionsPerson ?person ;
          roar:memberOf <https://data.goldenagents.org/datasets/saa/a2a/08953f2f-309c-baf9-e5b1-0cefe3891b37> . # notariële archieven a2a

    ?person a roar:Person .

    BIND(STRAFTER(STR(?person), '?person=') AS ?person_uuid)
 }
```

## Contact
l.vanwissen@uva.nl
