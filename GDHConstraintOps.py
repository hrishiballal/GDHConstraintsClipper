import requests, json, GeodesignHub
import shapelyHelper
import logging, config
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
		constraintGeoms = []
		finalGeoms = []
		diagGeoms = []
		for curFeature in constraints['features']:
			if curFeature['properties']['areatype'] =='constraints':
				constraintGeoms, errorCounter = self.genFeature(curFeature['geometry'],allGeoms=constraintGeoms, errorCounter=0)

		for curFeature in diaggeoms['features']:
			diagGeoms, errorCounter = self.genFeature(curFeature['geometry'],allGeoms=diagGeoms, errorCounter=0)

		for curDiagGeom in diagGeoms:
			for constraintGeom in constraintGeoms:
				d = curDiagGeom.intersects(constraintGeom)
				if d:

					d = curDiagGeom.intersection(constraintGeom)
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
	firstAPIHelper = GeodesignHub.GeodesignHubClient(url = config.apisettings['serviceurl'], project_id=config.apisettings['projectid'], token=config.apisettings['apitoken'])
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
