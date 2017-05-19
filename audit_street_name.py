# -*- coding: utf-8 -*-
""" 
Audit street names in the osm file, check wether a street name contains problematic 
charachters, abbreviated points, street type, or highway name. Display the result 
and the time it takes to audit the file.
"""

import pprint
from collections import defaultdict
import time
import osm_variables as osmv
import osm_functions as osmf

problematic_chars = defaultdict(set)
problematic_building_numbers = defaultdict(set)
problematic_points = defaultdict(set)
problematic_street_types = defaultdict(set)
problematic_highways = defaultdict(set)

def audit_char(s):
    """
    Check wether street name has the following problemetic characters: "'S", ",",
    ";", or ordinal number with capital letter. If it does, add street name into
    problematic_chars set.
    Args:
        s: street name
    """
    # problematic "'S"
    if "'S" in s:
        problematic_chars["'S"].add(s)
    # comma in street name
    if "," in s:
        problematic_chars[","].add(s)
    # semicollon in street name
    if ";" in s:
        problematic_chars[";"].add(s)
    # ordinal number with capital letter such as in 5Th
    p = osmv.ordinal_number_re.search(s)
    if p:
        ordinal = p.group().strip(" ")
        if any(x.isupper() for x in ordinal):
            problematic_chars[ordinal].add(s)


def audit_building_number_type(s):
    """
    Check wether street name has building (suite) number. If it does add street 
    name into problematic_building_numbers set.
    Args:
        s: street name
    """
    p = osmv.building_no_type_re.search(s)
    if p:
        bn = p.group().strip(" ").strip(".")
        if bn not in osmv.EXPECTED_BUILDING_NUMBER_TYPES:
            problematic_building_numbers[bn].add(s)

def audit_point(s):
    """
    Check wether street name has an abbreviated point (e.g S, E, N, W). 
    If it does add street name into problematic_points set.
    Args:
        s: street name
    """
    p = osmv.audit_point.search(s)
    if p:
        point = p.group().strip(" ")
        problematic_points[point].add(s)            

def audit_stret_type(s):
    """
    Check wether street name has an expected type (e.g Street, Road, Lane). 
    If it does not, add street name into problematic_street_types set.
    Args:
        s: street name
    """
    if not any(p in s for p in osmv.EXPECTED_STREET_TYPES):
        street_type = s
        if " " in s:
            street_type = street_type[street_type.rindex(" "):]
        problematic_street_types[street_type].add(s)


def audit_highway(s):
    """
    Check wether street name has a number that could be a highway number 
    (e.g. FM 121, Interstate 30). If the number is not highway number or 
    the highway name is not consistent with the mapping, add street name into 
    problematic_highways set.
    Args:
        s: street name
    """
    p = osmv.highway_re.search(s)
    if p:
        hwy = p.group().strip(" ").strip(".")
        if hwy not in osmv.HIGHWAY_MAPPING \
        or osmv.HIGHWAY_MAPPING[hwy] not in s:
            if "Suite" not in s:
                problematic_highways[hwy].add(s)

def audit_street_name(s):
    """
    Audit street name for problematic characters, building number, abbreviated
    points, street type, and highway name and number. 
    """
    audit_char(s)
    audit_building_number_type(s)
    audit_point(s)
    audit_stret_type(s)
    audit_highway(s)
    
def display_audit_street_name_result():
    """
    Display the results of auditing street names in the osm file.
    """
    print "Problematic Characters:"
    pprint.pprint(dict(problematic_chars))
    print "Problematic Building Numbers:"
    pprint.pprint(dict(problematic_building_numbers))    
    print "Problematic Points:"
    pprint.pprint(dict(problematic_points))    
    print "Problematic Street Types:"
    pprint.pprint(dict(problematic_street_types))    
    print "Problematic Highway Name:"
    pprint.pprint(dict(problematic_highways))            
    
def audit():
    """ 
    Audit street names in the osm file, display the results and the time it takes
    to audit the file
    """
    print "Auditing street names in " + osmv.OSM_PATH
    start = time.time()
    for elem in osmf.get_element(osmv.OSM_PATH):
        for tag in elem.iter("tag"):
            if osmf.is_street_name(tag):
                name = tag.attrib['v']
                audit_street_name(name)
    end = time.time()
    display_audit_street_name_result()
    print "Time elapsed: " + str(end - start) + " seconds"

if __name__ == "__main__":
    audit()