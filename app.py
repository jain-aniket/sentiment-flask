import sys
from sys import stdout
# from process import webopencv
import logging
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO, emit
# from camera import Camera
import random
from time import sleep



#----------------- Video Transmission ------------------------------#
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['DEBUG'] = True
socketio = SocketIO(app)
# camera = Camera(webopencv())

#---------------- Video Transmission --------------------------------#

# Grabbing sentiment object 
from sentiment import Sentiment
from process import sentiment_clf
sentiment = Sentiment(sentiment_clf())
# see commment in sentiment.py for what I need to access.

#---------------- Video Socket Connections --------------------------#
@socketio.on('input image', namespace='/test')
def test_message(input):
	print(input)
	sys.stdout.flush()
	print("Input Recieved ^^")
	sys.stdout.flush()
	sentiment.enqueue_input([input, (request.sid)])
	print("Input Enqueued")
	sys.stdout.flush()
	sleep(0.2)
	prediction = sentiment.get_text(request.sid)
	print("emitting prediction")
	sys.stdout.flush()
	emit('classified', prediction)
	print("emitted prediction")
	sys.stdout.flush()


@socketio.on('connect', namespace='/test')
def test_connect():
	app.logger.info("client connected")
	userID = request.sid
	print(str(userID)+ " CONNECTED --------------------")
	sys.stdout.flush()

@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')


def gen(userID):
	"""Video streaming generator function."""

	app.logger.info("starting to generate frames!")
	while True:
		print("About to Fetch prediction")
		sys.stdout.flush()
		prediction = sentiment.get_text(userID)
		print(prediction)
		sys.stdout.flush()
		#yield (b'--frame\r\n'
		#	   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		
@app.route('/', defaults={'userID': ''})
@app.route('/video_feed/<userID>')
def video_feed(userID):
	print("LINE 68 IN APP.PY")
	sys.stdout.flush()
	"""Video streaming route. Put this in the src attribute of an img tag."""

	return Response(gen(userID), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	socketio.run(app)
