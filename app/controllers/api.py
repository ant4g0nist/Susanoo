# @ant4g0nist

import os
import json
import time
import uuid
import yaml
import numpy
import random
import hashlib
import requests
import itertools
from ..helpers.constants import *
from ..models import Scan as ScanModel
from ..helpers.helper import Generator
from ..helpers.utils import TerminalColors

tty_colors = TerminalColors(True)

class SusanooConfig:
	def __init__(self, config):
		config 						= open(config,'r')
		self.scanId					= str(uuid.uuid1())
		self.config 				= yaml.load(config)
		self.hash					= getHash(config.read())
		self.host   				= self.config['host']
		self.userA_Authorization  	= self.config['UserA_Authorization']
		self.userB_Authorization  	= self.config['UserB_Authorization']
		self.headers_yaml 			= self.config['headers']

		self.generator 				= Generator()

		self.headers 				= {'User-Agent': 'mozilla/5.0 (iphone; cpu iphone os 7_0_2 like mac os x) applewebkit/537.51.1 (khtml, like gecko) version/7.0 mobile/11a501 safari/9537.5', 'Accept': 'application/json', 'Content-Type':'application/x-www-form-urlencoded'}

		self.set_headers()

		#save to db
		apiscan  = ScanModel.APIScanResults(scanId=self.scanId, hash=self.hash, updatedTime=time.strftime("%Y.%m.%d %H:%M:%S"), config=config.read().encode('hex'))
		apiscan.save()

	def set_headers(self, userB=None):
		headers = {}
		for i in self.headers_yaml:
			name 		  = i["name"]
			value 		  = i["value"]
			values 		  = self.generator.generate_inputs(i["inputs"])
			for k,v in values.items():
				headers[name]  = value.replace("%%(%s)"%k,v)

		for i in headers:
			self.headers[i] = headers[i]

		
		if not userB:
			for i in self.userA_Authorization:
				name  = i['name']
				value = i['value']

				self.headers[name] = value
		else:
			for i in self.userB_Authorization:
				name  = i['name']
				value = i['value']

				self.headers[name] = value

		
	def get_apis(self):
		self.apis = {}

		for api in self.config['apis']:
			apic = API(api, self.host)
			self.apis[api['name']] = apic

		return self.apis

class APIRequest:
	def __init__(self):
		pass

	def run(self, api, method, params, headers):

		try:
			return requests.request(method, url=api, headers=headers, data=params)
		except Exception as e:
			api_request_error_handler(api)
			return None

class API:
	def __init__(self, args, host):
		self.host 		= host
		self.args 		= args
		self.generator 	= Generator()
		self.name 		= self.args['name']
		self.raw_url 	= None
		self.api 		= self.args['api']
		self.method 	= self.args['method']
		self.inputs     = {}
		self.url_inputs = []

		# def set_url_inputs()
		if 'inputs' in self.args.keys() and self.args['inputs']:
			if 'url_input' in self.args['inputs']:
				url_inputs = dict(self.args['inputs']['url_input'])
				self.url_inputs.append(url_inputs)
				url = self.api
				self.raw_url = self.api	
				for j in url_inputs:
					input_name = j
					type_ 	   = url_inputs[j]['type']
					value	   = str(self.generator.generate(type_))
					url 	   = url.replace("%%(%s)"%input_name, value)

				self.api = url
				del self.args['inputs']['url_input']
			

			# print self.args["inputs"]
			self.inputs 	= self.generator.generate_inputs(self.args["inputs"])
			print self.inputs

