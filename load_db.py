# -*- coding: utf-8 -*-
"""
Build a database system from .csv files that were created from the osm files 
and were shaped to follow the schema.py data structures.
"""

import csv
import sqlite3 as sq3
import osm_variables as osmv

create_nodes_query = """
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);
"""

create_nodes_tags_query = """
CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);
"""

create_relations_query = """
CREATE TABLE relations (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);
"""

create_relations_nodes_query = """
CREATE TABLE relations_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    role TEXT,
    FOREIGN KEY (id) REFERENCES relations(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);
"""

create_relations_relations_query = """
CREATE TABLE relations_relations (
    id INTEGER NOT NULL,
    relation_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    role TEXT,
    FOREIGN KEY (id) REFERENCES relations(id),
    FOREIGN KEY (relation_id) REFERENCES relations(id)
);
"""

create_relations_tags_query = """
CREATE TABLE relations_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);
"""

create_relations_ways_query = """
CREATE TABLE relations_ways (
    id INTEGER NOT NULL,
    way_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    role TEXT,
    FOREIGN KEY (id) REFERENCES relations(id),
    FOREIGN KEY (way_id) REFERENCES ways(id)
);
"""

create_ways_query = """
CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);
"""

create_ways_nodes_query = """
CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);
"""

create_ways_tags_query = """
CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);
"""

insert_nodes_query = """
INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp)
VALUES (:id, :lat, :lon, :user, :uid, :version, :changeset, :timestamp)
"""
insert_nodes_tags_query = """
INSERT INTO nodes_tags (id, key, value, type)
VALUES (:id, :key, :value, :type)
"""
insert_relations_query = """
INSERT INTO relations (id, user, uid, version, changeset, timestamp)
VALUES (:id, :user, :uid, :version, :changeset, :timestamp)
"""
insert_relations_nodes_query = """
INSERT INTO relations_nodes (id, node_id, position, role)
VALUES (:id, :node_id, :position, :role)
"""
insert_relations_relations_query = """
INSERT INTO relations_relations (id, relation_id, position, role)
VALUES (:id, :relation_id, :position, :role)
"""
insert_relations_tags_query = """
INSERT INTO relations_tags (id, key, value, type)
VALUES (:id, :key, :value, :type)
"""
insert_relations_ways_query = """
INSERT INTO relations_ways (id, way_id, position, role)
VALUES (:id, :way_id, :position, :role)
"""
insert_ways_query = """
INSERT INTO ways (id, user, uid, version, changeset, timestamp)
VALUES (:id, :user, :uid, :version, :changeset, :timestamp)
"""
insert_ways_nodes_query = """
INSERT INTO ways_nodes (id, node_id, position)
VALUES (:id, :node_id, :position)
"""
insert_ways_tags_query = """
INSERT INTO ways_tags (id, key, value, type)
VALUES (:id, :key, :value, :type)
"""

def create_tables():
    """
    Create database tables for each csv file
    """
    with sq3.connect(osmv.DB_PATH) as con:
        cur = con.cursor()
        cur.execute(create_nodes_query)
        cur.execute(create_nodes_tags_query)
        cur.execute(create_relations_query)
        cur.execute(create_relations_nodes_query)
        cur.execute(create_relations_relations_query)
        cur.execute(create_relations_tags_query)
        cur.execute(create_relations_ways_query)
        cur.execute(create_ways_query)
        cur.execute(create_ways_nodes_query)
        cur.execute(create_ways_tags_query)
        con.commit()

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}

def import_csv(csv_file, query):
    """
    Import the .csv file into the corresponding database table
    """        
    with open (csv_file, 'rb') as csvfile:
        csv_reader = UnicodeDictReader(csvfile)
        with sq3.connect(osmv.DB_PATH) as conn:
            cur = conn.cursor()
            cur.executemany(query, csv_reader)
        
if __name__ == '__main__':
    create_tables()
    print "Tables Created"
    import_csv(osmv.NODES_PATH, insert_nodes_query)
    print "Done inserting nodes"
    import_csv(osmv.NODE_TAGS_PATH, insert_nodes_tags_query)
    print "Done insterting nodes_tags"
    import_csv(osmv.RELATIONS_PATH, insert_relations_query)
    print "Done insterting relations"
    import_csv(osmv.RELATION_NODES_PATH, insert_relations_nodes_query)
    print "Done insterting relations_nodes"
    import_csv(osmv.RELATION_RELATIONS_PATH, insert_relations_relations_query)
    print "Done insterting relations_relations"
    import_csv(osmv.RELATION_TAGS_PATH, insert_relations_tags_query)
    print "Done insterting relations_tags"
    import_csv(osmv.RELATION_WAYS_PATH, insert_relations_ways_query)
    print "Done insterting relations_ways"
    import_csv(osmv.WAYS_PATH, insert_ways_query)
    print "Done insterting ways"
    import_csv(osmv.WAY_NODES_PATH, insert_ways_nodes_query)
    print "Done insterting way_nodes"
    import_csv(osmv.WAY_TAGS_PATH, insert_ways_tags_query)
    print "Done insterting way_tags"