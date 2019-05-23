import random, string, sys
import ecdsa, hashlib
import binascii
import zmq, request, json, socket
from threading import Thread
import MessageChannelAgent
from typing import List, Dict
import sys, peer, terminal_helper

class Validator(peer.Peer):
   	
    def __init__(self, ip: str, api_url='R'): # True to zmq.REP
	Peer.__init__(self,ip, api_url, True)
	self.join()
        self.listen()

    def listen(self):
        while True:
		self.validate()

validators = []
step_one = terminal_helper.take_care(sys.args)
if step_one:
	k = terminal_helper.K
	MAJORITY = 2*k + 1 
	WHOLE = terminal_helper.num_of_peers
	PORT = terminal_helper.PORT # int
	i = 0
	for i in range(WHOLE-1):
		port_to_go = PORT + i
		validators.append(Thread(target=Validator, args=(str(port_to_go), terminal_helper.API_URL)))
		validators[i].start()
	
	

