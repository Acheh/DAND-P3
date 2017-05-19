# -*- coding: utf-8 -*-
"""
Clean zip codes in the osm file, clean zip codes that contain non-digit 
charachters, wrong number of digit, or zip code from area outside Dallas. Audit
cleaned zip codes, and display the result and the time it takes to clean and 
audit the file.
"""

import time
import audit_postcode as audit
import osm_variables as osmv
import osm_functions as osmf

def clean_zipcode(z):
    """
    Clean zip code value from non-digit characters, returns None if the value is
    not in the correct format (5 digits) or if it does not start with 75 or 76 
    (Dallas area zip codes start with 75 or 76)
    Args:
        z: zip code value
    Return:
        z: cleaned zip code value or None
    """
    p = osmv.zip_re.search(z)
    if p:
        zipcode = p.group()
        return zipcode
    return None
    
def clean():
    """
    Clean zip codes in the osm file then audit cleaned zip codes, display the 
    result and the time it takes to clean and to audit the file
    """
    print "Cleaning and auditing zip codes in " + osmv.OSM_PATH
    start = time.time()
    for elem in osmf.get_element(osmv.OSM_PATH):
        for tag in elem.iter("tag"):
            if osmf.is_zipcode(tag):
                zipcode = tag.attrib['v']
                zipcode = clean_zipcode(zipcode)
                if zipcode:
                    audit.audit_zipcode(zipcode)
    end = time.time()
    audit.display_audit_zipcodes_result()
    print "Time elapsed: " + str(end - start) + " seconds"

if __name__ == "__main__":
    clean()