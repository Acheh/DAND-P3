#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The main function of these codes is to process the osm file. First, it will clean
the data (street names, city names, zipcodes, and tag's key) and shape each element
into several data structures base on the schema in schema.py. Then, it will write
each data structure to the appropriate .csv files.
"""

import csv
import codecs
import pprint
import cerberus
import schema
import clean_postcode as postcode
import clean_street_name as street
import clean_city_name as city
import time
import osm_functions as osmf
import osm_variables as osmv
import os

SCHEMA = schema.schema

def shape_element(element, 
                  node_attr_fields=osmv.NODE_FIELDS, 
                  relation_attr_fields=osmv.RELATION_FIELDS,
                  way_attr_fields=osmv.WAY_FIELDS,
                  problem_chars=osmv.PROBLEMCHARS, 
                  default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    node_attribs = {}
    relation_attribs = {}
    relation_nodes = []
    relation_relations = []
    relation_ways = []
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way fornode, relation and way elements

    for att in element.attrib:
        if element.tag == 'node' and att in node_attr_fields:
            node_attribs[att] = element.attrib[att]
        elif element.tag == 'relation' and att in relation_attr_fields:
            relation_attribs[att] = element.attrib[att]
        elif element.tag == 'way' and att in way_attr_fields:
            way_attribs[att] = element.attrib[att]

    node_index = 0
    relation_nodes_index = 0
    relation_relations_index = 0
    relation_ways_index = 0
    for el in element:
        if el.tag == 'tag' and not problem_chars.search(el.attrib['k']):
            tag = {}
            tag['id'] = element.attrib['id']
            value = el.attrib['v']
            # Clean street name
            if osmf.is_street_name(el):
                value = street.clean_street_name(value)
            # Clean zipcodes
            if osmf.is_zipcode(el):
                value = postcode.clean_zipcode(value)
            # Clean city names:
            if osmf.is_city_name(el):
                value = city.clean_city_name(value)
            if value:
                tag['value'] = value 
                if ":" in el.attrib['k']:
                    ind = el.attrib['k'].index(":")
                    tag['type'] = str(el.attrib['k'])[:ind]
                    tag['key'] = str(el.attrib['k'])[ind+1:]
                else:
                    tag['key'] = el.attrib['k']
                    tag['type'] = default_tag_type
                tags.append(tag)
        
        if element.tag == 'way' and el.tag == 'nd':
            way_node = {}
            way_node['id'] = element.attrib['id']
            way_node['node_id'] = el.attrib['ref']
            way_node['position'] = node_index
            node_index = node_index + 1
            way_nodes.append(way_node)
            
        if element.tag == 'relation' and el.tag == 'member':
            relation_member = {}
            relation_member['id'] = element.attrib['id']
            relation_member['role'] = el.attrib['role']
            if el.attrib['type'] == 'node':
                relation_member['node_id'] = el.attrib['ref']    
                relation_member['position'] = relation_nodes_index
                relation_nodes_index += 1
                relation_nodes.append(relation_member)
            elif el.attrib['type'] == 'relation':
                relation_member['relation_id'] = el.attrib['ref']
                relation_member['position'] = relation_relations_index
                relation_relations_index += 1
                relation_relations.append(relation_member)
            elif el.attrib['type'] == 'way':
                relation_member['way_id'] = el.attrib['ref']
                relation_member['position'] = relation_ways_index
                relation_ways_index += 1
                relation_ways.append(relation_member)

    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'relation':
        return {'relation': relation_attribs, 
                'relation_nodes': relation_nodes,
                'relation_relations': relation_relations,
                'relation_tags': tags,
                'relation_ways': relation_ways}
    elif element.tag == 'way':
        return {'way': way_attribs, 
                'way_nodes': way_nodes, 
                'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))
        
class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(osmv.NODES_PATH, 'w') as nodes_file, \
         codecs.open(osmv.NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(osmv.RELATIONS_PATH, 'w') as relations_file, \
         codecs.open(osmv.RELATION_NODES_PATH, 'w') as relation_nodes_file, \
         codecs.open(osmv.RELATION_RELATIONS_PATH, 'w') as relation_relations_file, \
         codecs.open(osmv.RELATION_TAGS_PATH, 'w') as relation_tags_file, \
         codecs.open(osmv.RELATION_WAYS_PATH, 'w') as relation_ways_file, \
         codecs.open(osmv.WAYS_PATH, 'w') as ways_file, \
         codecs.open(osmv.WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(osmv.WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, osmv.NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, osmv.NODE_TAGS_FIELDS)
        relations_writer = UnicodeDictWriter(relations_file, osmv.RELATION_FIELDS)
        relation_nodes_writer = UnicodeDictWriter(relation_nodes_file, osmv.RELATION_NODES_FIELDS)
        relation_relations_writer = UnicodeDictWriter(relation_relations_file, osmv.RELATION_RELATIONS_FIELDS)
        relation_tags_writer = UnicodeDictWriter(relation_tags_file, osmv.RELATION_TAGS_FIELDS)
        relation_ways_writer = UnicodeDictWriter(relation_ways_file, osmv.RELATION_WAYS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, osmv.WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, osmv.WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, osmv.WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        relations_writer.writeheader()
        relation_nodes_writer.writeheader()
        relation_relations_writer.writeheader()
        relation_tags_writer.writeheader()
        relation_ways_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()
        
        for element in osmf.get_element(file_in, tags=('node', 'relation', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'relation':
                    relations_writer.writerow(el['relation'])
                    relation_nodes_writer.writerows(el['relation_nodes'])
                    relation_relations_writer.writerows(el['relation_relations'])
                    relation_tags_writer.writerows(el['relation_tags'])
                    relation_ways_writer.writerows(el['relation_ways'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

def display_osm_file_information():
    print 'OSM file: {}'.format(osmv.OSM_PATH)
    print 'OSM file size: {} KB'.format(osmf.get_file_size(osmv.OSM_PATH))
    print "Map boundaries:"
    print osmf.get_map_bounds(osmv.OSM_PATH)
    print "Element Counts:"
    print osmf.get_element_count(osmv.OSM_PATH)

def display_csv_files_information():
    try:
        print ''
        print '{:<25} {:>10}'.format('File Name', 'Size')
        for f in osmv.csv_files:
            print '{:<25} {:>10} KB'.format(f, osmf.get_file_size(f))
    except os.error:
        print '{:<25} {:>10}'.format(f, 'not found')
                    
if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    display_osm_file_information()
    print ''
    print "Processing..."
    start = time.time()
    process_map(osmv.OSM_PATH, validate=True)
    end = time.time()
    print "Time elapsed: " + str(end - start) + " seconds"
    print ''
    display_csv_files_information()
