import requests, sys
from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api
from typing import Dict, List
from threading import Thread
from ecdsa import VerifyingKey, NIST256p
import time
from celery import Celery
from celery.result import AsyncResult

_DEBUG = True
_trial = True


API_URL = 'http://127.0.0.1:5000'
PORT = '5000'
network = dict()

app = Flask(__name__)
api = Api(app)

asyn=Celery('tasks')

@asyn.task
def registration(ip:str, ver_key):
    global network
    ver = ver_key.encode('latin1')
    ver = VerifyingKey.from_string(ver, curve=NIST256p)
    network[ip] = ver
    if _DEBUG:
        for x in network:
       	    print (x+':'+network[x].to_string().decode('latin1'))


@asyn.task
def here_is_the_key(ip: str):
    global network
    key = serialize(network[ip])
    to_return = {'requested_verifying_key': key}
    return jsonify(to_return)

@asyn.task
def listing(ip: str):
    global network
    to_return = {'list': network}
    return jsonift(to_return)

#@asyn.task
@app.route('/join', methods=['POST'])
def join():
    data = json.loads(request.data)
    print(data)
    t1 = Thread(target=registration, args=(request.remote_addr, data['verifying_key']))
    t1.start()

    return 'Will be registered in the network in a short time.', 201

#@asyn.task
@app.route('/ver_key/<ip>', methods=['GET'])
def ver_key(ip):
    if _DEBUG:
        print(ip)
    k = here_is_the_key(ip)
    return {'requested_verifying_key': k}, 200

#@asyn.task
@app.route('/list', methods=['GET'])
def list():
    if _DEBUG:
        print('Requested the network list')
    l = listing.delay()
    return {'list': json.dumps(l)}, 200


# RECREATING THE KEYS : key.from_string(string_key, curve)
def serialize(key):
    key = key.to_string().decode('latin1')
    return key


if __name__ == '__main__':
    app.run(debug=True)
