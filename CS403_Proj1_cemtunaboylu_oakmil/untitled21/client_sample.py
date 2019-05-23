from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
import datetime
import requests, json
import http.client
import ecdsa 
import hashlib
URL = 'http://127.0.0.1:5000'

sk = ecdsa.SigningKey.generate(curve = ecdsa.NIST256p, hashfunc=hashlib.sha256)
vk = sk.get_verifying_key()
vk = vk.to_string().decode('latin1')
favor = {'verifying_key': vk}
print(vk)
print(type(vk))

#another_favor = {'message':'VERIFY', 'requested_ip': 9871}
favor_ = json.dumps(favor)
conn = http.client.HTTPConnection('localhost', 5000)

conn.request('POST', '/join', favor_)
resp= conn.getresponse()

#resp = request.get(URL+'/', data=(favor),verify=False)
print(resp)
