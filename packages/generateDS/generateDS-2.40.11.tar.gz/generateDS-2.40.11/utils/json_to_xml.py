#!/usr/bin/env python

"""
synopsis:
  convert (cannonical) JSON to XML

usage:
  xml_to_json.py [-h] [-m] [-v] infile

positional arguments:
  infile         JSON input file name/path

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Print messages during actions.

examples:
  python json_to_xml.py data01.json

notes:
  For external use/call, see function `convert`.
"""


import sys
import argparse
from lxml import etree
import json


def json_to_xml(parent, json_node, opts):
    tag = json_node.get('tag')
    attrib = json_node.get('attrib')
    text = json_node.get('text')
    if parent is None:
        element = etree.Element(tag, attrib=attrib)
    else:
        element = etree.SubElement(parent, tag, attrib=attrib)
    element.text = text
    json_children = json_node.get('children')
    if json_children:
        for json_child in json_children:
            json_to_xml(element, json_child, opts)
    return element


#def convert_json_to_xml(opts):
#    with open(opts.infile, 'r') as infile:
#        json_obj = json.load(infile)
#    xml_root = json_to_xml(None, json_obj, opts)
#    xml_string = etree.tostring(
#        xml_root,
#        pretty_print=True,
#        xml_declaration=True,
#        encoding='utf-8',
#    )
#    print(xml_string.decode())
#    return xml_root


def convert_json_to_xml(opts):
    with open(opts.infile, 'r') as infile:
        json_obj = json.load(infile)
    xml_root = json_to_xml(None, json_obj, opts)
    xml_doc = etree.ElementTree(xml_root)
    # use sys.stdout.buffer in order to handle bytes not str.
    xml_doc.write(
        sys.stdout.buffer,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8',
    )
    return xml_root


#
# Function for external use.
def convert(infile):
    opts = argparse.Namespace(
        infile=infile,
    )
    convert_json_to_xml(opts)


def main():
    description = """\
synopsis:
  convert (cannonical) JSON to XML
"""
    epilog = """\

examples:
  python json_to_xml.py data01.json

notes:
  For external use/call, see function `convert`.
"""
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "infile",
        help="JSON input file name/path"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print messages during actions.",
    )
    opts = parser.parse_args()
    convert_json_to_xml(opts)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    #import ipdb; ipdb.set_trace()
    main()