class Scans:
	def __init__(self, api, susanoo):
		self.susanoo 				= susanoo
		self.scanId					= self.susanoo.scanId
		self.hash					= self.susanoo.hash
		self.headers 			 	= self.susanoo.headers
		self.url_inputs				= api.url_inputs
		self.url 				 	= susanoo.host+api.api
		try:
			self.raw_url				= susanoo.host+api.raw_url
		except:
			self.raw_url	=	None
		self.method  			 	= api.method
		self.params  			 	= api.inputs
		self.name   				= api.name
		self.authorization_header 	= susanoo.userA_Authorization


		self.orig_request = APIRequest()
		self.orig_resp 	  = self.orig_request.run(self.url, self.method, self.params, self.headers)


	def authentication_check(self):

		headers = dict(self.headers)

		# check 1: with empty authorization header
		for i in self.authorization_header:
			# orignal request
			del headers[i['name']]	

		fuzz_request = APIRequest()
		fuzz_resp 	 = fuzz_request.run(self.url, self.method, self.params, headers)
		
		vuln = False
		if fuzz_resp:
			# check if fuzz_resp gives 401
			if fuzz_resp.status_code==401:
				vuln = True
				print tty_colors.green()+'%s api is authenticated'%self.name+tty_colors.default()

			elif fuzz_resp.status_code==200:	
				if self.orig_resp.text == fuzz_resp.text:
					vuln = True
					print tty_colors.red()+'holy cow, %s api is unauthenticated'%self.name+tty_colors.default()

		# check 2: with random header
		headers = self.susanoo.generator.generate_inputs(self.susanoo.headers_yaml)

		fuzz_request = APIRequest()
		fuzz_resp 	 = fuzz_request.run(self.url, self.method, self.params, headers)

		if fuzz_resp:
			if fuzz_resp.status_code==401:
				vuln = True
				print tty_colors.green()+'%s api is authenticated'%self.name+tty_colors.default()

			elif fuzz_resp.status_code>=500:
				handle500(self.url, self.method, self.params)

			elif fuzz_resp.status_code==200:	
				if self.orig_resp.text == fuzz_resp.text:
					vuln = True
					print tty_colors.red()+'holy cow, %s api is unauthenticated'%self.name+tty_colors.default()

		if vuln:
			self.save_to_db("unauthenticated", self.url, self.headers, self.method, self.params)

	def authorization_check(self):
		headers_a = dict(self.headers)

		self.susanoo.set_headers(1)

		headers_b = self.susanoo.headers

		fuzz_request = APIRequest()
		fuzz_resp 	 = fuzz_request.run(self.url, self.method, self.params, headers_b)

		vuln = False
		if fuzz_resp:
			# check if fuzz_resp gives 401
			if fuzz_resp.status_code==401:
				vuln = True
				print tty_colors.green()+'%s api is authorized'%self.name+tty_colors.default()

			elif fuzz_resp.status_code>=500:
				handle500(self.url, self.method, self.params)

			elif fuzz_resp.status_code==200:
				if self.orig_resp.text == fuzz_resp.text:
					vuln = True
					print tty_colors.red()+'holy cow, %s api is unauthorized'%self.name+tty_colors.default()

		self.susanoo.set_headers(0)

		if vuln:
			self.save_to_db("unauthorized", self.url, self.headers, self.method, self.params)

	def sqlinjection_heuristic_check(self):
		sql_injection_found = False
		
		for payload in HEURISTIC_CHECK_ALPHABET:

			params = dict(self.params)

			for param in params:
				request_params = dict(params)
				request_params[param] = "%s%s"%(request_params[param],payload)

				fuzz_request = APIRequest()
				fuzz_resp 	 = fuzz_request.run(self.url, self.method, request_params, self.headers)

				vuln = False
				if fuzz_resp:
					if any(i in fuzz_resp.text for i in FORMAT_EXCEPTION_STRINGS) and not any(i in self.orig_resp.text for i in FORMAT_EXCEPTION_STRINGS):
						vuln = True
						print tty_colors.red()+'server error in %s api'%self.name+tty_colors.default()
						print tty_colors.green()+"poc: %s"%json.dumps(params)+tty_colors.default()
						sql_injection_found = True

				if vuln:
					self.save_to_db("possible SQLi", self.url, self.headers, self.method, request_params, param)

		if not sql_injection_found:
			print tty_colors.green()+'heuristic checks for sql injection failed to find sqli for %s api'%self.name+tty_colors.default()

	def ratelimit_check(self):
		rate_limit = False
		count = 0
		while count<30:
			if not rate_limit:
				fuzz_request = APIRequest()
				fuzz_resp 	 = fuzz_request.run(self.url, self.method, self.params, self.headers)

				if any(i in fuzz_resp.text for i in RATE_LIMIT_STRINGS) and not any(i in self.orig_resp.text for i in RATE_LIMIT_STRINGS):
					print tty_colors.green()+"api: %s seems rate limited."%self.name+tty_colors.default()
					rate_limit = True
					break

			count+=1

		if not rate_limit:
			print tty_colors.red()+"api: %s is not properly rate limited."%self.name+tty_colors.default()
			self.save_to_db("rate limiting", self.url, self.headers, self.method, self.params)
			

	def fuzz(self):
		print tty_colors.red()+"[:Fuzz:] Not yet Implemented"+tty_colors.default()
		return

	def url_param_fuzz(self):
		url = self.raw_url
		count=10
		while count>0:
			for input in self.url_inputs:
				url = self.raw_url
				
				for j in input:
					input_name = j
					type_ 	   = input[j]['type']
					value	   = str(self.susanoo.generator.generate(type_)) + self.susanoo.generator.gen_unicode()
					url 	   = url.replace("%%(%s)"%input_name, value)

					fuzz_request = APIRequest()
					fuzz_resp 	  = self.orig_request.run(url, self.method, self.params, self.headers)

					vuln = False
					if fuzz_resp:
						print tty_colors.cyan()+"*"*100+tty_colors.default()

						if any(i in fuzz_resp.text for i in FORMAT_EXCEPTION_STRINGS) and not any(i in self.orig_resp.text for i in FORMAT_EXCEPTION_STRINGS):
							vuln = True
							print tty_colors.red()+'server error in %s api'%self.name+tty_colors.default()
							print tty_colors.green()+"poc %s"%json.dumps(url)+tty_colors.default()
							server_error_stack = True

					if vuln:
						self.save_to_db("Server Error Trace", url, self.headers, self.method, self.params, input_name)

			count-=1

	def save_to_db(self, vuln, api, headers, method, parameters, param=None):

		authApiScanResults = ScanModel.APIScanResults.objects(scanId=self.scanId)

		if authApiScanResults:
			authApiScanResults=authApiScanResults[0]
			apiscan = ScanModel.APIScan(api=api, headers=json.dumps(headers), parameters=json.dumps(parameters), method=method, vulnerability=vuln, scanId=self.scanId, updatedTime=time.strftime("%Y.%m.%d %H:%M:%S"), parameter=param)
			apiscan.save()

			authApiScanResults.apiscans.append(apiscan)
			authApiScanResults.save()

def api_request_error_handler(api):
	print tty_colors.blue()+'There was an error trying to request %s '%(api)+tty_colors.default()

def handle500(api, method, params):
	print tty_colors.red()+'%s is throwing 500 with following params for method %s'%(api, method)
	print tty_colors.blue()+'%s'%json.dumps(params)+tty_colors.default()

def getHash(config):
	m = hashlib.sha256()
	m.update(config)
	return m.hexdigest()
