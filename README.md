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

Voor de volledigheid is er ook een CSV gemaakt met alle persoonsnamen en hun coördinaten (xywh). Deze is te vinden in `data/personen.csv.gz` en is gemaakt met de volgende SPARQL-query op de Golden Agentsdata:

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rpp: <https://data.goldenagents.org/ontology/roar/>
PREFIX pnv: <https://w3id.org/pnv#>
PREFIX oa: <http://www.w3.org/ns/oa#>

SELECT DISTINCT ?id ?label ?xywh ?scanname { 
    
    # NB: Person names occur only once in this data. 
    # If two deeds are on the same scan and have the same name, the person URIs do not necesarrily correspond.
    ?document a rpp:IndexDocument ;
            rpp:mentionsPerson ?id ;
            rpp:onScan ?scan .
    
    ?id a rpp:Person ;
        pnv:hasName ?pn ;
        rdfs:label ?label .
    
    # The PersonName is the body of an Annotation
    ?annotation a oa:Annotation ;
                oa:hasBody ?pn ;
                oa:hasTarget [ oa:hasSource ?scan ;
                               oa:hasSelector/rdf:value ?xywh ] .
    
    BIND(STRAFTER(STR(?scan), 'scans/') AS ?scanname)
                
}

```


### Locaties

#### Mapping

##### person uuid to deed uri
```sparql
PREFIX rpp: <https://data.goldenagents.org/ontology/roar/>
SELECT ?person_uuid ?deed WHERE {

    ?deed a rpp:IndexDocument ;
          rpp:mentionsPerson ?person ;
          rpp:memberOf <https://data.goldenagents.org/datasets/saa/a2a/08953f2f-309c-baf9-e5b1-0cefe3891b37> . # notariële archieven a2a

    ?person a rpp:Person .

    BIND(STRAFTER(STR(?person), '?person=') AS ?person_uuid)
 }
```

##### scanname to scan uri
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rpp: <https://data.goldenagents.org/ontology/roar/>
SELECT DISTINCT ?scanname ?scan WHERE {
    
    ?deed a rpp:IndexDocument ;
          rpp:onScan ?scan ;
          rpp:memberOf <https://data.goldenagents.org/datasets/saa/a2a/08953f2f-309c-baf9-e5b1-0cefe3891b37> . # notariële archieven a2a
    
    ?scan a rpp:Scan ;
          rdfs:label ?scanname .
    
}
```

## Contact
l.vanwissen@uva.nl
