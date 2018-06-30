import requests
import json

API_ENDPOINT = "https://facebooklogger.herokuapp.com/"

class token:
	def __init__(self,uniqueToken):
		self.uniqueToken = uniqueToken
		self.service = None
	
	def add_name(self, service):
		self.service = service
		return True

	def message(self, loggingMessage):
		if not self.service:
			self.service = "NO1"
		headers = {
			'content-type': 'application/json',
		}
		url=API_ENDPOINT+'logging/'+self.service+'/'+self.uniqueToken
		if type(loggingMessage) != str:
			loggingMessage = json.dumps(loggingMessage,indent=2)
		r = requests.post(url,data=loggingMessage,headers=headers)
		if r.status_code>=300 or r.status_code <200:
			raise Exception('Wrong Toke')
		return r.status_code