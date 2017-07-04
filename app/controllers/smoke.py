# @ant4g0nist

import os
import json
import yaml
import numpy
import random
import requests
import itertools
from ..helpers.constants import *
from ..helpers.helper import Generator
from ..helpers.utils import TerminalColors

tty_colors = TerminalColors(True)

class SusanooConfig:
	def __init__(self, config):
		config 						= open(config,'r')
		self.config 				= yaml.load(config)
		self.host   				= self.config['host']
		self.headers_yaml 			= self.config['headers']
		self.generator 				= Generator()
		self.userA_Authorization  	= self.config['UserA_Authorization']
		self.userB_Authorization  	= self.config['UserB_Authorization']		
		self.headers 				= {'User-Agent': 'mozilla/5.0 (iphone; cpu iphone os 7_0_2 like mac os x) applewebkit/537.51.1 (khtml, like gecko) version/7.0 mobile/11a501 safari/9537.5', 'Accept': 'application/json', 'Content-Type':'application/x-www-form-urlencoded'}

		self.set_headers()

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
			print e
			api_request_error_handler(api)
			return None

class API:
	def __init__(self, args, host):
		self.host 		= host
		self.args 		= args
		self.generator 	= Generator()
		self.name 		= self.args['name']

		if "headers" in self.args.keys():
			self.headers    		= self.args['headers'] 

		self.status_code = self.args['status_code']
		self.raw_url 	= None
		self.api 		= self.args['api']
		self.method 	= self.args['method']
		self.inputs     = {}
		self.outputs	= args.setdefault('outputs', {})
		self.url_inputs = []


		# def set_url_inputs()
		if 'inputs' in self.args.keys():
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

			self.inputs 	= self.generator.generate_inputs(self.args)
		
class Scans:
	def __init__(self, api, susanoo):
		self.susanoo 				= susanoo
		self.headers 			 	= self.susanoo.headers
		self.url_inputs				= api.url_inputs
		self.url 				 	= susanoo.host+api.api

		try:
			self.raw_url				= susanoo.host+api.raw_url
		except:
			self.raw_url	=	None

		self.outputs				= api.outputs
		self.status_code			= api.status_code
		self.method  			 	= api.method
		self.params  			 	= api.inputs
		self.name   				= api.name
		self.authorization_header 	= susanoo.userA_Authorization

	def run(self):
		self.orig_request = APIRequest()
		self.orig_resp 	  = self.orig_request.run(self.url, self.method, self.params, self.headers)

		if self.orig_resp:
			if self.orig_resp.status_code>=500:
				handle500(self.url, self.method, self.params)
				return

			elif self.orig_resp.status_code==self.status_code:
				try:
				    json_output = self.orig_resp.json()
				except ValueError:
				    api_request_error_handler(self.url)
				    return

				outputs = {}
				for output in self.outputs:
					if "json_extract" in self.outputs[output].keys():
						value 	= eval(self.outputs[output]['json_extract'])(json_output)
						if not value:
							continue

						if self.outputs[output]["value"] in value:
							print tty_colors.green()+'Smoke scan for api: %s success. Given value of output found in api response.'%(self.name)+tty_colors.default()

						else:
							print tty_colors.red()+'Smoke scan for api: %s failed. Given value of output was not found in api response.'%(self.name)+tty_colors.default()

					if "list_extract" in self.outputs[output].keys():
						
						value 	= map(eval(self.outputs[output]['list_extract']),json_output)
						
						if not value:
							continue

						if self.outputs[output]["value"] in value:
							print tty_colors.green()+'Smoke scan for api: %s success. Given value of output found in api response.'%(self.name)+tty_colors.default()

						else:
							print tty_colors.red()+'Smoke scan for api: %s failed. Given value of output was not found in api response.'%(self.name)+tty_colors.default()
		else:
			# handle500(self.url, self.method, self.params)
			unexpected_status_code(self.url, self.method, self.params, self.orig_resp.status_code)
			return 

def api_request_error_handler(api):
	print tty_colors.blue()+'There was an error trying to request %s '%(api)+tty_colors.default()

def handle500(api, method, params):
	print tty_colors.red()+'%s is throwing 500 with following params for method %s'%(api, method)
	print tty_colors.blue()+'%s'%json.dumps(params)+tty_colors.default()

def unexpected_status_code(api, method, params, status_code):
	print tty_colors.red()+'%s is giving %s with following params for method %s'%(api, status_code, method)
	if params:
		print tty_colors.blue()+'%s'%json.dumps(params)+tty_colors.default()
