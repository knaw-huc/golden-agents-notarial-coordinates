# Golden Agents - Coördinaten Personen/Locaties Notarieel Archief Amsterdam

## Introductie en achtergrond

Deze dataset bevat een bewerkte versie van de exports van het VeleHanden-indexeringsproject Alle Amsterdamse Akten (https://alleamsterdamseakten.nl/). De data zijn voorzien van URI's op persoonsnamen en records zoals deze in de huidige index op het notarieel archief die beheerd wordt door het Stadsarchief Amsterdam ook kunnen worden aangetroffen (https://archief.amsterdam/indexen/persons?f=%7B%22search_s_register_type_title%22:%7B%22v%22:%22Notari%C3%ABle%20archieven%22%7D%7D). De exports zijn voor het laatst in het najaar van 2022 geactualiseerd. Belangrijke bewerkingen die in deze dataset kunnen worden aangetroffen en die momenteel niet in de reguliere Stadsarchief-index zijn opgenomen, zijn:

- Coördinaten op de scan van de begin- en eindmarkers die de documenteenheid (de akte) aanduiden zijn opgenomen;
- Locatienamen (buiten Amsterdam, niet op straatniveau) zijn opgenomen (nog niet gestandaardiseerd);
- Coördinaten en afmetingen van kaders die die op de scan locatienamen markeren, zijn opgenomen.

Door opname van scannamen en vooral coördinaten zou deze dataset het bijvoorbeeld gemakkelijker moeten maken om documentherkenning en entiteitsextractie mogelijk te maken op scans van akten waarvan ook HTR beschikbaar is (zie https://transkribus.eu/r/amsterdam-city-archives) en https://gitlab.com/readcoop/webdev/public-docs/-/blob/master/read-and-search/API-README.md).

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
