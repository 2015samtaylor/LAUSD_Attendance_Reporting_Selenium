from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
import json
import re
import xml.etree.ElementTree as ET
import warnings
import cx_Oracle
import pandas as pd

class api:
	# API constructor
	def __init__(self, base_url=None, client_id=None, client_secret=None, access_token=None, credential_file=None, plugin=None):
		if not base_url:
			raise RuntimeError('base_url is required')

		# Set the base_url.  Scrub out protocol and trailing slash if present
		self._base_url = base_url
		self._base_url = re.sub( r"^https?:\/\/", "", self._base_url)
		self._base_url = re.sub( r"\/+$", "", self._base_url)

		# Initialize API creds with values passed into constructor
		self._client_id = client_id
		self._client_secret = client_secret
		self._access_token = access_token

		# Check for credential_file.  If exists, read it and set values.
		self._credential_file = credential_file
		if self._credential_file:
			with open(self._credential_file, 'r') as f:
				config = json.load(f)

			if 'client_id' in config: self._client_id = config['client_id']
			if 'client_secret' in config: self._client_secret = config['client_secret']
			if 'access_token' in config: self._access_token = config['access_token']

		# Check for plugin.  If exists, read it from keyring and set values.
		self._plugin = plugin
		if self._plugin:
			import keyring

			# Set default blank values for creds
			keyring_creds = {
				"client_id": None,
				"client_secret": None,
				"access_token": None
			}

			# Try to update the blank creds with values from keyring
			try:
				keyring_creds.update( json.loads( keyring.get_password( self._base_url, self._plugin) ) )
			except:
				pass

			# Prompt for client_id if not defined
			if not keyring_creds['client_id'] or not keyring_creds['client_secret']:
				import getpass

				# Prompt for client_id if not defined
				while not keyring_creds['client_id']:
					keyring_creds['client_id'] = getpass.getpass( f"No client_id found for plugin {self._plugin} on {self._base_url}.  Please enter: ")

				# Prompt for client_secret if not defined
				while not keyring_creds['client_secret']:
					keyring_creds['client_secret'] = getpass.getpass( f"No client_secret found for plugin {self._plugin} on {self._base_url}.  Please enter: ")

				keyring.set_password( self._base_url, self._plugin, json.dumps(keyring_creds))

			# Set client_id, client_secret, and access_token
			self._client_id = keyring_creds['client_id']
			self._client_secret = keyring_creds['client_secret']
			self._access_token = keyring_creds['access_token']

		# Check for combination of client_id and client_secret or just an access_token
		if not ( (self._client_id and self._client_id) or (self._access_token) ):
			raise RuntimeError('One of the following required: (client_id and client_secret) or access_token')

		# Create session
		self.session = OAuth2Session(
			client=BackendApplicationClient(client_id=self._client_id),
			token={
				"token_type": "Bearer",
				"access_token": self._access_token
			}
		)

		# Set default headers for use with humans
		self.session.headers = {"Content-Type": "application/json", "Accept": "application/json"}

		# If access_token was not provided, obtain one.
		if not self._access_token:
			self._obtain_access_token()

	# Internal method for obtaining a bearer token using API credentials
	def _obtain_access_token(self):
		# Raise an error if either the client_id or client_secret was not defined
		if not (self._client_id and self._client_secret):
			raise RuntimeError('Tried to obtain a bearer token but missing a client_id or client_secret')

		# Fetch the access_token
		response = self.session.fetch_token(token_url=f'https://{self._base_url}/oauth/access_token', auth=HTTPBasicAuth(self._client_id, self._client_secret))

		# Set the access_token
		self._access_token = response['access_token']

		if self._credential_file:
			with open(self._credential_file, 'r') as f:
				config = json.load(f)

			config['access_token'] = self._access_token

			with open(self._credential_file, 'w') as f:
				json.dump(config, f, indent=4)

		if self._plugin:
			import keyring

			keyring.set_password( self._base_url, self._plugin, json.dumps({
				"client_id": self._client_id,
				"client_secret": self._client_secret,
				"access_token": self._access_token
			}))

	# General method for making API requests
	def request(self, url, method, **kwargs):
		# Strip schema and base_url
		url = re.sub( f"^(https?:\/\/)?{self._base_url}", "", url )

		# Strip leading slashes
		url = url.lstrip("/")

		# Make the request
		response = self.session.request( url=f"https://{self._base_url}/{url}", method=method, **kwargs )

		if response.status_code == 200:
			# 200 OK
			# Return response
			return response

		elif response.status_code == 401:
			# 401 Unauthorized

			# Trying to access an endpoint that is not available to plugins
			if "Must be logged in" in response.text:
				raise RuntimeError( response.text )
			# Otherwise probably an expired or invalid bearer token
			else:
				self._obtain_access_token()
				response = self.request( url=url, method=method, **kwargs)

		elif response.status_code == 403:
			# 403 Forbidden
			# Missing access to one or more fields.  Warn and compile a list of needed access_requests.

			# Inialize list of needed access_requests
			access_requests = []

			try:
				# Parse JSON or XML into list of fields
				if response.headers['Content-Type'] == "application/json":
					for error in response.json()['errors']:
						access_requests.append( error['field'] )
				if response.headers['Content-Type'] == "application/xml":
					tree = ET.ElementTree(ET.fromstring(response.text))
					root = tree.getroot()
					for field in root.findall("./errors/field"):
						access_requests.append( field.text )
				# Create XML tags to obtain access to these fields
				access_requests = sorted([ '<field table="{}" field="{}" access="ViewOnly" />'.format( *field.split(".") ) for field in access_requests ])

				# Warn with needed requests
				warnings.warn( f"No access to field. access_requests: {''.join(access_requests)}", PowerSchoolWarning)
			except:
				pass

			response.access_requests = access_requests

		return response

	# Shortcut methods for common verbs
	def get(self, url, **kwargs):
		return self.request( url=url, method='get', **kwargs )

	def post(self, url, **kwargs):
		return self.request( url=url, method='post', **kwargs )

	def put(self, url, **kwargs):
		return self.request( url=url, method='put', **kwargs )

	def delete(self, url, **kwargs):
		return self.request( url=url, method='delete', **kwargs )

	# API destructor
	def __del__(self):
		self.session.close()

# Define custom warning class
class PowerSchoolWarning(Warning):
	pass

# ODBC connection function
def odbc(self, server="", user="", password="", port=1521, database="psproddb", connectionstring=None):

	# Raise error if missing minimum arguments
	if not ( (server and user) or connectionstring ):
		raise RuntimeError("Must provide server and user or full connectionstring")

	# If connectionstring was not provided, build one
	if not connectionstring:
		# If no password was provided, retrieve it from keyring
		if not password:
			import keyring

			# Retrieve
			password = keyring.get_password( server, user )

			# If no password existed in keyring, obtain it from the user
			if not password:
				import getpass

				# Repeat until a password is proviced
				while not password:
					password = getpass.getpass( f"No password found for user {user}.  Please enter: ")

					# Set the password in keyring for future use
					keyring.set_password( server, user, password )

		# Build the connectionstring
		connectionstring = f"{user}/{password}@{server}:{port}/{database}"

	# Return the connection object
	return cx_Oracle.connect( connectionstring )