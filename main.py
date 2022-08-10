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

import os
import sys
import json

import pandas as pd

import lxml
import lxml.etree as ET

from docopt import docopt

NS = {"MMM": "https://maior.memorix.nl/XSI/3.0/"}

with open("mapping/person_uuid2deed_uri.json") as infile:
    person_uuid2deed_uri = json.load(infile)


def parse_files(folder_path: str, output="CSV"):

    # Parse every file in the folder
    for fn in sorted(os.listdir(folder_path)):
        print(f"Parsing {fn}...")
        fpath = os.path.join(folder_path, fn)

        tree = ET.parse(fpath)
        get_records(tree)


def get_records(tree):
    # Find all the records (=deeds) that have a location element
    records = tree.findall(
        "MMM:export/MMM:record",
        namespaces=NS,
    )

    data = []

    for r in records:

        # Get scan coordinates (begin/end)
        scan_coordinates = get_scan_coordinates(r)

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

        # Now the locations
        for n, e in enumerate(location_elements, 1):

            if deed_uri:
                location_uri = deed_uri + f"?location=Location{n}"
            else:
                location_uri = ""
            coordinate_data = get_coordinates(e)

        r_data = {}

        data.append(r_data)

    # And then save it somewhere
    # if output == "CSV":
    #     pass
    # elif output == "RDF":

    #     location = Resource(g, location_uri)
    #     location.add(RDF.type, ROAR.Location)

    #     annotation = Resource(g, Bnode())
    #     annotation.add(RDF.type, OA.Annotation)
    #     annotation.add(OA.hasBody, location.identifier)

    #     pass


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

    return {"name": name, "x": x, "y": y, "w": w, "h": h, "scan": scanname}


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

    return {
        "begin": {
            "geometry": {"type": "Point", "coordinates": scan_coordinates_data[0]}
        },
        "end": {"geometry": {"type": "Point", "coordinates": scan_coordinates_data[1]}},
    }


if __name__ == "__main__":

    arguments = docopt(__doc__)

    INPUTFOLDER = arguments["<inputfolder>"]
    OUTPUTFOLDER = arguments["<outputfolder>"]

    parse_files(INPUTFOLDER, OUTPUTFOLDER)
