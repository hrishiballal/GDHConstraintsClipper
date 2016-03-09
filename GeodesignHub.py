import requests, json

class GeodesignHubClient():

	def __init__(self, url, token, project_id):
		self.projectid = project_id
		self.token = token
		self.securl = url if url else 'https://www.geodesignhub.com/api/v1/'

	def get_diagram_geoms(self, diagid):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'diagrams' + '/'+ str(diagid) +'/'
		headers = {'Authorization': 'Token '+ self.token}
		r = requests.get(securl, headers=headers)
		return r

	def get_constraints_geoms(self):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'constraints' + '/'
		headers = {'Authorization': 'Token '+ self.token}
		r = requests.get(securl, headers=headers)
		return r

	def post_as_diagram(self,geoms, projectorpolicy, featuretype, description, reqid ):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(reqid) + '/'+ 'add' +'/' + projectorpolicy +'/'
		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}
		postdata = {'geometry':geoms, 'description':description, 'featuretype':featuretype}
		r = requests.post(securl, headers= headers, data = json.dumps(postdata))
		return r

	def post_as_ealuation_JSON(self, geoms, reqid, username=None):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(reqid) + '/e/map/json/'
		if username:
			securl += username +'/'
		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}

		r = requests.post(securl, headers= headers, data = json.dumps(geoms))
		return r

	def post_as_impact_JSON(self, geoms, reqid, username=None):
		''' Create a requests object with correct headers and creds. '''

		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(reqid) + '/i/map/json/'
		if username:
			securl += username +'/'

		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}
		r = requests.post(securl, headers= headers, data = json.dumps(geoms))
		return r

	def post_as_evaluation_GBF(self, geoms, reqid, username=None):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(reqid) + '/e/map/gbf/'
		if username:
			securl += username +'/'
		headers = {'Authorization': 'Token '+ self.token}

		r = requests.post(securl, headers= headers, files = {'geoms.gbf':geoms})
		return r

	def post_as_impact_GBF(self, geoms, reqid, username=None):
		''' Create a requests object with correct headers and creds. '''

		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(reqid) + '/i/map/gbf/'
		if username:
			securl += username +'/'
		headers = {'Authorization': 'Token '+ self.token}
		r = requests.post(securl, headers= headers, files = {'geoms.gbf':geoms})
		return r
