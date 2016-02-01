#Importing libraries
import RPi.GPIO as gpio
import serial, time
from flask import Flask, render_template, request
import datetime

#Setting up web server
ctrlSys = Flask(__name__)

#Setting up i/o
solPin = 24
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(solPin, gpio.OUT)
gpio.output(solPin, gpio.LOW)	

#Setting up serial
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
arduino.close()


def get():
	global aa, bb, cc
	finish = False
	aa = bb = cc = rr = -1
	print("Start to retrieve data @" + getTime())
	arduino.open()
	attempt = 0
	try:

		while (not finish):
			attempt = attempt + 1
			arduino.write("1")
			response = arduino.readline()
			print("At attempt"+str(attempt)+"                 received\""+response+"\"")
			rr = filter(str.isdigit, response)	#Keep usable strings
			if rr == '':	#Data invalid
				rr = -1
			if ((aa != -1) and (bb != -1) and (cc != -1)):
				finish = True
			rr = int(rr)
			if rr >= 4000 or rr <= 1000:	#Data invalid
				rr = -1
			elif rr >= 3000:	#Data belongs to sensor 3
				cc = int(rr)-3000
			elif rr >= 2000 :	#Data belongs to sensor 2
				bb = int(rr)-2000
			elif rr >= 1000:	#Data belongs to sensor 1
				aa = int(rr)-1000
			print ("sensor1=          "+str(aa))
			print ("sensor2=          "+str(bb))
			print ("sensor3=          "+str(cc))
			if attempt == 30:
				print("Trying 30 times without result received, disconnected?")
				finish = True
	except OSError:
		print("OSError Occured @" + getTime())
		pass
	except serial.SerialException:
		print("SerialException Occured @" + getTime())
		pass
	print("Data retreve ended @" + getTime())
	arduino.close()

def water(duration):
	print ("Start watering for " + duration + "seconds @" + getTime())
	gpio.output(solPin, gpio.HIGH)
	time.sleep(float(duration))
	gpio.output(solPin, gpio.LOW)
	print ("Finish watering for " + duration + "seconds @" + getTime())
	
def getTime():
	return datetime.datetime.now().strftime("%Y-%m-%d__%H:%M:%S")
	
#For Index page
@ctrlSys.route("/")
def index():
	get()
	sendData = {
		'title' : "Watering System Controller",
		'time' : getTime(),
		'pin' : solPin,
		'aa' : aa,
		'bb' : bb,
		'cc' : cc
       }
	return render_template("main.html", **sendData)

@ctrlSys.route("/", methods=['POST'])
def set() :
	watering = request.form['dura']
	if watering > 0:
		water(watering)
	get()
	sendData = {
		'pin' : solPin,
		'time' : getTime(),
		'aa' : aa,
		'bb' : bb,
		'cc' : cc,
		'pin' : solPin
    
    }
	return render_template("main.html", **sendData)
	

if __name__ == "__main__":
    ctrlSys.run(host="0.0.0.0", port=80, debug=True)