import requests

BASE_URL = "0.0.0.0"
def connection_ok(baseUrl):
	"""Check whetcher connection is ok

	Post a request to server, if connection ok, server will return http response 'ok' 

	Args:
		none

	Returns:
		if connection ok, return True
		if connection not ok, return False
	
	Raises:
		none
	"""
	global BASE_URL
	BASE_URL = baseUrl
	cmd = 'connection_test'
	url = baseUrl + cmd + "/"
	print('url: %s'% url)
	# if server find there is 'connection_test' in request url, server will response 'Ok'
	try:
		r=requests.get(url)
		if r.text == 'OK':
			return True
	except:
		return False

def __request__(url, times=10):
	for x in range(times):
		try:
			requests.get(url)
			return 0
		except :
			print("Connection error, try again")
	print("Abort")
	return -1

def run_action(cmd):
	"""Ask server to do sth, use in running mode

	Post requests to server, server will do what client want to do according to the url.
	This function for running mode

	Args:
		# ============== Back wheels =============
		'bwready' | 'forward' | 'backward' | 'stop'

		# ============== Front wheels =============
		'fwready' | 'fwleft' | 'fwright' |  'fwstraight'  |  'fwturn:{angle}'

		# ================ Camera =================
		'camready' | 'camleft' | 'camright' | 'camup' | 'camdown'
	"""
	# set the url include action information
	url = BASE_URL + 'run/?action=' + cmd
	print('url: %s'% url)
	# post request with url 
	__request__(url)

def run_speed(speed):
	"""Ask server to set speed, use in running mode

	Post requests to server, server will set speed according to the url.
	This function for running mode.

	Args:
		'0'~'100'
	"""
	# Set set-speed url
	url = BASE_URL + 'run/?speed=' + str(speed)
	print('url: %s'% url)
	# Set speed
	__request__(url)