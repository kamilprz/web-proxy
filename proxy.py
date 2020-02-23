#! /usr/bin/env python
import os, sys, _thread, socket, time
import tkinter as tk
from tkinter import*


#tkinter - GUI used to dynamically block and unlock URLs
def tkinter():
	console = tk.Tk()
	block = Entry(console)
	block.pack()
	unblock = Entry(console)
	unblock.pack()

# MAIN PROGRAM
def main():
	# Run a thread of our tkinter function..
	_thread.start_new_thread(tkinter,())

	

if __name__ == '__main__':
	main()

