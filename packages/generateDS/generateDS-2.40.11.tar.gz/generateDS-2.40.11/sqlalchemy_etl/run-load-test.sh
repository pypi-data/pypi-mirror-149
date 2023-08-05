#!/bin/bash -x
rm -i $1
./test03.py create $1
./test03.py -d people.xml add $1
