import random, string, sys
import ecdsa, hashlib
import binascii
import zmq, request, json, socket 
from peer import Peer
from threading import Thread
from MessageChannelAgent import MCA
from typing import List, Dict
import sys


k = 3
MAJORITY = 2*k + 1
WHOLE = 3*k + 1

blocks = dict()

def verify(signature:bytes, pub_key_from_api, block_of_validator:str):
	result = pub_key_from_api.verify(signature, block_of_validator.encode('utf-8'))
	if _DEBUG:
		print('received block : ' + block_of_validator)	
	if result:
		return True
		if _DEBUG: 
			print("Verified signature...")
	else:
		return False
class Validator(Peer):
	__socket = zmq.Context().socket(zmq.REP) 
	def __init__(self, ip:str, id:int, api_url = 'R'):
		if len(ip)<5: # port only
			self.__IP = '127.0.0.1:'+ip
		else:
			self.__IP = ip
		self.__ID = id
		self.__socket.bind('tcp://'+self.__IP)	
		Peer.__init__(self,ip,id,api_url)
		print('Validator constructed')
		self.join()
		self.listen()
	def listen(self):
			while True:
				recv = self.__socket.recv()
				addr = recv.remote_addr
				recv = json.loads(recv)
				block = recv[1]
				sig = recv[2]
				ind = recv[3]
				ver_key = self.request_verifying_key(add)
				if verify():
					b = k + (2*ind)
					e = k + (2*(ind+1))
					network = self.get_Network()
					network = network[b:e]
					if _DEBUG:
						print(network)
					self.ask_4_a_consensus(network,b,e,block,sig)
					global blocks
					signature = self.sign(block)
					blocks[self.__IP] = (block, signature)
					self.__socket.send({'vote_count': result, 'signature': signature, 'blocks':json.dumps(blocks)})

	def ask_4_a_consensus(self, assembly:Dict, beg, end, block, signature):
			thread_list = []
			counter = 0
			#dif = end - beg always 2 for now
			for i,peer in enumerate(assembly):
				if peer.get_ID() == 0: # the ID of the proposer
					continue
				ver_key = request_verifying_key(peer.get_IP())
				thread_list.append(Thread(target=send_validator, args=(i+beg, block, signature, ver_key)))
				thread_list[i].start()
				counter += 1
				if counter == 2:
					break
			for t in thread_list:
				t.join()
			return



def send_validator(i:int, block:str, signature, ip:str, ver_key):
	global blocks
	socket = zmq.Context().socket(zmq.REQ)
	if len(ip) <5:
		# only port is given
		socket.connect('tcp://127.0.0.1:'+ip)
	else:
		socket.connect(ip)
	packet = (block, signature.decode('utf-8'))
	socket.send(json.dumps(packet))
	mes =  socket.recv()
	result = verify(i, mes['signature'], ver_key, mes['block'])	
	if verify:
		blocks[mes.remote_addr] = packet
amount = int(sys.argv[1])

validator_threads = []
for i in range(amount):
	validator_threads.append(Thread(target=Validator, args=('127.0.0.1:50'+str(amount+i),0)))
	validator_threads[i].start()

