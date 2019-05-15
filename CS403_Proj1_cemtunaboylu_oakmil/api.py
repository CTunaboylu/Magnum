import requests, sys
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from typing import Dict, List
from threading import Thread
from ecdsa import VerifyingKey
import multiprocessing

from celery import Celery
from celery.result import AsyncResult

_DEBUG = True
_trial = True

API_URL = 'http://127.0.0.1:5000'
PORT = '5000'
network = dict()
endpoint = ''

app = Flask(__name__)

"""
app.config.update(
    CELERY_BROKER_URL=API_URL,
    CELERY_RESULT_BACKEND='db+sqlite:///network.db'
)

def make_celery(app):
	
	Require for Flask context, skip it

	c = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
	c.conf.update(app.config)
	TaskBase = c.Task

	class ContextTask(TaskBase):
		abstract = True
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)
	c.Task = ContextTask
	return c


celery = make_celery(app)

"""
api = Api(app)

#@celery.task(name='registration')
def registration(ip, ver_key):
		global network
		ver = ver_key.encode('latin1')
		ver = VerifyingKey.from_string(ver, curve=NIST256p)
		network[ip] = ver
		return {'message': 'OK'}, 201 # 201 to indicate it is created
#@celery.task(name='here_is_the_key')
def here_is_the_key(ip:str):
	global network
	key = serialize(network[ip])
	return {'requested_verifying_key' : key }

#@celery.task(name='listing')
def listing(ip:str):
	global network
	return {'list' : network }

	
@app.route('/join/<data>', methods = ['POST'])
def join(data):
	#data = (request.get_json())
	print(data)
	p1 = multiprocessing.Process(target=registration, args=(request.remote_addr, request.args.get('verifying_key')))
	p1.start()

	return {'msg': 'Will be registered in the network in a short time.'}, 201
@app.route('/ver_key/<ip>', methods = ['GET'])
def ver_key(ip):
	if _DEBUG:
		print(ip)
	k = here_is_the_key(ip)
	return {'request_verifying_key':k}, 200


@app.route('/list', methods = ['GET'])
def list():
	if _DEBUG:
		print('Requested the network list')
	l = listing.delay()
	return {'list': json.dumps(l)}, 200

# RECREATING THE KEYS : key.from_string(string_key, curve)

	
def serialize(key):
	key = key.to_string().decode('latin1')
	return key
		


endpoint = '{}/'.format(API_URL)



if __name__ == '__main__':
	app.run(debug = True)

