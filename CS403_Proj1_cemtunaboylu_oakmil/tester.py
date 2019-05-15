"""LIBRARIES"""
from threading import Thread
from typing import List, Dict
import ecdsa, hashlib 
import binascii, string, random

import time 
"""LIBRARIES_END"""
_DEBUG = True

# Update the list size by number of peers 
#file format for peer files : chain_{IPAddress}.txt 

""" Each thread will have an ID [0, peer_number], after the check it will update validation_list[thread_id] to True or False. For performance we will have the hash of the list which is full of True values - assuming that the peer count does not change. If so, new hash will be generated. - . If it is necessary to check if all peers have the 'correct' chain, it will be faster to check if the current hash matches the AllTrueHash. 

# thread ids are their indexes in the controllers list for simplicity 
controllers = [] 

# Communicate to the API to have the up to date network information : number of peers, peer IP and peer validation key

# returns the network array -> here, divide it to useful parts
def take_a_look_at_network():
"""	

#_io.TextIOWrapper
# iofile.readlines()
# FINAL HASH VALIDATION
# RELATED VARIABLES:
hash_dict = dict()

# IP_List will be given, threads will partition the list one by one and check the hashes, if multiple final hashes are found they will be stored as hash:amount to be able observe ratios of hashes
def count_consensus(ip:str, h_dict:Dict): 
	pass 
# FINAL HASH VALIDATION END 
# HASH CHAIN VALIDATION FUNCTIONS
# RELATED VARIABLES:
validation_list = []
validation_hash = 0

def validate_hash_chain(id:int, val_list:List, transactions:List, block_num:int):
	passes = True
	block_len = 32 # built in 
	offset = 0
	while passes and len(transactions[offset:]) ==  block_len:
		block = transactions[offset:offset+block_len]
		offset += block_len
		block_hash = transactions[offset+block_len+1]	   		
		h = hashlib.sha256(block.encode('utf-8')).hexdigest()
		# compare 
		if h == block_hash:
			if _DEBUG:
				print("They match")
				print(h)
			passes = True
		else:
			passes = False			
	val_list[id] = passes
	
# Communicate with API and get ip, val_key, len(network)	
def evaluate(validation_hash:int, id:int, peer_ip:str, peer_val_key:ecdsa.keys.VerifyingKey, val_list:List, block_num:int):
	
	with open(f'chain_{peer_ip}.txt ','r') as text_file:
		line_list = text_file.readlines()
	validate_hash_chain(id, peer_ip, line_list, block_num)
	hash_chain_OK = check_val_list(validation_hash,validation_list)	

def update_list(val_list:List):
	len_val = len(val_list)
	if len_val == num_of_peers:
		return 
	elif len_val < num_of_peers: # list is shorter then it needs to be 
		diff = num_of_peers - len_val
		val_list.append(True for n in range(diff)) 
		return hash(frozenset(val_list)) # return new validation hash 
	else: # len val > num_of_peers
		pass	 
def check_val_list(validation_hash:int, val_list:List):
	h = hash(frozenset(val_list)) # we know the hash of the updated list -v all True
	if validation_hash == h:
		return True 
	else :
		return False 
# HASH CHAIN VALIDATION FUNCTIONS END 
# MAIN PART 
def test(validation_hash:int, validation_list:List, block_amount:int):
	network_ip = ''
	current_network = learn(network_ip)
	thread_list = []
	for index,peer in enumerate(current_network):
		thread_list[index] = Thread(target = evaluate, args=(validation_hash, index, peer.get_IP(), peer.get_ver_key(), validation_list, block_amount ))
		validation_list[peer.get_IP()] = True
	validation_hash = hash(frozenset(validation_list))
		
"""
l = []
for i in range (20):
	l.append(random.choice(string.ascii_letters + string.digits) for n in range(32)) 
start = time.perf_counter_ns()
m = frozenset(l)	
finish = time.perf_counter_ns() - start
print(f'Time elapsed in nano sec: {finish}')
print(hash(frozenset(l)))	
print(type(hash(frozenset(l))))	

l.append(random.choice(string.ascii_letters + string.digits) for n in range(32)) 
print(hash(frozenset(l)))
 """
s = random.choice(string.ascii_letters + string.digits)
h = hashlib.sha256(s.encode('utf-8')).hexdigest()
print(h)
print(type(h))
