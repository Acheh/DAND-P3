# -*- coding: utf-8 -*-
""" 
Clean street names in the osm file from problematic charachters, abbreviated 
points, street type, and highway name. Audit cleaned street names and display 
the result and the time it takes to clean and audit the file.
"""
import time
import osm_variables as osmv
import osm_functions as osmf
import audit_street_name as audit

# ================================================== #
#               Cleaning Functions                   #
# ================================================== #
def get_expected_value(v, expv=None, mapv=None):
    """
    Get an expected value from an input value.
    Args:
        v: input value
        expv: list of expected values
        maps: mapping relations in dict
    Returns:
        an expected value or None
    """
    v = v.strip(".").title()
    if expv != None and v in expv:
        return v
    v = v.lower()
    if mapv != None and v in mapv:
        return mapv[v] 
    return None

def get_street_number(s):
    """
    Get cleaned street number from a street name. (e.g. 7604 Dallas Street returns
    street name Dallas Street and street number 7604)
    Args:
        s: street name
    Returns:
        s: street name without street number
        sn: street number
    """
    sn = None
    p = osmv.street_number_re.search(s)
    if p:
        sn = (p.group()).strip(" ")
        # Remove street number from street name
        s = s.replace(sn, "").strip(" ")
    return s, sn

def get_building_number(s):
    """
    Get cleaned building number from a street name. (e.g. Dallas Street Suite 201
    returns street name Dallas Street and building number Suite 201)
    Args:
        s: street name
    Returns:
        s: street name without street number
        bn: building number
    """
    bn = None
    p = osmv.building_no_phrase_re.search(s)
    if p:
        bn = p.group().strip(" ")
        # Remove building number from street name
        s = s[:s.index(bn)].strip(" ")
        # Clean building number
        bn = bn.replace(".", "")
        bn = bn.replace("Ste", "Suite")
        bn = bn.replace("# ", "#")
        bn = bn.replace("#", "No.")
    return s, bn

def get_start_point(s):
    """
    Get cleaned cardinal/ordinal (South, West, North, East, etc.) point at 
    the beginning of a street name. (e.g. South Dallas Street returns street
    name Dallas Street and point South)
    Args:
        s: street name
    Returns:
        s: street name without a point at the beginning of it
        sp: street point
    """
    sp = None
    p = osmv.starting_word_re.search(s)
    if p:
        word = p.group()
        # Get the expected value of the point
        sp = get_expected_value(word,
                                osmv.EXPECTED_POINTS,
                                osmv.POINT_MAPPING)
        if sp:
            # Remove point from street name
            s = s.replace(word, "", 1).strip(" ")
    return s, sp

def get_end_point(s):
    """
    Get cleaned cardinal/ordinal (South, West, North, East, etc.) point at 
    the end of a street name. (e.g. Dallas Street North returns street
    name Dallas Street and point North)
    Args:
        s: street name
    Returns:
        s: street name without a point at the end of it
        sp: street point
    """
    sp = None
    p = osmv.ending_word_re.search(s)
    if p:
        word = p.group()
        # Get the expected value of the point, except for point that follows
        # the word "Avenue" so that "Avenue N" won't be mapped to Avenue North
        if "Avenue " + word not in s:
            sp = get_expected_value(word,
                                    osmv.EXPECTED_POINTS,
                                    osmv.POINT_MAPPING)
        if sp:
            # Remove point from street name
            s = s.replace(word, "", 1).strip(" ")
    return s, sp
            
