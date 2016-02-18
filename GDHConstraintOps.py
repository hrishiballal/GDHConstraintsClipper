import requests, json, GeodesignHub
import shapelyHelper
import logging
from shapely.geometry.base import BaseGeometry
from shapely.geometry import shape, mapping, shape, asShape
from shapely.geometry import MultiPolygon, MultiPoint, MultiLineString
from shapely import speedups
import shapelyHelper

class ConstraintsClipper():
	''' A class to conduct basic (6) GIS operations during copy diagrams. '''

	def genFeature(self, geom, allGeoms, errorCounter):
		try:
			curShape = asShape(geom)
			allGeoms.append(curShape)
		except Exception as e:
			logging.error(explain_validity(curShape))
			errorCounter+=1
		return allGeoms, errorCounter

	def clipToConstraints(self, constraints, diaggeoms):
		boundaryGeoms = []
		finalGeoms = []
		diagGeoms = []
		for curFeature in constraints['features']:
			if curFeature['properties']['areatype'] =='boundaries':
				boundaryGeoms, errorCounter = self.genFeature(curFeature['geometry'],allGeoms=boundaryGeoms, errorCounter=0)

		for curFeature in diaggeoms['features']:
			diagGeoms, errorCounter = self.genFeature(curFeature['geometry'],allGeoms=diagGeoms, errorCounter=0)

		for curDiagGeom in diagGeoms:
			for boundaryGeom in boundaryGeoms:
				d = curDiagGeom.intersects(boundaryGeom)
				if d:

					d = curDiagGeom.intersection(boundaryGeom)
					d= json.loads(shapelyHelper.export_to_JSON(d))

					if (d['type']=='MultiPolygon'):
						for curCoords in d['coordinates']:
							f = {}
							f['type']= 'Feature'
							f['properties']= {}
							f['geometry']= {'type':'Polygon', 'coordinates':curCoords}
							finalGeoms.append(f)

					else:
						scf = {}
						scf['type']= 'Feature'
						scf['properties']= {}
						scf['geometry']= d
						finalGeoms.append(scf)


		return finalGeoms


if __name__ == "__main__":
	firstAPIHelper = GeodesignHub.GeodesignHubClient(url = 'http://local.dev:8000/api/v1/', project_id='62ead880b1592bc0', token='5d72a5465bc8a61bb6dd02457cbf97150735bfbf')


	r1 = firstAPIHelper.get_constraints_geoms()
	firstDiagID = 58 # diagram to be clipped to constraints.
	r2 = firstAPIHelper.get_diagram_geoms(firstDiagID)

	if r1.status_code == 200:

		op = json.loads(r1.text)
		constraints = op['geojson']

	if r2.status_code == 200:
		op = json.loads(r2.text)
		diaggeoms = op['geojson']

	myConstraintsClipper = ConstraintsClipper()
	choppedFeatures = myConstraintsClipper.clipToConstraints(constraints, diaggeoms)

	# print len(choppedFeatures)

	for curFeat in choppedFeatures:
		tmpGJ = {'type':'FeatureCollection', 'features': [curFeat]}
		targetReqID= 13
		# print json.dumps(tmpGJ)
		upload = firstAPIHelper.post_as_diagram(geoms = tmpGJ, projectorpolicy= 'project',featuretype = 'polygon', description= 'Chopped Corridoor', reqid = targetReqID)
		print upload.text
