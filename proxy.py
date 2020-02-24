
import os, sys, threading, socket, time
import tkinter as tk
from tkinter import*

# dict for blocked URLs		
blocked = {}	
# dict for cache
cache = {}
BUFFER_SIZE = 4096
MAX_CONNECTIONS = 60
PORT = 8080
connections = 0

#tkinter - GUI used to dynamically block and unlock URLs
def tkinter():
	console = tk.Tk()

	def block_url():
		ret = block.get()
		temp = blocked.get(ret)
		if temp is None:
			blocked[ret] = 1	
			print(">> Blocked: " + ret)
		else:
			print(">> Already blocked")

	block = Entry(console)
	block.pack()
	block_button = Button(console, text = "Block URL", command = block_url)
	block_button.pack()

	def unblock_url():
		ret = unblock.get()
		temp = blocked.get(ret)
		if temp is None:
			print(">> " + ret + " is not blocked")
		else:
			blocked.pop(ret)
			print(">> Unblocked: " + ret)

	unblock = Entry(console)
	unblock.pack()
	unblock_button = Button(console, text = "Unblock URL", command = unblock_url)
	unblock_button.pack()

	# prints all blocked urls
	def print_blocked():
		print(blocked)

	print_blocked = Button(console, text = "Print Blocked URLs", command = print_blocked)
	print_blocked.pack()

	# prints all cached urls
	def print_cache():
		for key, value in cache.iteritems(): # fix when empty
			print(key)

	print_cache = Button(console, text = "Print Cache", command = print_cache)
	print_cache.pack()

	mainloop()
	

# MAIN PROGRAM
def main():
	# boot up the tkinter gui
	# _thread.start_new_thread(tkinter,())
	thread = threading.Thread(target = tkinter)
	thread.setDaemon(True)
	thread.start()

	try:
		# Ininitiate socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		# bind socket to port
		sock.bind(('', PORT))						
		sock.listen(MAX_CONNECTIONS)						
		print(">> Initializing sockets...")
		print(">> Listening on port {0} ...\n".format(PORT))		
	except Exception:
		print(">> Error")
		sys.exit(2)
	
	global connections
	while connections <= MAX_CONNECTIONS:
		try:
			# accept connection from browser
			conn, client_address = sock.accept()
			connections += 1
			# create thread	for the connection			
			thread = threading.Thread(name = client_address, target = proxy_connection, args = (conn, client_address)) 
			thread.setDaemon(True)
			thread.start()
			print("New connection. Number of connections: " + str(connections))
		except KeyboardInterrupt:
			sock.close()
			sys.exit(1)
	sock.close()


# receive data and parse it, check http vs https
def proxy_connection(conn, client_address):
	global connections
	try:
		# receive data from browser
		data = conn.recv(BUFFER_SIZE)
		# print(data)
		if len(data) > 0:
			# get first line of request
			request_line = data.decode().split('\n')[0]
			method = request_line.split(' ')[0]
			url = request_line.split(' ')[1]
			if method == 'CONNECT':
				type = 'https'
			else:
				type = 'http'

			if isBlocked(url):
				connections -= 1
				conn.close()
				return

			else:
				# need to parse url for webserver and port
				print(">> Request: " + request_line)
				webserver = ""
				port = -1
				tmp = parseURL(url, type)
				if len(tmp) > 0:
					webserver, port = tmp
					# print(webserver)
					# print(port)
				else:
					return 

				# TODO: check cache??
				print("Connected to " + webserver + " on port " + str(port))

				# connect to web server socket
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((webserver, port))

				# handle http requests
				if type == 'http':
					print("im a http request")
					# send client request to server
					sock.send(data)

					while True:
						try:
							# try to receive data from the server
							webserver_data = sock.recv(BUFFER_SIZE)
						except socket.error:
							print("Connection Timeout")
							sock.close()
							conn.close()
							connections -= 1
							return
						
						# if data is not emtpy, send it to the browser
						if len(webserver_data) > 0:
							conn.send(webserver_data)

						# communication is stopped when a zero length of chunk is received
						else:
							sock.close()
							conn.close()
							connections -= 1
							return

				elif type == 'https':
					

	except Exception:
		print("im na exception")
		pass
	
	connections -= 1
	print('iebfulsdfd')
	conn.close()
	return

def isBlocked(url):
	for x in blocked:
		if x in url:
			print(url + " is blocked.")
			return True
	return False


def parseURL(url, type):
	# isolate url from ://
	http_pos = url.find("://")		
	if (http_pos == -1):
		temp = url
	else:
		temp = url[(http_pos+3):]

	# find pos of port if there is one
	port_pos = temp.find(":")		

	# find end of webserver
	webserver_pos = temp.find("/") 	
	if webserver_pos == -1:
		webserver_pos = len(temp)

	webserver = ""
	port = -1
	# default port
	if (port_pos == -1 or webserver_pos < port_pos):
		if type == "https":
			# https
			port = 443
		else:
			# http
			port = 80
		webserver = temp[:webserver_pos]
	# defined port
	else:												
		port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
		webserver = temp[:port_pos]

	return [webserver, int(port)]

if __name__ == '__main__':
	main()
