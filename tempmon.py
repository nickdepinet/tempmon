"""
Temperature monitoring using Dallas DS18B20 sensors
"""
import time
import threading
import smtplib
from email.mime.text import MIMEText

class sensor():
	def __init__(self, idNumber):
		self.id = idNumber

	def getTemp(self):
		try:
			file = open(''.join(['/sys/bus/w1/devices/', self.id, '/w1_slave']))
			text = file.read()
			file.close()
			temperature = (float(text.split('\n')[1].split(' ')[9][2:]) / 1000) * (9.000/5.000) + 32.000
		except IOError:
			return -1
		return temperature


class readThread(threading.Thread):
	def __init__(self, sensors, limit):
		threading.Thread.__init__(self)
		self.sensors = sensors
		self.limit = limit
	def run(self):
		while(True):
			for ds in self.sensors:
				temp = ds.getTemp()
				print(str(temp) + ' degrees Fahrenheit')
				if temp > self.limit:
					alert(temp, limit)
					break
			time.sleep(1800)


def getSensors(config):
	sensors = []
	for item in open(config):
		sensors.append(sensor(item.rstrip()))
	return sensors

def alert(temp, limit):
	body = ''.join(['The server room temperature is ', str(temp), ', above the set limit of ', str(limit), '.'])
	msg = MIMEText(body)
	msg['Subject'] = 'Server room temperature alert'
	msg['From'] = 'alert@tempmonpi.csh.rit.edu'
	# msg['To'] = 'rtp@csh.rit.edu'
	msg['To'] = 'depinetnick@gmail.com'
	# Set the proper smtp server settings here for your setup
	# TODO: move this into config and read it
	s = smtplib.SMTP('brownstoat.csh.rit.edu')
	s.sendmail('alert@tempmonpi.csh.rit.edu', ['depinetnick@gmail.com'], msg.as_string())
	s.quit()


if __name__ == "__main__":
	alert(2, 1)
	# read = readThread(getSensors('config/sensors.config'), 85)
	# read.run()
