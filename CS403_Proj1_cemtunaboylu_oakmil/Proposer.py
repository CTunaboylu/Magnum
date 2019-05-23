import random, string, sys
import ecdsa, hashlib
import binascii
import zmq, request, json, socket 
from peer import Peer
from threading import Thread
from MessageChannelAgent import MCA
from typing import List, Dict


_DEBUG = True
k = 3
MAJORITY = 2*k + 1
WHOLE = 3*k + 1



class Proposer(Peer):
	def __init__(self, ip:str, id:int, api_url = 'R'):
		Peer.__init__(self,ip,id,api_url)
		x = Thread(target=self.implement_API )
		x.start()
		#self.implement_API()
		print('Proposer constructed')
	
	def implement_API(self):
		#default mode
		import os 
		cmd = 'python api.py'
		os.system(cmd)
		if _DEBUG:
			print('Implementation of API finished.')


proposer = Proposer('127.0.0.1:5001',0)
proposer.propose(10)
