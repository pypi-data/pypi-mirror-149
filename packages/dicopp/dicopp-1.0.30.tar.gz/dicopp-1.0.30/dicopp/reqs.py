import requests
import random

from . import com

url = "http://localhost:3121"
jsonrpcversion="2.0"

def req(a):
	payload = {
		"id" : random.randint(0,(2**16)-1),
		"jsonrpc" : jsonrpcversion,
		"method" : a,
		"version" : jsonrpcversion
	}
	return incom(payload)
def requ(a,para):
	payload = {
		"id" : random.randint(0,(2**16)-1),
		"jsonrpc" : jsonrpcversion,
		"method" : a,
		"version" : jsonrpcversion,
		"params" : para
	}
	incom(payload)
def reque(a,para):
	payload = {
		"id" : random.randint(0,(2**16)-1),
		"jsonrpc" : jsonrpcversion,
		"method" : a,
		"version" : jsonrpcversion,
		"params" : para
	}
	return incom(payload)

def incom(payload):
	response = requests.post(url, json=payload).json()
	com.post(response)
	return response['result']

def reque_simple(a,para):
	payload = {
		"id" : random.randint(0,(2**16)-1),
		"jsonrpc" : jsonrpcversion,
		"method" : a,
		"version" : jsonrpcversion,
		"params" : para
	}
	return requests.post(url, json=payload).json()