import socket
import serial
import json
import http.client, urllib.parse

def sendDisplayText(displayMsg, ser):
	try:
		print("sendDisplayText called")
		msgToSend = "#D%s@" % displayMsg
		print("msg to send - %s" % msgToSend )
		ser.write(bytes(msgToSend, 'UTF-8'))
	except ValueError as e:
		print("ValueError: {0}".format(e.strerror))
	except TypeError as e:
		print("TypeError: {0}".format(e.strerror))
	
def sendDisplayMsg(cmdData, ser):
	try:
		print("sendDisplayMsg called")
		sendDisplayText( cmdData['msg'], ser)
	except ValueError as e:
		print("ValueError: {0}".format(e.strerror))
	except KeyError as e:
		print("KeyError: {0}".format(e.strerror))
	except TypeError as e:
		print("TypeError: {0}".format(e.strerror))
	
def sendSetSpeedMsg(cmdData, ser):
	try:
		#print("sendSetSpeedMsg called")
		leftSpeed = cmdData['leftSpeed']
		
		leftDirection = 'F'
		if(leftSpeed < 0):
			leftDirection = 'R'
			leftSpeed = leftSpeed * -1
		leftSpeed = leftSpeed * 2
		if(leftSpeed > 255):
			leftSpeed = 255

		rightSpeed = cmdData['rightSpeed']
		
		rightDirection = 'F'
		if(rightSpeed < 0):
			rightDirection = 'R'
			rightSpeed = rightSpeed * -1
		rightSpeed = rightSpeed * 2
		if(rightSpeed > 255):
			rightSpeed = 255
		
		msgToSend = "#S%c%03d%c%03d@" % (leftDirection, leftSpeed, rightDirection, rightSpeed)
		print("msg to send - %s" % msgToSend)
		ser.write(bytes(msgToSend, 'UTF-8'))
	except ValueError as e:
		print("ValueError: {0}".format(e.strerror))
	except KeyError as e:
		print("KeyError: {0}".format(e.strerror))
	except TypeError as e:
		print("TypeError: {0}".format(e.strerror))
	
	
def main():

	ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
	#ser = serial.Serial('/dev/tty1', 9600, timeout=1)

	print ("connecting to google ...")
	sendDisplayText("CONNECTING TO GOOGLE",ser)

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com", 80))
	local_address = s.getsockname()[0]
	s.close()
	print("local address is %s" % local_address)
	sendDisplayText("IP %s" % local_address,ser)

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
	sendDisplayText("STARTING SERVICE",ser)

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	my_socket.bind(('', 8881))

	print ("start service ...")

	while True :
		message = my_socket.recv(8192)
		#print ("message (%s) from : %s" % (str(message), address[0]))
		stringdata = message.decode('utf-8')
		#print(stringdata)
		#print("parsing")
		try:
			decoded = json.loads(stringdata)
			# pretty printing of json-formatted string
			#print (json.dumps(decoded, sort_keys=True, indent=4))
			if(decoded['cmd'] == 'setSpeed'):
				#print("this is a setSpeed cmd")
				sendSetSpeedMsg(decoded, ser)
			elif(decoded['cmd'] == 'displayMsg'):
				#print("this is a displayMsg cmd")
				sendDisplayMsg(decoded, ser)
			else:
				print("unknown cmd")
		except ValueError as e:
			print("ValueError: {0}".format(e.strerror))
		except KeyError as e:
			print("KeyError: {0}".format(e.strerror))
		except TypeError as e:
			print("TypeError: {0}".format(e.strerror))

if __name__ == "__main__" :
	main()