def clean_highway(s):
    """
    Clean highway name.
    Args:
        s: street name
    Returns:
        s: street name
    """
    p = osmv.highway_re.search(s)
    if p:
        hwy_no = p.group().strip(" ")
        ###############################################
        #         Handle Special Cases                #
        ###############################################
        # Clean highway number from "-" such as in I-20
        hwy_no = hwy_no.replace("-", "")
        # Clean highway number 35 E
        if hwy_no == "35" and "35 E" in s:
            s = s.replace("35 E", "35 East")
        # Clean highway number 35E
        if hwy_no == "35E":
            hwy_no = "35"
            s = s.replace("35E", "35 East")
        ###############################################
        #         Handle General Cases                #
        ###############################################                            
        # Get the expected highway name
        hwy_name = get_expected_value(hwy_no,
                                      None,
                                      osmv.HIGHWAY_MAPPING)
        if hwy_name:
            # Handle business highway
            hwy_bus= ""
            if "Business" in s[:s.index(hwy_no)]:
                hwy_bus = " Business"
            # Remove highway name from street name and move 
            # business name to the end of it
            s = s[s.index(hwy_no):] + hwy_bus
            # Return street name with cleaned highway name
            return hwy_name + " " + s
    return s
        
def clean_type(s):
    """
    Clean street type.
    Args:
        s: street name
    Returns:
        s: street name
    """
    p = osmv.ending_word_re.search(s)
    if p:
        word = p.group()
        ###############################################
        #         Handle Special Cases                #
        ###############################################
        # Handle: Webb Chapel Rd 200
        if word == "200":
            word = "Rd"
            s = s.replace("200", "No.200")
        # Handle: Ave K.
        if word == "K.":
            s = s.replace(".", "")
            word = "Ave"
        # Handle: Hwy78
        if word == "Hwy78":
            s = osmv.TX_road + " 78"
        ###############################################
        #         Handle General Cases                #
        ###############################################
        # Get the expected street type
        st = get_expected_value(word,
                                osmv.EXPECTED_STREET_TYPES,
                                osmv.TYPE_MAPPING)
        if st:
            # Return street name with cleaned street type
            return s.replace(word, st)
    return s

def clean_ordinal(s):
    """
    Clean ordinal number in street name to consistently use st, nd, rd, or th
    without any capital letter. (e.g. 1St should be 1st and 14TH should be 14th)
    Args:
        s: street name
    Returns:
        s: street name
    """
    p = osmv.ordinal_number_re.search(s)
    if p:
        n = p.group()
        return s.replace(n, n.lower())
    return s

def clean_problematic_chars(name):
    """
    Capitalize leading letter in each word, remove comma, remove semicolon and 
    all charatecters that follow, and clean ordinal number.
    Args:
        s: street name
    Returns:
        s: street name
    """
    # Capitalize leading letter, clean "'s" and ordinal number
    name = name.title()
    name = name.replace("'S ", "'s ")
    name = clean_ordinal(name)
    # Remove comma
    name = name.replace(",", "")
    # Remove semicolon and all characthers that follow
    if ";" in name:
        name = name[:name.index(";")]
    return name

# ================================================== #
#               Main Function                        #
# ================================================== #
def clean_street_name(name):
    """
    Clean street name from problematic characters, building number, abbreviated
    points, unexpected street type and highway name and number. 
    Args:
        name: street name
    Return:
        name: cleaned street name
    """
    name = clean_problematic_chars(name)
    # Strip of and clean building number, street number, start point, and
    # end point from street name
    name, building_no = get_building_number(name)
    name, street_no = get_street_number(name)
    name, start_pt = get_start_point(name)
    name, end_pt = get_end_point(name)
    # Clean highway name and street type in street name    
    name = clean_highway(name)
    name = clean_type(name)    
    # Put street name back together
    if end_pt:
        name = name + " " + end_pt
    if start_pt:
        name = start_pt + " " + name
    if street_no:
        name = street_no + " " + name
    if building_no:
        name = name + " " + building_no    
    return name

def cleaning():
    """
    Clean street names in the osm file then audit cleaned street names, display 
    the result and the time it takes to clean and to audit the file
    """
    print "Cleaning and auditing street names in " + osmv.OSM_PATH
    start = time.time()
    for elem in osmf.get_element(osmv.OSM_PATH):
        for tag in elem.iter("tag"):
            if osmf.is_street_name(tag):
                name = tag.attrib['v']   
                name = clean_street_name(name)
                audit.audit_street_name(name)           
    end = time.time()
    audit.display_audit_street_name_result()
    print "Time elapsed: " + str(end - start) + " seconds"
    

if __name__ == "__main__":
    cleaning()
