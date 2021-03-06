# Imports for config and bparts
import configparser
import io
import sys
config = configparser.ConfigParser()
#Reads the master.ini config file in the configs folder
config.read('../configs/master.ini')
#Takes the techcamp folder path from the master.ini config file
techcamp_path = config['paths']['techcamp']
#Adds the techcamp folder as a system path so that is can find bparts
sys.path.append(techcamp_path)
from bparts import commsocket

#Other imports
import socket
import picamera
import threading
import io
from Queue import Queue
from time import sleep
from datetime import datetime
from bparts import commsocket

camera = picamera.PiCamera()
# Globals
flask_port = int(config['ports']['flask_port'])
cmd = ''
message=''
time=0
time_delay =5
q=Queue(maxsize=1)


def take_pic(time):
	while 1:
		sleep(1)
		#Change camera settings	
		camera.color_effects = (128,128) #sets the camera to black and white
		camera.resolution=(320,240) #sets the resolution of the camera
		camera.annotate_text_size = 16 #default 32
		camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #adds time stamp to image

		camera.capture('app/static/images/stream.jpg') #Take the image
		print 'Img taken'
		if time==10:
			camera.capture('data/images/bw/bw_'+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.jpg')
			time=0
		time = time+1

		#Checks if item in queue; aka should it take a color picture
		while not q.empty():
				#Change camera settings	
			camera.color_effects = None #removes all color effects
			camera.resolution=(2592,1944)  #sets the resolution of the camera
			camera.annotate_text_size = 48 #default 32
			camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Adds time stamp to image
			camera.capture('app/static/images/color.jpg') #Take the image
			camera.capture('data/images/color/color_'+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.jpg')
			#ends queue task
			q.task_done()

def take_color(message):
	print message
	if message == 'color':
		sleep(time_delay)
		q.put(1)

def commsocket_funct():
	print 'Starting Commsocket'
	commsocket.server(take_color, flask_port)

# Main Loop
x = threading.Thread(name='img_stream', target=take_pic,args=(time,))
y = threading.Thread(name='socket', target=commsocket_funct)
print 'starting now'
x.start()
y.start()

	#Listen to the flask socket; Removed 4/18/18 due to respfunct error
	#commsocket.server(answer(), flask_port)

	#consantly create a image in the image folder for Flask



