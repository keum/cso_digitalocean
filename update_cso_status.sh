#!/bin/bash

# source /home/fred/.bash_profile

# change this to your path
cd /home/ubuntu/workspace/cso_digitalocean
./cso_status_geojson.py

# grab timestamp from file
timestamp=$(<timestamp.txt)

# push update to git
git add -A
git commit -m "Status for $timestamp"
git push origin master
