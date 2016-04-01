# King County Real-Time CSO Status Viewer

Requires [geojson](https://pypi.python.org/pypi/geojson/).

## Background
Reads the CSO status from King County's web server and combines it with a CSV file of the point coordinates,
then creates a GeoJSON file of the current CSO status for King County and Seattle.

The resulting GeoJSON file can be added to a webmap.

Example CSO status data from [King County's server](http://your.kingcounty.gov/dnrp/library/wastewater/cso/img/CSO.CSV):

		CSO_TagName,04-01-2016 09:30:01 AM
		11TH.CSOSTATUS_N,3
		30TH.CSOSTATUS_N,3
		NPDES072,3
		...

The coordinates (lat, lon, EPSG 3857) are in a CSV file.

		CSO_TagName,X_COORD,Y_COORD,Name,DSN
		ALKI,-122.4225,47.57024,King County CSO: Alki,051
		ALSK,-122.406947,47.559442,King County CSO: Alaska St SW,055
		...
## Output
The current CSO status is zipped up with the coordinates and properties for each CSO location. 
Properties included are:

| Property      | Value                                                                                                                              |
|---------------|------------------------------------------------------------------------------------------------------------------------------------|
| CSO_TagName   | Name code for  CSO location                                                                                                        |
| DSN           | Data Source Name                                                                                                                   |
| Name          | Long name for CSO location                                                                                                         |
| Time_stamp    | Timestamp of most recent query                                                                                                     |
| CSO_Status    | CSO status code (1 - 4)                                                                                                            |
| Description   | Description of CSO status code. <ol> <li>Overflowing now</li> <li>Overflowed in the last 48 hours</li> <li>No recent overflow</li> <li>Data not available</li></ol>|
| marker-color  | <ol> <li>Red</li> <li>Yellow</li> <li>Green</li> <li>Grey</li> </ol>                                    							 |
| marker-symbol | <ol> <li>square</li> <li>triangle</li> <li>circle</li> <li>cross</li> </ol>                                                       |
| marker-size   | <ol> <li>large</li> <li>medium</li> <li>small</li> <li>small</li> </ol>                                                   |

## Running with cron

Make sure that both `cso_status_geojson.py` and `get_cso_status.sh` are executable. 
Modify the path in `get_cso_status.sh` to reflect where the repo was cloned.
		
		#!/bin/bash

		# change this to your path
		cd /home/fred/github/cso_digitalocean
		./cso_status_geojson.py
		
Then use `crontab -e` to set up the cron job. This example will run every 15 minutes (at :00, :15, :30, and :45):

		*/15 * * * * /home/fred/github/cso_digitalocean/get_cso_status.sh # KC CSO status
