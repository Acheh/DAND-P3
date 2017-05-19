#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
import osm_functions as osmf
import osm_variables as osmv

SAMPLE_FILE = "dallas_sample.osm"

k = 150 # Parameter: take every k-th top level element

with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')
    # Write every kth top level element
    for i, element in enumerate(osmf.get_element(osmv.OSM_PATH)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))
    output.write('</osm>')