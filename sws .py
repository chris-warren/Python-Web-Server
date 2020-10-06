#line for testing
#nc 10.10.1.100 1234 <swstestinput.txt
#GET test.txt HTTP/1.0
#Connection: keep-alive



import socket
import sys
import datetime
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '10.10.1.100'
#sys.argv[0]
port = 1234
#sys.argv[1]

s.bind((ip, port))
s.listen(5)


#file1 = open("test.txt","a") 
clientsocket, address = s.accept()
while True:

	#establish connection to client

	

	#try serving request
	try:
		#recieve request10
		print(f"Connection from {address} has been established!")
		request = clientsocket.recv(1024).decode("utf-8")
		#parse request
		request = request.replace("\r", " ")
		parsedreq = request.split(" ")

		print("request: " + str(parsedreq))
		print("\n \n \n")

		# f.read(1024)
		if(parsedreq[0]=='GET' and parsedreq[2]== 'HTTP/1.0'):
			#look for file name given by request
			file = open(parsedreq[1])
			#prepare file to send
			outgoing = file.read()
			clientsocket.send("HTTP/1.0 200 OK\n".encode("utf-8"))
			#send bytes to client
			for x in range(0,len(outgoing)):
				clientsocket.send(outgoing[x].encode("utf-8"))
		else:
			#unkown command
			clientsocket.send("HTTP/1.0 400 Bad Request\n".encode("utf-8"))

		#print log
		print(datetime.datetime.now(), end=" ")
		print(ip, end=" ")
		print(port, end=" ")
		print(parsedreq[0], end=" ")

		#if non persistent, close connection
		#clientsocket.close()

	#if filename or path does not exist, send 404
	except IOError:
		clientsocket.send("HTTP/1.0 404 Not Found\n".encode("utf-8"))




#parse command
	#serve get request

	#serve 404 error

	#serve invalid command error