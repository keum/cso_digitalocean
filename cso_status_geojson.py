#!/usr/bin/python
"""
Creates a GeoJSON file of the current CSO status for King County and Seattle.
Reads the CSO status from King County's web server and combines it with
a CSV file of the point coordinates.

The resulting GeoJSON file can be added to a webmap.
"""
import urllib2
import csv
import geojson
from subprocess import call

# ===================
# RETRIEVE CSO STATUS
# ===================
# Download csv status values from the King County website.
f_cso_status = urllib2.urlopen("http://your.kingcounty.gov/dnrp/library/wastewater/cso/img/CSO.CSV")

# File has a header line that looks like this, so extract the time string:
# CSO_TagName,04-01-2016 09:30:01 AM
# We want to use this rather than the system time when the script/cronjob runs
# because it is the actual time the data were queried.
status_timestamp = f_cso_status.readline().strip().split(',')[1]

# Read rest of csv file into a python list named cso_status_csv
cso_status_csv = f_cso_status.readlines()  #read each line of downloaded csv file
cso_status = {} # initialize empty dictionary for CSO status_timestamp
for line in cso_status_csv:
    # King County CSO sites have names like WMIC.CSOSTATUS_N
    #    for these, only take the CSO_TagName before the '.'
    # Seattle has CSO sites with names like NPDES01
    tokens = line.strip().split(',') # Now have something like ['WMIC.CSOSTATUS_N','3'] for each line
    cso_name = tokens[0].split('.')[0] # Separate out the name for the King County ones. This won't affect the Seattle names.
    cso_status[cso_name] = tokens[1] # Add status entry to the dictionary

# ==================
# BUILD GEOJSON FILE
# ==================
# Initialize feature list for GeoJSON FeatureCollection
cso_feature_list = []
style_dict = {"1":{'marker-color':'#C12D2D',
                   'marker-symbol':'square',
                   'marker-size':'large',
                   'description':'Overflowing now'},
              "2":{'marker-color':'#FFD700',
                   'marker-symbol':'triangle',
                   'marker-size':'medium',
                   'description':'Overflowed in the last 48 hrs'},
              "3":{'marker-color':'#689F38',
                   'marker-symbol':'circle',
                   'marker-size':'small',
                   'description':'No recent overflow'},
              "4":{'marker-color':'#A2A2A2',
                   'marker-symbol':'cross',
                   'marker-size':'small',
                   'description':'Data not available'}
              }

# Open the CSO coordinate file as a CSV DictReader in order to access field names.
with open('cso_coord.csv','rb') as cso_coord_csv:
    reader = csv.DictReader(cso_coord_csv)
    for row in reader:
        status_code = cso_status[row['CSO_TagName']]
        lon = float(row['X_COORD'])
        lat = float(row['Y_COORD'])
        # Use the geojson module to build the feature
        cso_point = geojson.Point((lon,lat))
        cso_feature = geojson.Feature(geometry=cso_point,
            properties={"CSO_TagName":row['CSO_TagName'],
                        "DSN":row['DSN'],
                        "Name":row['Name'],
                        "Time_stamp":status_timestamp,
                        "Location": '{:1.3f} , {:1.3f}'.format(lon,lat),
                        "CSO_Status": status_code,
                        "description": style_dict[status_code]['description'],
                        "marker-color": style_dict[status_code]['marker-color'],
                        "marker-symbol": style_dict[status_code]['marker-symbol'],
                        "marker-size": style_dict[status_code]['marker-size']
                        })
        cso_feature_list.append(cso_feature)

# Create a FeatureCollection
cso_feature_collection = geojson.FeatureCollection(cso_feature_list)

# Dump the FeatureCollection to a GeoJSON file in the same directory as this script.
with open('cso_test_file.geojson', 'wb') as out_file:
   out_file.write(geojson.dumps(cso_feature_collection))

# =====================
# PUSH UPDATE TO GITHUB
# =====================
# call is from the subprocess module
call('git add .', shell = True)
call('git commit -m "Status for ' + status_timestamp + '"', shell = True)
call('git push origin master', shell = True)
