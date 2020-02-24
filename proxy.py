
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
	
	
	while connections <= MAX_CONNECTIONS:
		try:
			# accept connection from browser
			conn, client_address = sock.accept()
			connections += 1
			# create thread				
			thread = threading.Thread(name = client_address, target = proxy_connection, args = (conn, client_address)) 
			thread.setDaemon(True)
			thread.start()
			print("New connection. Number of connections: " + str(connections))
		except KeyboardInterrupt:
			sock.close()
			sys.exit(1)
	sock.close()


def proxy_connection(conn, client_address):
	# receive data and parse it, check http vs https
	try:
		data = conn.recv(BUFFER_SIZE)
		# print(data)
		if data:
			request_line = data.decode().split('\n')[0]
			method = request_line.split(' ')[0]
			url = request_line.split(' ')[1]
			print(method)
			print(url)

			if isBlocked(url):
				connections -= 1
				conn.close()
	except Exception:
		pass


def isBlocked(url):
	for x in blocked:
		if x in url:
			print(url + " is blocked.")
			return True
	return False

if __name__ == '__main__':
	main()
