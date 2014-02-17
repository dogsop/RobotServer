import socket
import json
import http.client, urllib.parse

def main():

	print ("connecting to google ...")

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com", 80))
	local_address = s.getsockname()[0]
	s.close()
	print("local address is %s" % local_address)

	print ("posting to gateway.smellydog.net ...")
	
	params = urllib.parse.urlencode({'id': 9345, 'action': 'update', 'robotIpAddress': local_address, 'robotWebPort': 9000, 'robotControlPort': 8881})
	
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	
	conn = http.client.HTTPSConnection("gateway.smellydog.net")
	conn.request("POST", "/robot/index.php", params, headers)
	response = conn.getresponse()
	print(response.status, response.reason)
	data = response.read()
	print(data)
	conn.close()

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	my_socket.bind(('', 8881))

	print ("start service ...")

	while True :
		message = my_socket.recv(8192)
		#print ("message (%s) from : %s" % (str(message), address[0]))
		stringdata = message.decode('utf-8')
		print(stringdata)
		print("parsing")
		try:
			decoded = json.loads(stringdata)
			# pretty printing of json-formatted string
			#print (json.dumps(decoded, sort_keys=True, indent=4))
			if(decoded['cmd'] == 'setSpeed'):
				print("this is a setSpeed cmd")
			elif(decoded['cmd'] == 'displayMsg'):
				print("this is a displayMsg cmd")
			else:
				print("unknown cmd")
		except (ValueError, KeyError, TypeError):
			print ("JSON format error")

if __name__ == "__main__" :
	main()
