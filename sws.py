#line for testing
#nc 10.10.1.100 1236 <swstestinput.txt
#python3 sws.py '10.10.1.100' 1236

import socket
import sys
import datetime
import threading 

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = sys.argv[1]
port = int(sys.argv[2])


s.bind((ip, port))
s.listen(5)

def threadedsocket(clientsocket, address):
	try:
		#recieve request
		print(f"Connection from {address} has been established!")
		request = clientsocket.recv(1024).decode("utf-8")
		splitreqs = request.split("\r\n\r\n")
		for x in range(0, len(splitreqs)):
	
			#parse request
			splitreqs[x] = splitreqs[x].replace("\r\n", " ")
			splitreqs[x] = splitreqs[x].replace(": ", " ")
			splitreqs[x] = splitreqs[x].replace(":", " ")
			parsedreq = splitreqs[x].split(" ")

			#print first part of log
			print(datetime.datetime.now(), end=" ")
			print(ip, end=" ")
			print(port, end=" ")
			print(parsedreq[0], end=" ")
			print(parsedreq[1], end=" ")
			print(parsedreq[2], end="; ")

			if(parsedreq[0]=='GET' and parsedreq[2]== 'HTTP/1.0'):
				#look for file name given by request
				file = open(parsedreq[1])
				#prepare file to send
				outgoing = file.read()
				clientsocket.send("HTTP/1.0 200 OK\n".encode("utf-8"))
				print("HTTP/1.0 200 OK")
				#send bytes to client
				for x in range(0,len(outgoing)):
					clientsocket.send(outgoing[x].encode("utf-8"))
			else:
				#unkown command
				clientsocket.send("HTTP/1.0 400 Bad Request\n".encode("utf-8"))
				print("HTTP/1.0 400 Bad Request")
			print("\n \n \n")
			if(len(parsedreq)>=5):
				#unless requested keep-alive, close socket
				if(parsedreq[4]!='keep-alive'):
					clientsocket.close()
					return

	#if filename or path does not exist, send 404
	except IOError:
		clientsocket.send("HTTP/1.0 404 Not Found\n".encode("utf-8"))
		print("HTTP/1.0 404 Not Found")


#main loop
while True:
	clientsocket, address = s.accept()
	connected = True
	clientsocket.settimeout(60)
	#spawn thread to handle client request
	threading.Thread(target = threadedsocket,args = (clientsocket,address)).start()
