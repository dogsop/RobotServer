import socket


def main():

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	local_address = s.getsockname()[0]
	s.close()
	print("local address is %s" % local_address)

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	my_socket.bind(('',8881))

	print ("start service ...")

	while True :
		message , address = my_socket.recvfrom(8192)
		print ("message (%s) from : %s" % ( str(message), address[0]))
		parsed_message = message.decode("utf-8").split('|')
		if(len(parsed_message) < 3):
			print ("bad message")
		else:
			for index, item in enumerate(parsed_message):
				print (index, item )

if __name__ == "__main__" :
    main()
