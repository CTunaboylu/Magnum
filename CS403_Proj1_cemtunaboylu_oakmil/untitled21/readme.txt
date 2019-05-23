chain_IPAddress_II.txt file anatomy:
hash
block
signatures line by line 
hash
block
signatures line by line
.
.
.
Peer Class:
	ips as parameters are port numbers for the peer. Since they already work on localhost, jsut their ports are enough  
Validator Class: 
	from the parameters of terminal helper, we can deduce the number of validators.
	Then we will gradually increment their ports with respect to the iteration

Terminal format for terminal_helper : python python_script.py
						-l block_length 
						-r how_many_rounds
						-k number of peers : 3k+1
						-p port

				

