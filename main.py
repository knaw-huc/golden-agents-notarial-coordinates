"""
main

Usage:
    main.py <inputfolder> <outputfolder>
    main.py <inputfolder> <outputfolder> --mappingfile 'mapping/person_uuid2deed_uri.json'
    main.py <inputfolder> <outputfolder> --output RDF
    main.py (-h | --help)

Arguments:
  inputfolder        Folder with VeleHanden export files.
  outputfolder       Folder to write CSV or RDF files to.

Options:
    -h --help       Show this screen.
    --mappingfile   Location of the person_uuid to deed URI file [default: "mapping/person_uuid2deed_uri.json"]
    --output (CSV|RDF) [default: CSV]
"""

# TODO: wkt?
# [d["x"], d["y"]],
# [d["x"] + d["w"], d["y"]],
# [d["x"] + d["w"], d["y"] - d["h"]],
# [d["x"], d["y"] - d["h"]],
# [d["x"], d["y"]],

import os
import json

import pandas as pd

import lxml
import lxml.etree as ET

from docopt import docopt

NS = {"MMM": "https://maior.memorix.nl/XSI/3.0/"}

with open("mapping/person_uuid2deed_uri.json") as infile:
    person_uuid2deed_uri = json.load(infile)


def parse_files(folder_path: str, output="CSV"):

    filenames = os.listdir(folder_path)
    filenames = [i for i in sorted(filenames) if i.endswith(".xml.gz")]

    record_data_all = []
    location_data_all = []

    # Parse every file in the folder
    for fn in filenames:
        print(f"Parsing {fn}...")
        fpath = os.path.join(folder_path, fn)

        tree = ET.parse(fpath)
        record_data, location_data = get_records(tree)

        record_data_all += record_data
        location_data_all += location_data

        break

    # And then save it somewhere
    if output == "CSV":
        save_to_csv(record_data_all, location_data_all)

    elif output == "RDF":

        save_to_rdf(record_data_all, location_data_all)


def save_to_csv(record_data, location_data):
    print("Saving as CSV!")

    df_records = pd.DataFrame(record_data)
    df_locations = pd.DataFrame(location_data)

    df_records.to_csv(os.path.join(folder_path, f"records.csv"), index=False)
    df_locations.to_csv(os.path.join(folder_path, f"locations.csv"), index=False)


def save_to_rdf(record_data, location_data, format="turtle"):
    print("Saving as RDF!")
    from rdflib import (
        ConjunctiveGraph,
        Literal,
        Namespace,
        RDF,
        RDFS,
        URIRef,
        XSD,
        DCTERMS,
        BNode,
    )
    from rdflib.resource import Resource

    g = ConjunctiveGraph()
    OA = Namespace("http://www.w3.org/ns/oa#")
    RPP = Namespace("https://data.goldenagents.org/ontology/rpp/")
    PREZI = Namespace("http://iiif.io/api/presentation/3#")

    g.bind("dcterms", DCTERMS)
    g.bind("oa", OA)
    g.bind("iiif_prezi", PREZI)
    g.bind("rpp", RPP)

    with open("mapping/scanname2scan_uri.json") as infile:
        scanname2scan_uri = json.load(infile)

    # We transform the coordinates on the page into annotations on the material

    # First the records (start/end)

    # Problem here: there is no RDF serialization of https://iiif.io/api/annex/openannotation/
    # So this needs to be changed once the context is updated.
    # Let's pretend it's in the iiif3_prezi context: https://iiif.io/api/presentation/3/context.json

    for record in record_data:

        for kind in ["begin", "end"]:
            x, y = record[f"{kind}_coordinates"]
            scanname = record[f"{kind}_scanname"]

            scanURI = scanname2scan_uri.get(scanname)
            if not scanURI:
                continue

            annotation = Resource(g, BNode())
            annotation.add(RDF.type, OA.Annotation)

            pointSelector = Resource(g, BNode())
            pointSelector.add(
                RDF.type, PREZI.PointSelector
            )  # This does not exist, see: https://iiif.io/api/annex/openannotation/
            pointSelector.add(PREZI.x, Literal(x, datatype=XSD.decimal))
            pointSelector.add(PREZI.y, Literal(y, datatype=XSD.decimal))

            specificResource = Resource(g, BNode())
            specificResource.add(RDF.type, OA.SpecificResource)
            specificResource.add(OA.hasSource, URIRef(scanURI))
            specificResource.add(OA.hasSelector, pointSelector.identifier)

            annotation.add(OA.textualBody, Literal(kind))
            annotation.add(OA.hasTarget, specificResource.identifier)

    g.serialize("records.ttl", format=format)

    # And now the locations

    g = ConjunctiveGraph()
    g.bind("dcterms", DCTERMS)
    g.bind("oa", OA)
    g.bind("iiif_prezi", PREZI)
    g.bind("rpp", RPP)

    for loc in location_data:
        location_uri = loc["id"]
        label = loc["label"]
        xywh = loc["xywh"]
        scanname = loc["scanname"]

        scanURI = scanname2scan_uri.get(scanname)
        if not scanURI:
            continue

        location = Resource(g, URIRef(location_uri))
        location.add(RDF.type, RPP.Location)
        location.add(RDFS.label, Literal(label))

        annotation = Resource(g, BNode())
        annotation.add(RDF.type, OA.Annotation)

        fragmentSelector = Resource(g, BNode())
        fragmentSelector.add(RDF.type, OA.FragmentSelector)
        fragmentSelector.add(
            DCTERMS.conformsTo, URIRef("http://www.w3.org/TR/media-frags/")
        )
        fragmentSelector.add(RDF.value, Literal(xywh))

        specificResource = Resource(g, BNode())
        specificResource.add(RDF.type, OA.SpecificResource)
        specificResource.add(OA.hasSource, URIRef(scanURI))
        specificResource.add(OA.hasSelector, fragmentSelector.identifier)

        annotation.add(OA.hasBody, location.identifier)
        annotation.add(OA.hasTarget, specificResource.identifier)

    g.serialize("locations.ttl", format=format)


