# -*- coding: utf-8 -*-
"""
This file contains helper functions to process the OSM files. 
"""
import xml.etree.cElementTree as ET
import os

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """
    Yield element if it is the right type of tag
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def get_element_count(osm_file):
    """
    Get the count of node, relation, and way. 
    Args: 
        osm_file
    Returns:
        the count of node, relation, and way in a dictionary 
    """
    elements = {'node': 0, 'relation': 0, 'way': 0}
    for elem in get_element(osm_file):
        if elem.tag == 'node':
            elements['node'] += 1
        elif elem.tag == 'relation':
            elements['relation'] += 1
        else:
            elements['way'] +=1
    return elements

def get_file_size(file):
    """
    Get a file size in KB, rounded to 1 decimal place
    Args:
        file
    Returns:
        file size in KB
    """
    return round(float(os.path.getsize(file))/1000,1)
            
def get_map_bounds(osm_file):
    """
    Get osm map boundaries
    Args:
        osm_file
    Returns:
        minimum and maximum latitude and minimum and maximum longitude in a dictionary
    """
    boundaries = None
    for event, elem in ET.iterparse(osm_file):
        if elem.tag == "bounds":
            boundaries= {'Latitude': [elem.attrib['minlat'], elem.attrib['maxlat']], 
                         'Longitude': [elem.attrib['minlon'], elem.attrib['maxlon']]}            
        break # we're done
    return boundaries

def is_street_name(elem):
    """Check whether an element consist of street address"""
    return (elem.attrib['k'] == "addr:street")

def is_zipcode(elem):
    """Check whether an element consist of a zip code"""
    return (elem.attrib['k'] == "addr:postcode")

def is_city_name(elem):
    """Check whether an element consist of city name"""
    return (elem.attrib['k'] == "addr:city")