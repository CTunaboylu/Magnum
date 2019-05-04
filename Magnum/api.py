import requests
from flask import Flask, request, jsonify
from flask_restful import Resource, api
from typing import Dict, List
from threading import Thread

_DEBUG = True
_trial = True

API_URL = 'http://127.0.0.1:5000'

endpoint = '{}/'.format(API_URL)


response = requests.put((endpoint), json={'PNR': '1274S'})
content = (response.json())
print (content)
print (content['PNR'])
print (response.status_code)
if response.ok:
        print('item created')

response = requests.get((endpoint), json={'PNR': '1274S', 'seat_number': 14})
if response.ok:
        print ("item found")
        content = (response.json())
        print (content['PNR'])

class Network:
	__network = dict()
	__endpoint = ''
	def __init__(self, api_url:str, ):
		endp = '{}/'.format(api_url)
		self.__endpoint = endp
		self.__app = Flask(__name__)
		self.__api = Api(app)
		
	def add_2_network(self,ip:str, p_key:ecdsa.keys.VerifyingKey):
		self.__network[ip] = p_key
		return b'OK'
		
	def get(self):
		if _DEBUG:
			print("listening...")
		data =(request.get_json())
		if b'JOIN' in data['message']:
			
	def listen(self):
		
