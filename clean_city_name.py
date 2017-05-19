# -*- coding: utf-8 -*-
"""
Clean city names in the osm file, clean city names that contain non-alphabet 
charachters, state name, and problematic name. Audit cleaned city names, and 
display the result and the time it takes to clean and 
audit the file.
"""

import time
import audit_city_name as audit
import osm_variables as osmv
import osm_functions as osmf

def clean_city_name(c):
    """
    Clean city names that contain non-alphabet charachters, state name, and 
    problematic name
    Args:
        c: city name
    Return:
        c: cleaned city name or None
    """
    c = c.title()
    # Remove comma and all characters that follows
    if ',' in c:
        c = c[:c.index(',')]
    # Remove period
    if '.' in c:
        c = c.replace('.', '')
    # Remove state name
    c = c.replace('Tx', '')
    c = c.replace('Texas', '')
    # Map problematic name
    for x in osmv.CITY_MAPPING:
        if x in c:
            c = c.replace(x, osmv.CITY_MAPPING[x])
    # Remove name with digit character
    if any(x.isdigit() for x in c):
        return None
    else:
        return c.strip(' ')
    
def clean():
    """
    Clean city names in the osm file then audit cleaned city names, display the 
    result and the time it takes to clean and to audit the file
    """
    print "Cleaning and auditing city names in " + osmv.OSM_PATH
    start = time.time()
    for elem in osmf.get_element(osmv.OSM_PATH):
        for tag in elem.iter("tag"):
            if osmf.is_city_name(tag):
                name = tag.attrib['v']
                name = clean_city_name(name)
                if name:
                    audit.audit_city_name(name)
    end = time.time()
    audit.display_audit_city_name_result()
    print "Time elapsed: " + str(end - start) + " seconds"

if __name__ == "__main__":
    clean()