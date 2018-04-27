# DAND-P3
OpenStreetMap Dallas Texas Metro Area Data Case Study

Using data munging techniques such as assessing data quality for validity, completeness, consistency and uniformity to clean the OSM data of Dallas Texas area.

Files in this project:
1. **readme.txt**
2. **osm_variables.py**
This file consists of file paths, regular expressions, mapping rules, and expected values used in th Open Street Data Wrangling project
3. **osm_functions.py**
This file contains helper functions to process the OSM files.
* get_element
* get_element_count
* get_file_size
* get_map_bounds
* is_street_name
* is_zipcode
* is_city_name
4. **take_sample.py**
This file was used to extract data sample from the original OSM file.
5. **dallas_sample.osm**
This file is data sample from the Dallas-Texas OSM file.
6. **schema.py**
This file cotaints a database schema used to validate csv files. Please not that this is a modified version of schema.py provided in Preparing for Database - SQL lesson. It is modified to accomodate relation elements that were not included in the original schema.py.
7. **audit_city_name.py**
This file audit city names in osm file, check wether a city name includes problematic characters, or state name (TX or Texas). It displays the audit results and the time it takes to audit the file.
8. **audit_postcode.py**
This file audit zip codes in the osm file, check wether a zip code contains non-digit charachters, wrong format (not 5 digit), or non Dallas zip code (Dallas zip codes starts with 75 or 76). It displays the audit result and the time it takes to audit the file.
9. **audit_street_name.py**
This file audit street names in the osm file, check wether a street name contains problematic charachters, abbreviated points, abbreviated street types, or abbreviated highway names. Display the audit result and the time it takes to audit the file.
10. **clean_city_name.py**
This file clean city names in the osm file. It cleans city names that contain non-alphabet charachters, state name, and problematic name. Then, it audits cleaned city names, and displays the result and the time it takes to clean and audit the file.
11. **clean_postcode.py**
This file clean zip codes in the osm file. It cleans zip codes that contain non-digit charachters, wrong number of digit, or zip code from area outside Dallas. Then, it audits cleaned zip codes, and displays the result and the time it takes to clean and audit the file.
12. **clean_street_name.py**
This file cleans street names in the osm file from problematic charachters, abbreviated points, abbreviated street types, and abbreviated highway names. Then, it audits cleaned street names and displays the result and the time it takes to clean and audit the file.
13. **write_csvs.py**
The main purpose of these codes is to process the osm file. First, it will clean the data (street names, city names, zipcodes, and tag's key) and shape each element into several data structures base on the schema in schema.py. Then, it will write each data structure to the appropriate csv files.
14. **load_db.py**
Build a database system from csv files that were created from the osm files and were shaped to follow the schema.py data structures.
15. report.pdf
This file contains a final report of the project, including map area, problem encountered in the map, data overview, additional data exploration, additional ideas, conclusion, and references.
16. **output.txt**
This file contains the output from running audits, cleanings, write_csvs, and load_db files.

### Before running the codes:
* The OSM file path is currently set to 'dallas_sample.osm'. If you need to run these codes on different osm file, please change the OSM_PATH variable in osm_variables.py.
* Due to the small number of Dallas OSM data that need cleaning, the 'dallas_sample.osm' does not capture most of the problems encountered in the full OSM file. 
