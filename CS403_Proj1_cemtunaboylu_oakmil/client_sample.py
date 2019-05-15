from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
import datetime
import requests, json
import http.client

URL = 'http://127.0.0.1:5000'

favor = {'message':'JOIN', 'verifying_key': 987654321}
another_favor = {'message':'VERIFY', 'requested_ip': 9871}
favor_ = json.dumps(favor)
conn = http.client.HTTPConnection('localhost', 5000)

conn.request("GET", "/JOIN", favor_)
resp= conn.getresponse()

#resp = request.get(URL+'/', data=(favor),verify=False)
print(resp)
