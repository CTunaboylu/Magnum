"""LIBRARIES"""
from threading import Thread, Lock
from typing import List, Dict
import ecdsa, hashlib 
import binascii, string, random, sys
import 
import time 
"""LIBRARIES_END"""
_DEBUG = True

""" Each thread will have an ID [0, peer_number], after the check it will update validation_list[thread_id] to True or False. For performance we will have the hash of the list which is full of True values - assuming that the peer count does not change. If so, new hash will be generated. - . If it is necessary to check if all peers have the 'correct' chain, it will be faster to check if the current hash matches the AllTrueHash. 

# thread ids are their indexes in the controllers list for simplicity 

# IP_List will be given, threads will partition the list one by one and check the hashes, if multiple final hashes are found they will be stored as hash:amount to be able to observe ratios of hashes->we expect at least MAJORITY of peers to have the same hashes 
# Communicate to the API to have the up to date network information : number of peers, peer IP and peer validation key

# returns the network array -> here, divide it to useful parts

	CHAIN FILE FORMAT:
	Hash:hash:decoded('utf-8') 
	Block:block of length l
	Signatures:signatures \n of length 3k+1 decoded('utf-8') 
note: A peer includes its own signature at the end of the signatures to make sure that the count adds up to MAJORITY(2k+1) when checking since it is the part of the consensus group
"""

#_io.TextIOWrapper

def communicate_with_API(self, method:str,end_p:str, *args):
	conn = http.client.HTTPConnection(self.__api_url)
	if len(args) == 0:
		conn.request(method, end_p, args[0])
	else:
		conn.request(method, end_p)
	response = conn.getresponse()
	return response
def validate_hash_chain(block_chain:List, ip:str, l:int): 
	check = True
	cursor = l
	for line in block_chain:
		if 'Hash:' in line:
			break
		else:
			cursor += 1	
		
	#first line is an empty hash 
	while cursor < len(block_chain):
		block = ''.join(block_chain[cursor+1:l])
		h_prev = hashlib.sha256(block.encode('utf-8')).hexdigest()
		check = h_prev == block_chain[cursor]
		for line in block_chain[cursor:]:
			if 'Hash:'  in line:
				break
			else:
				cursor += 1 
	return check

def check_signatures_of_consensus(block_chain:List, ip:str, l:int, MAJORITY:int): 
	cursor = l
	in_block = 1
	for line in block_chain:
		if 'Signatures:' in line:
			in_block += 1
			break
		else:
			cursor += 1	

	#first line is an empty hash 
	while cursor < len(block_chain):
		signatures= block_chain[cursor+1:l]
		if len(signatures) < MAJORITY:
			print(f'In block{in_block}, the signatures are less than majority')
			return False
		for line in block_chain[cursor:]:
			if 'Signatures:'  in block_chain:
				in_block += 1
				break
			else:
				cursor += 1 
	return True	

	
def evaluate_chains_of_peers(block_chain:List, id:int, MUTEX, peer_ip:str, val_dict:Dict):
		#hash(frozenset(val_dict)) can be used if fail 
	whole = ''.join(block_chain)
	h_whole = hashlib.sha256(whole.encode('utf-8')).hexdigest()
	MUTEX.acquire()
	if h_whole in val_dict:
		val_dict[h_whole] += 1
	else:
		val_dict[h_whole] = 1 # add to the hash dict
	MUTEX.release()
	return

def check_val_dict(validation_dict:Dict, MAJORITY:int):
	closest = ''
	for key in validation_dict:
		if _DEBUG:
			print(f'For {key} there are '+str(validation_dict[key])+'peers' )
		if validation_dict[key] >= MAJORITY:
			return (True, key, validation_dict[key])
		elif validation_dict[key] > validation_dict[closest]:
			closest = key
			
	# if we are here there is no majority
	return (False, closest,validation_dict[closest]) 

def THREAD_TEST(block_chain:List, id:int, ip:str, l:int, MAJORITY:int, MUTEX, validation_dict:Dict)
	signature_check = check_signatures_of_consensus(block_chain,ip,l,MAJORITY)
	hash_chain_validation = validate_hash_chain(block_chain, ip, l)	
	evaluate_chains_of_peers(block_chain, id, MUTEX, ip, validation_dict)
	if signature_check and hash_chain_validation:
		print(f'Thread {id} for {ip}, signatures and hash chains are valid')
	else:
		if signature_check:
			print(f'Thread {id} for {ip}, signatures are valid BUT HASH CHAINS FAILED')
		elif hash_chain_validation:
			print(f'Thread {id} for {ip}, hash chains are valid BUT SIGNATURES FAILED')
		else:
			print(f'Thread {id} for {ip}, ALL FAILED')


controllers = []
network = communicate_with_API('GET','/list')
val_dict = dict() # {hash:amount} 

l = input('Length of block:')
k = input('K for peer amount (3K+1)')
r = input('Number of rounds:')

MAJORITY = (2*k)+1
MUTEX = Lock()
for index,ip in enumerate(network):
	try:
		b_c = []
		with open(f'chain_{ip}_II.txt') as f:
			b_c = f.readlines()		
		controllers[index] = Thread(target = THREAD_TEST, args=(b_c, val_dict, MAJORITY, MUTEX, index, ip, l))
		controllers[index].start()
	except: 
		print(sys.exc_info()[0])

for c in controllers:
	c.join()

do_we_have_consensus, which_key, by_how_much = check_val_dict(val_dict, MAJORITY)

print('RESULT:')
print('Could the network have a consensus: '+str(do_we_have_consensus)+' with '+ which_key + 'by '+ str(by_how_much)+'/'+ str(MAJORITY))

"
