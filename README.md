# Golden Agents - Coördinaten Personen/Locaties Notarieel Archief Amsterdam

- [Golden Agents - Coördinaten Personen/Locaties Notarieel Archief Amsterdam](#golden-agents---coördinaten-personenlocaties-notarieel-archief-amsterdam)
  - [Introductie en achtergrond](#introductie-en-achtergrond)
    - [Licentie en hergebruik](#licentie-en-hergebruik)
  - [Data](#data)
    - [Formaten](#formaten)
  - [Methode](#methode)
    - [Personen](#personen)
    - [Locaties](#locaties)
      - [Mappings](#mappings)
        - [Person uuid to deed uri](#person-uuid-to-deed-uri)
        - [Scanname to scan uri](#scanname-to-scan-uri)
  - [Contact](#contact)

## Introductie en achtergrond

Deze dataset bevat een bewerkte versie van de exports van het VeleHanden-indexeringsproject Alle Amsterdamse Akten (https://alleamsterdamseakten.nl/). De data zijn voorzien van URI's op persoonsnamen en records zoals deze in de huidige index op het notarieel archief die beheerd wordt door het Stadsarchief Amsterdam ook kunnen worden aangetroffen (https://archief.amsterdam/indexen/persons?f=%7B%22search_s_register_type_title%22:%7B%22v%22:%22Notari%C3%ABle%20archieven%22%7D%7D). 

De exports zijn voor het laatst in het najaar van 2022 geactualiseerd. Belangrijke bewerkingen die in deze dataset kunnen worden aangetroffen en die momenteel niet in de reguliere Stadsarchief-index zijn opgenomen, zijn:

- Coördinaten (xy) op de scan van de begin- en eindmarkeringen die de documenteenheid (de akte) aanduiden zijn opgenomen;
- Locatienamen en hun locatie op de scan (xywh) .

De huidige index levert deze gegevens (xywh kaders) wel mee voor persoonsnamen, maar voor de volledigheid zijn ook zij in deze repository opgenomen. 

Door opname van scannamen en vooral coördinaten zou deze dataset het bijvoorbeeld gemakkelijker moeten maken om documentherkenning en entiteitsextractie mogelijk te maken op scans van akten waarvan ook HTR beschikbaar is (zie https://transkribus.eu/r/amsterdam-city-archives) en https://gitlab.com/readcoop/webdev/public-docs/-/blob/master/read-and-search/API-README.md).

### Licentie en hergebruik
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7387918.svg)](https://doi.org/10.5281/zenodo.7387918)

Deze dataset is vrij te gebruiken en te hergebruiken onder de Creative Commons Naamsvermelding 4.0 Internationaal (CC BY 4.0) licentie. Dit betekent dat je de dataset mag gebruiken en aanpassen, zolang je de bron vermeldt.

* van Wissen, Leon, Reinders, Jirsi, & van den Heuvel, Pauline. (2022). Golden Agents - Coördinaten Personen/Locaties Notarieel Archief Amsterdam (v1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.7387918

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

De data zijn beschikbaar in de volgende formaten:
* text/csv (CSV)
  * [`locations.csv`]('data/locations.csv')
  * [`persons.csv.gz`]('data/persons.csv.gz')
  * [`records.csv`]('data/records.csv')
* text/turtle (RDF)
  * [`PII_20170117.xml.gz_locations.ttl`](data/PII_20170117.xml.gz_locations.ttl)
  * [`PII_20170117.xml.gz_records.ttl`](data/PII_20170117.xml.gz_records.ttl)
  * [`PII_20170403.xml.gz_locations.ttl`](data/PII_20170403.xml.gz_locations.ttl)
  * [`PII_20170403.xml.gz_records.ttl`](data/PII_20170403.xml.gz_records.ttl)
  * [`PII_20170724.xml.gz_locations.ttl`](data/PII_20170724.xml.gz_locations.ttl)
  * [`PII_20170724.xml.gz_records.ttl`](data/PII_20170724.xml.gz_records.ttl)
  * [`PII_20170731.xml.gz_locations.ttl`](data/PII_20170731.xml.gz_locations.ttl)
  * [`PII_20170731.xml.gz_records.ttl`](data/PII_20170731.xml.gz_records.ttl)
  * [`PII_20171120.xml.gz_locations.ttl`](data/PII_20171120.xml.gz_locations.ttl)
  * [`PII_20171120.xml.gz_records.ttl`](data/PII_20171120.xml.gz_records.ttl)
  * [`PII_20180301.xml.gz_locations.ttl`](data/PII_20180301.xml.gz_locations.ttl)
  * [`PII_20180301.xml.gz_records.ttl`](data/PII_20180301.xml.gz_records.ttl)
  * [`PII_20180921.xml.gz_locations.ttl`](data/PII_20180921.xml.gz_locations.ttl)
  * [`PII_20180921.xml.gz_records.ttl`](data/PII_20180921.xml.gz_records.ttl)
  * [`PII_20190120.xml.gz_locations.ttl`](data/PII_20190120.xml.gz_locations.ttl)
  * [`PII_20190120.xml.gz_records.ttl`](data/PII_20190120.xml.gz_records.ttl)
  * [`PII_20190515.xml.gz_locations.ttl`](data/PII_20190515.xml.gz_locations.ttl)
  * [`PII_20190515.xml.gz_records.ttl`](data/PII_20190515.xml.gz_records.ttl)
  * [`PII_20191017.xml.gz_locations.ttl`](data/PII_20191017.xml.gz_locations.ttl)
  * [`PII_20191017.xml.gz_records.ttl`](data/PII_20191017.xml.gz_records.ttl)
  * [`PII_20200403.xml.gz_locations.ttl`](data/PII_20200403.xml.gz_locations.ttl)
  * [`PII_20200403.xml.gz_records.ttl`](data/PII_20200403.xml.gz_records.ttl)
  * [`PII_20201005.xml.gz_locations.ttl`](data/PII_20201005.xml.gz_locations.ttl)
  * [`PII_20201005.xml.gz_records.ttl`](data/PII_20201005.xml.gz_records.ttl)
  * [`PII_20220215.xml.gz_locations.ttl`](data/PII_20220215.xml.gz_locations.ttl)
  * [`PII_20220215.xml.gz_records.ttl`](data/PII_20220215.xml.gz_records.ttl)
  * [`PII_20220810.xml.gz_locations.ttl`](data/PII_20220810.xml.gz_locations.ttl)
  * [`PII_20220810.xml.gz_records.ttl`](data/PII_20220810.xml.gz_records.ttl)




## Methode

### Personen

Voor de volledigheid is er ook een CSV gemaakt met alle persoonsnamen en hun coördinaten (xywh). Deze is te vinden in [`data/personen.csv.gz`](data/persons.csv.gz) en is gemaakt met de volgende SPARQL-query op de Golden Agentsdata:

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rpp: <https://data.goldenagents.org/ontology/rpp/>
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

#### Mappings

De mappingbestanden die gebruikt worden om de personen aan de juiste akte te koppelen én om de Golden Agents scan-URI te vinden, zijn gemaakt met de volgende query's:

##### Person uuid to deed uri

Zie: [`mapping/person_uuid2deed_uri.json.gz`](mapping/person_uuid2deed_uri.json.gz)

```SPARQL
PREFIX rpp: <https://data.goldenagents.org/ontology/rpp/>
SELECT ?person_uuid ?deed WHERE {

    ?deed a rpp:IndexDocument ;
          rpp:mentionsPerson ?person ;
          rpp:memberOf <https://data.goldenagents.org/datasets/saa/a2a/08953f2f-309c-baf9-e5b1-0cefe3891b37> . # notariële archieven a2a

    ?person a rpp:Person .

    BIND(STRAFTER(STR(?person), '?person=') AS ?person_uuid)
 }
```

##### Scanname to scan uri

Zie: [`mapping/scanname2scan_uri.json.gz`](mapping/scanname2scan_uri.json.gz)

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rpp: <https://data.goldenagents.org/ontology/rpp/>
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
