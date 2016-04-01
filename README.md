# King County Real-Time CSO Status Viewer

Requires [geojson](https://pypi.python.org/pypi/geojson/).

Reads the CSO status from King County's web server and combines it with a CSV file of the point coordinates,
then creates a GeoJSON file of the current CSO status for King County and Seattle.

The resulting GeoJSON file can be added to a webmap.

Example CSO status data from [King County server](http://your.kingcounty.gov/dnrp/library/wastewater/cso/img/CSO.CSV):

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



formatted_geojson_data_dict = {'type':'FeatureCollection','features':
[{'type':'Feature','properties':{},'geometry':{'type':'Point','coordinates':[]}}]}

NEED a Data structure template in python to look like this then convert to  GeoJSON

{'type':'FeatureCollection",
  'features': [{'type': 'Features',
                'properties':{'CSO_TagName': 'ALKI',
                              'Value': 3},
                'geometries':{'type':'point',
                'coordinates':[-122.322,
                              47.607]}
                }
               ]
}

"""
