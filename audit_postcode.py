# -*- coding: utf-8 -*-
""" 
Audit zip codes in the osm file, check wether a zip code contains non-digit 
charachters, wrong format (not 5 digit), or non Dallas zipcode (Dallas zipcodes
starts with 75 or 76). 
Display the result and the time it takes to audit the file.
"""
import pprint
from collections import defaultdict
import time
import osm_variables as osmv
import osm_functions as osmf

problematic_zipcodes = defaultdict(set)
        
def audit_zipcode(z):
    """
    Check wether a zip code contains non-digit charachters, wrong format 
    (not 5 digit), or non Dallas zip code (Dallas zip codes starts with 75 or 76).
    Args:
        z: zip code value
    """
    # Check for non-digit value
    if not all(x.isdigit() for x in z):
        problematic_zipcodes['non-digit'].add(z) 
    # Check for non 5-digit value
    if len(z) != 5:
        problematic_zipcodes['non 5-digit'].add(z)
    # Check for non 75 or 76
    if not z.startswith('75') and not z.startswith('76'):
        problematic_zipcodes['non Dallas'].add(z)


def display_audit_zipcodes_result():
    """
    Display the results of auditing zip codes in the osm file.
    """
    print "Problematic zip codes:"
    pprint.pprint(dict(problematic_zipcodes)) 


def audit():
    """ 
    Audit zip codes in the osm file, display the result and the time it takes
    to audit the file
    """
    print "Auditing zip codes in " + osmv.OSM_PATH
    start = time.time()
    for elem in osmf.get_element(osmv.OSM_PATH):
        for tag in elem.iter("tag"):
            if osmf.is_zipcode(tag):
                zipcode = tag.attrib['v']
                audit_zipcode(zipcode)
    end = time.time()
    display_audit_zipcodes_result()
    print "Time elapsed: " + str(end - start) + " seconds"


if __name__ == "__main__":
    audit()