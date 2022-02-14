import threading
import binascii
from time import sleep
import sys
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO

class Sentiment(object):
	def __init__(self, clf):
		self.to_process = []
		self.to_output = {}
		self.clf = clf
		thread = threading.Thread(target=self.keep_processing, args=())
		thread.daemon = True
		thread.start()

	def process_one(self):
		if not self.to_process:
			return

		input_str, userID = self.to_process.pop(0)
		print("Processing: ")
		sys.stdout.flush()
		output_string = self.clf.process(input_str)
		print("Finished Processing")
		sys.stdout.flush()

		self.to_output[userID] = output_string
	
	def keep_processing(self):
		while True:
			self.process_one()
			sleep(0.005)

	def enqueue_input(self, input):
		self.to_process.append(input)

	def get_text(self, userID):
		while not ((userID in self.to_output) and (self.to_output[userID])):
			sleep(0.005)
		print("Returning:")
		sys.stdout.flush()
		return self.to_output.pop(userID, None)
