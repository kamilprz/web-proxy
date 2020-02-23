#! /usr/bin/env python
import os, sys, _thread, socket, time
import tkinter as tk
from tkinter import*

# dict for blocked URLs		
blocked = {}	
# dict for cache
cache = {}
BUFFER_SIZE = 4096

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
		for key, value in cache.iteritems():
			print(key)

	print_cache = Button(console, text = "Print Cache", command = print_cache)
	print_cache.pack()

	mainloop()
	
# MAIN PROGRAM
def main():
	# boot up the tkinter gui
	_thread.start_new_thread(tkinter,())

	# user input port number
	port = int(input(">> Enter Listening Port Number: "))

	try:
		# Ininitiate socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		# bind socket to port
		s.bind(('', port))						
		s.listen()						
		print(">> Initializing sockets...")
		print(">> Server boot successful [ {0} ]\n".format(port))		
	except Exception:
		print(">> Error")
		sys.exit(2)
	
	while True:
		try:
			# connection from browser
			conn, client_addr = s.accept()		
			# receive data
			data = conn.recv(BUFFER_SIZE)		
			# start thread
			_thread.start_new_thread(proxy_thread, (conn, data, client_addr)) 
		except KeyboardInterrupt:
			s.close()
			sys.exit(1)
	s.close()

if __name__ == '__main__':
	main()
