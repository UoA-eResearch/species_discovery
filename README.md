# species_discovery
Python scripts to geocode and parse xls data into json, and html/js to plot it on a map

#Running a local geocoder

Run the following commands:

    wget http://twofishes.net/binaries/server-assembly-0.84.9.jar
    wget http://twofishes.net/indexes/revgeo/2015-03-05.zip
    unzip 2015-03-05.zip
    java -jar server-assembly-0.81.9.jar --hfile_basepath 2015-03-05-20-05-30.753698

This creates a server listening on port 8080 and 8081. JSON requests can be made to 8081, e.g. http://localhost:8081/?query=nyc

#Dependencies
Run `pip install xlrd xlwt xlutils requests` to install dependencies

#Geocoding
Run `python geocode.py dataset.xls` to read the Locality field from the xls, geocode it and write the latlong back to a copy of the xls file.

#Packing

Run `python parse.py dataset.xls_geocoded.xls` to parse relevant fields out of the xls file and write a json file. This script trims out unnecessary data to minimise the file size of the resulting json file. Move the json file into the map folder to serve it.
