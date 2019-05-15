#proproses a block of transaction to the other validators 
# n = 3k + 1 

import random, string, sys
import ecdsa, hashlib
import binascii
import zmq, request, json, socket 
from threading import Thread
from MessageChannelAgent import MCA
from typing import List, Dict

from pathlib import Path


_DEBUG = True
k = 3
MAJORITY = 2*k + 1
WHOLE = 3*k + 1
consensus = []
consensus.append(0 for i in range(k))

if _DEBUG:
	print(consensus)
def generate_block(len:int):
	block  = ''
	for i in range(len):
		tx = "".join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
		block += tx + "\n"  
	if _DEBUG:
		print ("The transaction block: \n", block)
	return block

def verify(counter:int, i:int,signature:bytes, pub_key_from_api, block_of_validator:str):
	result = pub_key_from_api.verify(signature, block_of_validator.encode('utf-8'))
	if _DEBUG:
		print('received block : ' + block_of_validator)	
	if result:
		counter += 1
		if _DEBUG: 
			print("Verified signature...")
def send_validator(i:int, block:str, signature, ip:str, ver_key):
	socket = zmq.Context().socket(zmq.REQ)
	if len(ip) <5:
		# only port is given
		socket.connect('tcp://127.0.0.1:'+ip)
	else:
		socket.connect(ip)
	packet = (block, signature.decode('utf-8'))
	socket.send(json.dumps(packet))
	mes =  socket.recv()
	counter = 0
	for m in mes:
		verify(counter, i, mes['signature'], ver_key, mes['block'])	
	consensus[i] = counter

class Peer:
	__IP = '' # just port numbers for this assignement
	__ID = 0
	__socket = zmq.Context().socket(zmq.REQ) 
	__block_file = '' 
	__block = ''
	__verifying_key = ecdsa.keys.VerifyingKey
	__signing_key = ecdsa.keys.SigningKey
	
	def __init__(self, ip:str, id:int, api_url = 'R'):
		if len(ip)<5: # port only
			self.__IP = '127.0.0.1:'+ip
		else:
			self.__IP = ip
		self.__ID = id
		self.__block_file = "chain."+ip+".txt"
		with open(self.__block_file, 'w') as f:
			f.close()
		self.__socket.connect('tcp://'+self.__IP)	
		self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc = hashlib.sha256)
		self.__verifying_key = self.__signing_key.get_verifying_key()
		if 'R' in api_url:
			#means that this is the root to create the API
			if len(api_url) == 1: # create with default local IP
				api_url = '127.0.0.1'
				port = 5000 + id
			self.__MCA = MCA(api_url, port)
		
	def join(self):
		v_key = self.__verifying_key.to_string().decode('latin1')
		#join_data = {'verifying_key':v_key}
		#join_data = json.dumps(join_data)
		to_join = "127.0.0.1:5000"
		response = self.__MCA.post_API(to_join,'/join', self.__IP, v_key)
		if _DEBUG: 
			print(response)
		if response.status_code == 201:
			if _DEBUG:
				print('Succesfully joined network.'+self.__IP)
			return 
		else: 
			print('Cannot join the network.'+response.status+' '+str(response.status_code))
			return
	
	def request_verifying_key(self, ip:str):
		to_join = "127.0.0.1:5000"
		response = self.__MCA.get_Ver_Key(to_join,'/ver_key/'+ip)
		if _DEBUG:
			print(response)
		if 200 in response.status_code:
			resp = json.loads(response)
			ver = response['request_verifying_key'].encode('latin1')
			ver = VerifyingKey.from_string(ver, curve=NIST256p)
			if _DEBUG:
				print("Requested verifying key:")
				print(ver)
			return ver
		else:
			print('Status code: ' + str(response.status_code)+'v.key: '+str(resp))
	def propose(self, len:int):
		h_prev = ''
		with open(self.__block_file, 'r+') as block_file:
			my_block = block_file.readlines() 
			my_block = "\n".join(my_block)
			if _DEBUG:
				print(my_block)
			h_prev = hashlib.sha256(my_block.encode('utf-8')).hexdigest()
		block = h_prev
		block += generate_block(len)
		signature = self.sign(block)
		if _DEBUG:
			print("Proposed: ***")
			print(block)
			print(signature)
			print("***")
		
		#ask
		consensus = self.ask_4_a_consensus(self.get_Network())
		#listen		
		
		if consensus < MAJORITY: 
			print('Failed to form a consensus with consensus:'+str(consensus)+'on' +str( MAJORITY))
		else:
			print(f'Formed a consensus {consensus}/{MAJORITY}')
			this_is_your_block(block)
			return True  # for starting another round
	def ask_4_a_consensus(self, assembly:Dict):
		thread_list = []
		counter = 0
		for i,peer in enumerate(assembly):
			if peer.get_ID() == self.__ID:
				continue
			ver_key = request_verifying_key(peer.get_IP())
			thread_list.append(Thread(target=send_validator, args=(i, block, signature, ver_key)))
			thread_list[i].start()
			counter += 1
			if counter == k:
				break
		for t in thread_list:
			t.join()
		c = 0
		for p in consensus:
			if p>0:
				c += p
		
		if _DEBUG:
			print('Consensus has finished: Agreed:'+str(c)+'/'+str(MAJORITY))
		return c

	def get_Network(self):
		to_join = "127.0.0.1:5000"
		dic = self.__MCA.get_List(to_join,'/list')
		return dic		
	def this_is_your_block(self, blck:str):
		with open(self.__block_file, 'r+') as f:
			b = f.readlines()
			if len(b) == 0:
				b = ''
				h_prev = ''
			else:
				b = "\n".join(b)
				h_prev = hashlib.sha256(b.encode('utf-8')).hexdigest()
			self.__block = h_prev
			self.__block += blck
			f.seek(0)
			f.write(self.__block)
			f.truncate()
			if _DEBUG:
				print("Previous block hash: "+h_prev)
				print("Current incoming block: "+blck)
				print("Final -v of the self block :"+self.__block)
			
	def sign(self):
		signature = self.__signing_key.sign(self.__block.encode('utf-8'))	 
		if _DEBUG:
			print(f"Signature for the block {self.__block} is {signature}")
		return signature
	def sign(self,block:str):
		signature = self.__signing_key.sign(block.encode('utf-8'))	 
		if _DEBUG:
			print(f"Signature for the block {block} is {signature}")
		return signature
	def get_verifying_key_key(self):
		return self.__verifying_key
	def get_IP(self):
		return self.__IP











