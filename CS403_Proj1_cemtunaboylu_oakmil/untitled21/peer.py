# proproses a block of transaction to the other validators
# n = 3k + 1 

import random, string, sys
import ecdsa, hashlib
import binascii
import zmq, request, json, socket
from threading import Thread, Lock
from typing import List, Dict

from pathlib import Path

_DEBUG = True
k = 3
MAJORITY = 2 * k + 1
WHOLE = 3 * k + 1

def generate_block(len: int):
	block = ''
	for i in range(len):
		tx = "".join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
		block += tx + "\n"
		if _DEBUG:
			print("The transaction block: \n", block)
	return block


def verify(signature: bytes, pub_key_from_api, block_of_validator: str):
	result = pub_key_from_api.verify(signature, block_of_validator.encode('utf-8'))
	if _DEBUG:
		print('received block : ' + block_of_validator)
		if result:
		    print("Verified signature...")
	return result
def send_via_thread(block:str, consensus:Dict, MUTEX, my_ip:str, ip:str, ver_key, signature:bytes ):
	if _DEBUG:
		id = get_ident()
		active_count = active_count()
		s_size = stack_size()
		print(f"Thread Â{id} is started. Stack size is {s_size} Currently there is {active_count} threads.")
	socket = zmq.Context().socket(zmq.REQ)
	socket.connect(ip)
	packet = {'block':block, 'signature':signature.decode('utf-8'), 'sender_ip':my_ip)
	
	socket.send(json.dumps(packet))
	mes = socket.recv()
	sign_outsider = mes['signature']	
	result = verify(sign_outsider.encode('utf-8') ,ver_key, consensus, mes['block'])
	if result:
		MUTEX.acquire()
		try:
			consensus[sign_outsider] = pub_key
		except:
			print(f"Problem with the {ip} peer")
			print("Could not update the consensus dictionnary")
		finally:
			MUTEX.release()
			if _DEBUG:
				print(f" Thread for ip {ip} is finished ")
		
def ask_4_Consensus(consensus:Dict, block: str, my_ip:str, signature:bytes, network:Dict):
	threads = []
	MUTEX = Lock()
	for i,p in enumerate(network):
		if p.ip == my_ip:
			continue
		ip = p
		ver_key = network[p]
		threads.append( Thread( target=send_via_thread, args=(block, consensus, MUTEX, my_ip, ip, ver_key, signature)))
		threads[i].start()
	for t in threads:
		t.join()
	consensus_group = len(consensus)
	if consensus_group+1 >=  MAJORITY: # +1 for self representation in the consensus group
		return (True, consensus_group)
	
	return (False,consensus_group)

