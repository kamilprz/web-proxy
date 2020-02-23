#! /usr/bin/env python
import os, sys, _thread, socket, time
import tkinter as tk
from tkinter import*

# dict for blocked URLs		
blocked = {}	

#tkinter - GUI used to dynamically block and unlock URLs
def tkinter():
	console = tk.Tk()
	block = Entry(console)
	block.grid(row=0,column=0)
	block_button = Button(console, text="Block URL")
	block_button.grid(row=0, column=1)

	unblock = Entry(console)
	unblock.grid(row=1, column=0)
	unblock_button = Button(console, text="Unblock URL")
	unblock_button.grid(row=1, column=1)

	mainloop()
	
# MAIN PROGRAM
def main():
	# boot up the tkinter gui
	_thread.start_new_thread(tkinter,())

	# user input port number
	listening_port = int(input(">> Enter Listening Port Number: "))

	

if __name__ == '__main__':
	main()
