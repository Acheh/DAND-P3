# -*- coding: utf-8 -*-
""" 
Audit city names in osm file, check wether a city name includes problematic
characters, or state name (TX or Texas). 
Display the result and the time it takes to audit the file.
"""
import pprint
from collections import defaultdict
import time
import osm_variables as osmv
import osm_functions as osmf

problematic_cities = defaultdict(set)
        
def audit_city_name(c):
    """
    Check wether a city name consists of problematic characters, or state 
    name (TX or Texas).
    Args:
        z: zipcode value
    """
    # check for city name that includes state name
    if any(x in c.lower() for x in ['tx', 'texas']):
        problematic_cities['include state'].add(c)
    # check for city name that include non alphabet character
    elif not all(x.isalpha() for x in c.lower().replace(' ','')):
        problematic_cities['non-alphabet'].add(c)
    # check for city with abbreviated name
    for x in osmv.CITY_MAPPING.keys():
        if x.lower() in c.lower() and osmv.CITY_MAPPING[x] not in c:
            problematic_cities['problematic names'].add(c)

def display_audit_city_name_result():
    """
    Display the results of auditing city names in the osm file.
    """
    print "Problematic City Names:"
    pprint.pprint(dict(problematic_cities))      
    

def audit():
    """ 
    Audit city names in the osm file, display the result and the time it takes
    to audit the file
    """
    print "Auditing City Names in " + osmv.OSM_PATH
    start = time.time()
    for elem in osmf.get_element(osmv.OSM_PATH):
        for tag in elem.iter("tag"):
            if osmf.is_city_name(tag):
                name = tag.attrib['v']
                audit_city_name(name)
    end = time.time()
    display_audit_city_name_result()
    print "Time elapsed: " + str(end - start) + " seconds"


if __name__ == "__main__":
    audit()