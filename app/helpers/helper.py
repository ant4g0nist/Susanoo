# @ant4g0nist

import os
import uuid
import string
import struct
import random
import constants

class Generator(object):
	"""
		Class to generate random inputs
	"""
	def __init__(self):
		seed = os.urandom(10)
		random.seed(seed)

	def generate_inputs(self, input_description):
		"""
			Generate inputs
		""" 
		call_params = {}

		def walk_inputs(data_set, params, parent_key=None, type_=None):
		    if isinstance(data_set, dict):
			    for input_name, value in data_set.items():
			        if 'type' not in value:
			            type_ = type(value)
			            
			            parent_key = input_name
			            params[parent_key] = []	

			            inputs = walk_inputs(value, {}, parent_key, type_)
			            if inputs:
			            	if type_==dict:
				                params[input_name] = inputs
			            	elif type_==list:
				            	
				            	params[parent_key].append(inputs)
			            continue

			        if 'required' in value or self.once_every(5):
			            
			            resource_name = None

			            if value['type'] in ('resource', 'list_resource'):
			                resource_name = value.setdefault('resource_name', input_name)
			            if "value" in value.keys():
				            new_input = self.generate_input(value['type'], resource_name, value["value"])
			            else:
				        	new_input = self.generate_input(value['type'], resource_name)
			            if "expand" in value and isinstance(new_input, dict):
			                for k, value in new_input.items():
			                    params[k] = value
			            else:
			                params[input_name] = new_input
			    return params

		    elif isinstance(data_set, list):
				# print data_set
				for i in data_set:
					inputs = walk_inputs(i, params, parent_key, list)
					if parent_key in params.keys():
						if inputs:
							params[parent_key].append(inputs)

				return params		

		walk_inputs(input_description, call_params, type_=dict)
		
		return call_params


	def generate_input(self, input_type=None, resource_name=None, value=None):

	    # Check if it's a list
	    if value:
	    	result = value
	    	return result

	    is_list = False
	    if input_type.startswith('list_'):
	        is_list = True
	        input_type = input_type[5:]

	    if is_list:
	        result = []
	        for i in xrange(0, random.randint(0, 5)):
	            result.append(self.generate(input_type, resource_name))
	    else:
	        result = self.generate(input_type, resource_name)
	    return result

	def generate(self, input_type, resource_name=None):
		if 'hex-' in input_type:
			size = int(input_type.replace('hex-',""))

			generator = self.__getattribute__("gen_hex")    
			return generator(size)

		elif 'int-' in input_type:
			size = int(input_type.replace('int-',""))
			generator = self.__getattribute__("gen_int")    
			return generator(size)

		generator = self.__getattribute__("gen_%s" % input_type)
		
		return generator()

	def gen_hex(self, size):
		hex = os.urandom(size/2).encode('hex')
		return hex[:size]

	def gen_int(self, size):
		def random_range(n):
			range_start = 10**(n-1)
			range_end = (10**n)-1
			return random.randint(range_start, range_end)
		return random_range(size)

	def gen_unicode(self):
	    chunk = []
	    for i in xrange(random.randint(1, 128)):
	        chunk.append(struct.pack("f", random.random()))
	    return unicode("".join(chunk), errors='ignore')

	def gen_ascii(self):
	    return ''.join(random.choice(string.letters + string.digits) for _ in range(random.randint(1, 512)))

	def gen_string(self):
		if random.randint(0,1):
			return self.gen_unicode()
		    
		if random.randint(0,1):
			return self.gen_ascii()
			
		return random.choice(constants.PAYLOADS)

	def gen_email(self):
		return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))+"@gmail.com"

	def gen_username(self):
		return ''.join(random.choice(string.ascii_lowercase + string.digits+"_") for _ in range(10))
	
	def gen_latlng(self, seprator=","):
		return str(random.uniform(-180,180))+seprator+str(random.uniform(-90, 90))

	def gen_uuid(self):
		return str(uuid.uuid1())