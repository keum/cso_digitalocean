#!/bin/bash

# change this to your path
cd /home/fred/github/cso_digitalocean
./cso_status_geojson.py

# grab timestamp from file
timestamp=$(<timestamp.txt)

# push update to git
git add timestamp.txt cso_test_file.geojson && \
git commit -m "Status for $timestamp" && \
git push
