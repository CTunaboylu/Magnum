# to install ecdsa, run "pip3 install ecdsa" in the command prompt
import random
import string
import sys
import ecdsa
import hashlib
import binascii

# randomly generate secret and public keys
sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc = hashlib.sha256)
pk = sk.get_verifying_key()
print("public key:", binascii.hexlify(pk.to_string()))

# a message to sign
name = "erkay"

# signature of the message
signature = sk.sign(name.encode('utf-8'))

# print the signature in hex
print ("Signature for message 'erkay': ", binascii.hexlify(signature))

# verify the signature
# (need to catch the exception if it does not verify)
print("This must be True: ") 
try:
    print (pk.verify(signature, name.encode('utf-8')))
except ecdsa.BadSignatureError:
    print (False) 

# verify the signature for an incorrect message (should not verify)
name = "erkan"
print("This must be False: ")
try:
    print (pk.verify(signature, name.encode('utf-8')))
except ecdsa.BadSignatureError:
    print (False)

# generate a block of l = 10 transactions
# each transaction is a random string
# the first block of transactions
h = ""   # set to empty string as it is the first block
block = h
for i in range(0,10):
    tx = "".join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    block += tx + "\n"  
h = hashlib.sha256(block.encode('utf-8')).hexdigest()
print(f'Hash of the block: {h}')
print ("The transaction block: \n", block)
signature = sk.sign(block.encode('utf-8'))

print ("Signature for the block: ", binascii.hexlify(signature))

try:
    print (pk.verify(signature, block.encode('utf-8')))
except ecdsa.BadSignatureError:
    print (False)

# the second block of transactions
block = h  # set to the hash of the previous block
for i in range(0,10):
    tx = "".join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    block += tx + "\n"  
h = hashlib.sha256(block.encode('utf-8')).hexdigest()    
print(f'Hash of the block: {h}')

print ("The transaction block: \n", block)
signature = sk.sign(block.encode('utf-8'))

print ("Signature for the block: ", binascii.hexlify(signature))

try:
    print (pk.verify(signature, block.encode('utf-8')))
except ecdsa.BadSignatureError:
    print (False)

# the third block of transactions
block = h  # set to the hash of the previous block
for i in range(0,10):
    tx = "".join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    block += tx + "\n"  
h = hashlib.sha256(block.encode('utf-8')).hexdigest()
print(f'Hash of the block: {h}')

print ("The transaction block: \n", block)
signature = sk.sign(block.encode('utf-8'))

print ("Signature for the block: ", binascii.hexlify(signature))

try:
    print (pk.verify(signature, block.encode('utf-8')))
except ecdsa.BadSignatureError:
    print (False)    
