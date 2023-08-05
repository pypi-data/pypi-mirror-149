#!/bin/bash -x

./generateDS.py -f -o collect_children_lib.py --member-specs=dict collect_children.xsd
./collect_children.py
