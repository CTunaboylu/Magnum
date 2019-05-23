import sys

opts_fncs = {'-p': change_ip,'-l':blck_len, '-r':num_of_rounds, '-k':num_of_peers}
l_arg = 0
num_of_peers = 0
num_of_rounds = 0
K = 0
PORT = ''
API_URL = 'http://127.0.0.1:5000'
#opts_fncs[myvar](parameter1, parameter2)
def change_port(p:int):
	global PORT
	PORT = p 
def blck_len(l:int, l_arg:int):
	global l_arg
	l_arg = l
def num_of_peers(k:int, num_of_peers:int):
	global num_of_peers
	global K
	K = k
	num_of_peers = 3*k + 1 
def num_of_rounds(r:int,num_of_rounds:int):
	global num_of_rounds
	num_of_rounds=r


def take_care(args):
	lngth = len(args)
	if lngth != 9:
		print('Illegal terminal arguments!')
		return False
	else:
		for i in range(lngth):
			opt = args[i].lower()
			if opt in opts_fncs:
				opts_fncs[opt](int(args[i+1]))
				i+=1
	return True



