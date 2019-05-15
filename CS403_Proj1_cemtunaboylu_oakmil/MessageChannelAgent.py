#TEST THE API 	
import http.client, socket, json
import ecdsa, hashlib
from api import registration, here_is_the_key, listing, app
import celery
from celery.result import AsyncResult

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
print("Computer Name :" + hostname)    
print("Computer IP :" + IPAddr) 

class MCA:

	def __init__(self, ip:str, port:int):
		#self.ip = ip
		#self.port = port	
		
	def post_API(self,to_join, endpoint:str,ip, data):
		"""
		p = registration.delay(ip, data)
		print ('Task-ID: {}'.format(p.task_id))
		print ('Result-async: {}'.format(p.result))
		print ('Result-async: {}'.format(p.result))
		print ('Result-async: {}'.format(p.result))
		print(p.backend)
		print ('Result-sync: {}'.format(p.get()))

		res = app.AsyncResult(p.task_id)
		print(res.ready())
		"""
		self.__connection = http.client.HTTPConnection(to_join)
		self.__connection.request('POST', endpoint, data)
		self.__connection.close()
		return self.__connection.getresponse()
	def get_Ver_Key(self, to_join, endpoint:str): # data is embedded in the endpoint /ver_key/<req_self.ip>
		"""
		v = here_is_the_key.delay(ip)
		print ('Task-ID: {}'.format(v.task_id))
		print ('Result-async: {}'.format(v.result))
		print ('Result-async: {}'.format(v.result))
		print ('Result-async: {}'.format(v.result))
		print(v.backend)
		print ('Result-sync: {}'.format(v.get()))
		res = app.AsyncResult(v.task_id)
		print(res.ready())
		"""
		self.__connection = http.client.HTTPConnection(to_join)
		self.__connection.request('GET', endpoint)
		self.__connection.close()
		return self.__connection.getresponse()
	def get_List(self, to_join, endpoint):
		"""
		n = listing.delay(ip)
		print ('Task-ID: {}'.format(n.task_id))
		print ('Result-async: {}'.format(n.result))
		print ('Result-async: {}'.format(n.result))
		print ('Result-async: {}'.format(n.result))
		print(n.backend)
		print ('Result-sync: {}'.format(n.get()))
		res = app.AsyncResult(n.task_id)
		print(res.ready())
		"""
		self.__connection = http.client.HTTPConnection(to_join)
		self.__connection.request('GET', endpoint)
		self.__connection.close()
		return self.__connection.getresponse()
		
		

