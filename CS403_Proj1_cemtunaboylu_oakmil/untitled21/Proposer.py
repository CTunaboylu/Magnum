import random, string, sys
import ecdsa, hashlib
import binascii
import zmq, request, json, socket
import terminal_helper

from threading import Thread
from typing import List, Dict

from CS403_Proj1_cemtunaboylu_oakmil.peer import Peer

_DEBUG = True


class Proposer(Peer):
    def __init__(self, ip: str, api_url='R'):
        Peer.__init__(self, ip,api_url, False)
        x = Thread(target=self.implement_API)
        x.start()
        # self.implement_API()
        if _DEBUG:
		print('Proposer constructed')

    def implement_API(self):
        # default mode
        import os
        cmd = 'python api.py'
        os.system(cmd)
        if _DEBUG:
            print('Implementation of API finished.')
if _DEBUG:
	print(len(sys.args))
	print(sys.args)

# 0 being the script itself 

step_one = terminal_helper.take_care(sys.args)
if step_one:
	k  = terminal_helper.K
	WHOLE = terminal_helper.num_of_peers
	MAJORITY = 2*k + 1 
	l = terminal_helper.l_arg
	r = terminal_helper.num_of_rounds
	port = terminal_helper.PORT
	# in this case id of the proposer equals to their ports since in peer.py : self.__IP = ... + str(int)
	proposer = Proposer(str(port), terminal_helper.API_URL, False)
	proposer.propose(r)
