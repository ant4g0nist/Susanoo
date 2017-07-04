Susanoo:
=================================================

	Susanoo is a REST API security testing framework. 

##	Features

- Configurable inputs/outputs formats
- API Vulnerability Scan: Normal scanning engine that scans for IDOR, Authentication issues, SQL injections, Error stacks.
- Smoke Scan: Custom output checks for known pocs can be configured to run daily.

## Types of Scans:
	* API Vulnerability Scan
		**  Scans for following bugs:
			***   Indirect Object References
			***   Authentication issues
			***   SQL injections
			***   Error stacks

	* Smoke Scan
		**  A known Proof-of-concept can be configured to run daily/weekly etc.
		

## Configuration:
 
	Susanoo takes yaml files in configuration. Please check the examples folder for sample configuration files.


##	Parameter Types:
~~~
	resource --> static
		Eg: In the following example the value "password" is used for grant_type:

			password: {"type":"resource", "required":True, "value":"p@ssw0rd"}

	hex-n:
		Generate hex of length n.
			Eg: a hex value of length 16 is generated for uniqueId in below example:

				id: {'type':'hex-16', 'required': True} 

	int-n:
		Generates int of size n
			Eg: a int value of size 4 is generated for uniqueId in below example:
			
				bonus: {'type':'int-4', 'required':'True'}

	email:
		Generates random email id
			Eg: a random email id is generated and assigned for email_id

				email_id: {"type":"email", "required":True}

	username:
		Generates random username
			Eg: a random username is generated and assigned for username

				username: {"type":"username", "required":True}

	string:
		Generates random strings
			Eg: generates random strings of variable length.

				string: {"type":"string", "required":True}

~~~

## Donation:

If you like the project, you can buy me beers :) 

[![Donate Bitcoin](https://img.shields.io/badge/donate-bitcoin-green.svg)](https://ant4g0nist.github.io)


## Installation:

	^^/D/projects >>> git clone https://github.com/ant4g0nist/susanoo
	^^/D/projects >>> cd susanoo
    ^^/D/p/susanoo >>> sudo pip install -r requirements.txt

## Usage:
	
	^^/D/p/susanoo >>> cd db
	^^/D/p/s/db >>> sudo mongod --dbpath . --bind_ip=127.0.0.1	

	^^/D/p/susanoo >>> python susanoo.py


##	TODO:

- [ ] Use celery/scheduler to schedule the scans
- [ ] Chain apis together? pickup value from one api and use in another
- [ ] Add more vulnerability checks
- [ ] Make it more reliable
- [ ] Parallelize scans using Celery
- [ ] Add better reporting

## Thanks:

- Go-Jek Security Team
- [restfuzz](https://github.com/redhat-cip/restfuzz)