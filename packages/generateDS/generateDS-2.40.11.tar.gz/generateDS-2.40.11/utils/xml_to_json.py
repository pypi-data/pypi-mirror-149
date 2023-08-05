#!/usr/bin/env python

"""
synopsis:
  convert XML to (cannonical) JSON

usage:
  xml_to_json.py [-h] [-m] [-v] infile

positional arguments:
  infile         XML input file name/path

optional arguments:
  -h, --help     show this help message and exit
  -m, --map      convert to map/dict. default is list.
  -v, --verbose  Print messages during actions.

examples:
  python xml_to_json.py data01.xml
  python xml_to_json.py --map data01.xml

notes:
  For external use/call, see function `convert`.
"""


# import sys
import argparse
from lxml import etree
import json


def xml_to_json(node, opts):
    # convert attributes
    tag = node.tag
    attrs = dict(node.attrib)
    children = [xml_to_json(child, opts) for child in node.getchildren()]
    text = ""
    if node.text:
        text = node.text
    json_obj = [tag, attrs, children, text]
    return json_obj


def xml_to_json_map(node, opts):
    # convert attributes
    tag = node.tag
    attrib = dict(node.attrib)
    children = [xml_to_json_map(child, opts) for child in node.getchildren()]
    text = ""
    if node.text:
        text = node.text
    json_obj = {
        'tag': tag,
        'attrib': attrib,
        'text': text,
    }
    if children:
        json_obj['children'] = children
    return json_obj


def convert_xml_to_json(opts):
    doc = etree.parse(opts.infile)
    root = doc.getroot()
    if opts.map:
        json_obj = xml_to_json_map(root, opts)
    else:
        json_obj = xml_to_json(root, opts)
    json_string = json.dumps(json_obj, indent=2)
    print(json_string)


#
# Function for external use.
def convert(infile, map=False):
    opts = argparse.Namespace(
        infile=infile,
        map=map,
    )
    convert_xml_to_json(opts)


def main():
    description = """\
synopsis:
  convert XML to JSON
"""
    epilog = """\

examples:
  python xml_to_json.py data01.xml
  python xml_to_json.py --map data01.xml

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
        help="XML input file name/path"
    )
    parser.add_argument(
        "-m", "--map",
        action="store_true",
        help="convert to map/dict.  default is list.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print messages during actions.",
    )
    opts = parser.parse_args()
    convert_xml_to_json(opts)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    #import ipdb; ipdb.set_trace()
    main()
