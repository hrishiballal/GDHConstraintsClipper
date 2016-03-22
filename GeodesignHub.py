import requests, json

class GeodesignHubClient():

	def __init__(self, url, token, project_id):
		self.projectid = project_id
		self.token = token
		self.securl = url if url else 'https://www.geodesignhub.com/api/v1/'

	def get_all_systems(self):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems' + '/'
		headers = {'Authorization': 'Token '+ self.token}
		r = requests.get(securl, headers=headers)
		return r

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

	def get_boundaries_geoms(self):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'boundaries' + '/'
		headers = {'Authorization': 'Token '+ self.token}
		r = requests.get(securl, headers=headers)
		return r

	def post_as_diagram(self,geoms, projectorpolicy, featuretype, description, sysid ):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(sysid) + '/'+ 'add' +'/' + projectorpolicy +'/'
		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}
		postdata = {'geometry':geoms, 'description':description, 'featuretype':featuretype}
		r = requests.post(securl, headers= headers, data = json.dumps(postdata))
		return r

	def post_as_ealuation_JSON(self, geoms, sysid, username=None):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(sysid) + '/e/map/json/'
		if username:
			securl += username +'/'
		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}

		r = requests.post(securl, headers= headers, data = json.dumps(geoms))
		return r

	def post_as_impact_JSON(self, geoms, sysid, username=None):
		''' Create a requests object with correct headers and creds. '''

		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(sysid) + '/i/map/json/'
		if username:
			securl += username +'/'

		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}
		r = requests.post(securl, headers= headers, data = json.dumps(geoms))
		return r

	def post_as_evaluation_GBF(self, geoms, sysid, username=None):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(sysid) + '/e/map/gbf/'
		if username:
			securl += username +'/'
		headers = {'Authorization': 'Token '+ self.token}

		r = requests.post(securl, headers= headers, files = {'geoms.gbf':geoms})
		return r


	def post_gdservice_JSON(self, geometry, jobid):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'gdservices/callback/'
		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}
		data = {"geometry": geometry, "jobid": jobid}
		r = requests.post(securl, headers= headers, data = json.dumps(data))
		return r

	def post_as_impact_GBF(self, geoms, sysid, username=None):
		''' Create a requests object with correct headers and creds. '''

		securl = self.securl+ 'projects'+ '/' + self.projectid + '/' +'systems'+'/'+ str(sysid) + '/i/map/gbf/'
		if username:
			securl += username +'/'
		headers = {'Authorization': 'Token '+ self.token}
		r = requests.post(securl, headers= headers, files = {'geoms.gbf':geoms})
		return r