def get_records(tree):

    # Find all the records (=deeds)
    records = tree.findall(
        "MMM:export/MMM:record",
        namespaces=NS,
    )

    record_data = []
    location_data = []

    for r in records:

        # Get scan coordinates (begin/end)
        (scan_begin_coordinates, scan_begin_scanname), (
            scan_end_coordinates,
            scan_end_scanname,
        ) = get_scan_coordinates(r)

        # Find the elements
        person_elements = r.xpath(
            ".//MMM:record[MMM:field/@name = 'person_name']", namespaces=NS
        )
        location_elements = r.xpath(
            ".//MMM:record[MMM:field/@name = 'location_name']",
            namespaces=NS,
        )

        # Then, get the _current_ deed uuid, as is used on the SAA website (archief.amsterdam/indexen)
        # We do this through the only uuids that were kept: the person uuids
        person_uuids = [i.attrib["uuid"] for i in person_elements]
        deed_uri = get_deed_uri(person_uuids)

        record_data.append(
            {
                "id": deed_uri,
                "begin_coordinates": scan_begin_coordinates,
                "begin_scanname": scan_begin_scanname,
                "end_coordinates": scan_end_coordinates,
                "end_scanname": scan_end_scanname,
            }
        )

        # Now the locations
        for n, e in enumerate(location_elements, 1):

            if deed_uri:
                location_uri = deed_uri + f"?location=Location{n}"
            else:
                location_uri = ""

            if d := get_coordinates(e):

                r_data = {
                    "id": location_uri,
                    "label": d["name"],
                    "xywh": [d["x"], d["y"], d["w"], d["h"]],
                    "scanname": d["scanname"],
                }

                location_data.append(r_data)

    return record_data, location_data


def get_coordinates(e: lxml.etree.Element) -> dict:

    try:
        name = e.xpath(
            "MMM:field[@name = 'location_name']/MMM:value/text()", namespaces=NS
        )[0]
        x = e.xpath("MMM:field[@name = 'x']/MMM:value/text()", namespaces=NS)[0]
        y = e.xpath("MMM:field[@name = 'y']/MMM:value/text()", namespaces=NS)[0]
        w = e.xpath("MMM:field[@name = 'width']/MMM:value/text()", namespaces=NS)[0]
        h = e.xpath("MMM:field[@name = 'height']/MMM:value/text()", namespaces=NS)[0]
        scanname = e.xpath(
            "MMM:field[@name = 'scanname']/MMM:value/text()", namespaces=NS
        )[0]
    except IndexError:
        return {}

    return {
        "name": str(name),
        "x": int(x),
        "y": int(y),
        "w": int(w),
        "h": int(h),
        "scanname": str(scanname),
    }


def get_deed_uri(person_uuids: list) -> str:

    for person_uuid in person_uuids:
        deed_uri = person_uuid2deed_uri.get(person_uuid)

        if deed_uri:
            return deed_uri


def get_scan_coordinates(e: lxml.etree.Element) -> dict:

    scan_coordinates = e.xpath(
        "MMM:field[@name = 'scan_coordinates']/MMM:value/text()", namespaces=NS
    )[0]

    scan_coordinates_data = json.loads(scan_coordinates)

    begin_data = (
        [scan_coordinates_data[0]["x"], scan_coordinates_data[0]["y"]],
        scan_coordinates_data[0]["filename"],
    )
    end_data = (
        [scan_coordinates_data[1]["x"], scan_coordinates_data[1]["y"]],
        scan_coordinates_data[1]["filename"],
    )

    return begin_data, end_data


if __name__ == "__main__":

    arguments = docopt(__doc__)

    INPUTFOLDER = arguments["<inputfolder>"]
    OUTPUTFOLDER = arguments["<outputfolder>"]

    parse_files(INPUTFOLDER, OUTPUTFOLDER)