class Peer:
	__IP = ''  # just port numbers for this assignement
	__block_file = ''
	__block = ''
	__verifying_key = ecdsa.keys.VerifyingKey
	__signing_key = ecdsa.keys.SigningKey
	__consensus = dict() # dict of signatures and ver keys gathered from peers that are verified
	def __init__(self, ip: str, api_url, is_rep:bool): # ips are ports since they work on local host
		if len(ip) < 6:  # port only
		    self.__IP = '127.0.0.1:' + ip
		else:
		    self.__IP = ip # just a guard in case we give full IP
		self.__block_file = "chain." + ip + "II.txt"
		with open(self.__block_file, 'w') as f:
		    f.close()
		if is_rep: # validator
			self.__socket = zmq.Context().socket(zmq.REP) 
			self.__socket.bind('tcp://' + self.__IP)
		else:
			self.__socket = zmq.Context().socket(zmq.REQ) 
			self.__socket.connect('tcp://' + self.__IP)
		
		self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc=hashlib.sha256)
		self.__verifying_key = self.__signing_key.get_verifying_key()
		self.__api_url = api_url
	def communicate_with_API(self, method:str,end_p:str, *args):
		conn = http.client.HTTPConnection(self.__api_url)
		if len(args) == 0:
			conn.request(method, end_p, args[0])
		else:
			conn.request(method, end_p)
		response = conn.getresponse()
		return response
	def join(self):
		v_key = self.__verifying_key.to_string().decode('latin1')
		join_data = {'verifying_key' : v_key }
		join_data_json = json.dumps(join_data)
		response = self.communicate_with_API('POST', '/join', join_data_json)
		if _DEBUG:
		    print(response)
		if response.status_code == 201:
		    if _DEBUG:
			print('Succesfully joined network.' + self.__IP)
		    return
		else:
		    print('Cannot join the network.' + response.status + ' ' + str(response.status_code))
		    return

	def request_verifying_key(self, ip: str):
		response = self.communicate_with_API('GET', '/ver_key/'+ip)
		if _DEBUG:
		    print(response)
		if 200 in response.status_code:
		    resp = json.loads(response)
		    ver = response['requested_verifying_key'].encode('latin1')
		    ver = VerifyingKey.from_string(ver, curve=NIST256p)
		    if _DEBUG:
			print("Requested verifying key:")
			print(ver)
		    return ver
		else:
		    print('Status code: ' + str(response.status_code) + 'v.key: ' + str(resp))

	def propose(self, num_rounds: int):
		h_prev = ''
		while num_rounds >= 0:
			num_rounds -= 1
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

			# ask
			agreed, consensus_group = ask_4_consensus(self.__consensus, block, signature, self.get_Network())

			if agreed:
				if  _DEBUG:
					print(f'Formed a consensus {consensus}/{MAJORITY}')
				self.this_is_your_block(block)
				#Commit
				self.commit(signature)
				# for starting another round
			else: 
				print('Failed to form a consensus with consensus')
				return 

	def validate(self):
		packet_json = self.__socket.recv()
		packet = json.loads(packet_json)
		
		network = self.get_Network()
		sign_outsider = packet['signature'].decode('utf-8')
		result = verify(sign_outsider, network['sender_ip'], packet['block'])
		if result:
			signature = self.sign(packet['block'])
			if _DEBUG:
				print('block is verified. Starting consensus formation protocol for this node.')
			agreed, consensus_group = ask_4_consensus(self.__consensus, packet['block'], signature, network)
			if agreed:
				if  _DEBUG:
		    			print(f'Formed a consensus {consensus}/{MAJORITY}')
				self.this_is_your_block(block)
				#Commit
				self.commit(signature)
			else: 
				print('Failed to form a consensus with consensus:')
				
	def commit(self, signature:bytes): # self.__block = is the accepted block already, consensus dict is updated too
		# have a lock on the chain if chain is unique, others file waiting - give them an expiration date 
		with open(self.__block_file, 'r+') as f:
			b = f.readlines()
			h_prev = ''
			if len(b) > 0:
				b = "\n".join(b)
				h_prev = hashlib.sha256(b.encode('utf-8')).hexdigest()
			f.write('Hash:'+h_prev+"\n")
			f.write('Block:'+self.__block)
			f.write('Signatures:')
			for c in consensus:	
				f.write(c.decode('utf-8')+"\n")
			#add self to the file 
			f.write(signature.decode('utf-8')+"\n")
	def get_Network(self):
		dic = self.communicate_with_API('GET', '/list')
		return json.loads(dic)
	
	def this_is_your_block(self, blck: str):
		self.__block = blck
	def sign(self):
		signature = self.__signing_key.sign(self.__block.encode('utf-8'))
		if _DEBUG:
		    print(f"Signature for the block {self.__block} is {signature}")
		return signature

	def sign(self, block: str):
		signature = self.__signing_key.sign(block.encode('utf-8'))
		if _DEBUG:
		    print(f"Signature for the block {block} is {signature}")
		return signature

	def get_verifying_key(self):
		return self.__verifying_key

	def get_IP(self):
		return self.__IP
