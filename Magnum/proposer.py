#proproses a block of transaction to the other validators 
# n = 3k + 1 
#REST API FOR p2p Network 


import random, string, sys
import ecdsa, hashlib
import binascii
import zmq, request, json 

from typing import List, Dict

_DEBUG = True
_sample = True
k = 3
MAJORITY = 2*k + 1
WHOLE = 3*k + 1

def generate_block(len:int):
	h = ''
	block = h
	for i in range(len):
		tx = "".join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
		block += tx + "\n"  
	h = hashlib.sha256(block.encode('utf-8')).hexdigest()
	if _DEBUG:
		print ("The transaction block: \n", block)
	return block

class Peer:
	__IP = '' # just port numbers for this assignement
	__ID = 0
	__socket = zmq.Context().socket(zmq.REQ) 
	__block = '' 
	__verifying_key = ecdsa.keys.VerifyingKey
	__signing_key = ecdsa.keys.SigningKey
	def __init__(self, ip:str, id:int, api_url = 'R'):
		self.__IP = ip
		self.__ID = id
		self.__socket.connect('tcp://'+self.__IP)	
		self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc = hashlib.sha256)
		self.__verifying_key = self.__signing_key.get_verifying_key()
		if 'R' in api_url:
			#means that this is the root to create the API
			if len(api_url) == 1: # create with default local IP
				api_url = 'http://127.0.0.1:5000'
			self.__network_bridge = '{}/'.format(api_url)
		
	def join(self):
		response = requests.put((self.__network_bridge), json={'Message': b'JOIN', 'verifying_key' : self.__verifying_key})
		content = (response.json())
		if _DEBUG: 
			print(content)
		if b'OK' in content['Message']:
			return 
		else: 
			return
			# take care
	def request_verifying_key(self, ip:str):
		response = requests.put((self.__network_bridge), json={'Message': b'JOIN', 'verifying_key' :self.__verifying_key})
		content = (response.json())
		if _DEBUG:
			print(content)
		return content['requested_verifying_key']

	def propose(self, len:int):
		self.__block = generate_block(len)
		signature = sign_the_block(self.__block, self.__signing_key)
		#ask
		#listen		
	def ask_4_a_consensus(self, assembly:Dict):
		pass
	def listen(self):
		consensus = 1 # current node included 
		counter = 1 # current node included 
		while consensus < MAJORITY or counter < WHOLE:
			message = self.__socket.recv() # json {'block' : block:str, 'signature': sign:bytes }
			counter += 1
			if message['block'] == self.__block:
				verify(message['signature'])
	def verify(self, signature:bytes, ip:str, block_of_validator:str):
		pub_key_from_api = requested_verifying_key(ip)
		result = pub_key_from_api.verify(signature, block_of_validator.encode('utf-8'))
		if _DEBUG:
			print('current peer block : '+self.__block)
			print('received block : ' + block_of_validator)	
		if result:
			consensus += 1
			if _DEBUG: 
				print("Verified signature...")
	def this_is_your_block(self, blck:str):
		self.__block = blck
	def sign(self):
		signature = self.__signing_key.sign(self.__block.encode('utf-8'))	 
		if _DEBUG:
			print(f"Signature for the block: {block} is {signature}")
		return signature
class Proposer(Peer):
	pass	
class Validator(Peer):
	pass
if _sample:
	sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc = hashlib.sha256)
	pk = sk.get_verifying_key()
	#print("public key:", binascii.hexlify(pk.to_string()))
	print(type(pk))
	print(type(sk))
	block = generate_block(10)
	signature = sk.sign(block.encode('utf-8'))
	print(pk.verify(signature, block.encode('utf-8')))
