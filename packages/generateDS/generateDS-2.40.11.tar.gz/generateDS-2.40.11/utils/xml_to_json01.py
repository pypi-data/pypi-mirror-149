#!/usr/bin/env python

"""
synopsis:
    Convert an XML document to JSON.  Write to stdout.
usage:
    xml_to_json.py <input_file>
examples:
    python xml_to_json.py my_xml_file.xml
"""

import sys
from lxml import etree
import json


def convert(path):
    doc = etree.parse(path)
    old_tree = doc.getroot()
    new_tree = convert_tree(old_tree)
    json_tree = json.dumps(new_tree, indent=2)
    return json_tree


def convert_tree(elem):
    node = {
        'tag': etree.QName(elem).localname,
        'text': elem.text,
        'tail': elem.tail,
    }
    attributes = dict(elem.attrib)
    node['attrib'] = attributes
    parent = elem.getparent()
    for nsprefix, ns in elem.nsmap.items():
        if parent is None or nsprefix not in parent.nsmap:
            attributes[f'xmlns:{nsprefix}'] = ns
    children = []
    node['children'] = children
    for child in elem:
        children.append(convert_tree(child))
    return node


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit('usage: python xml_to_json.py input_file.xml')
    infilename = args[0]
    json_tree = convert(infilename)
    print(json_tree)


if __name__ == '__main__':
    main()
