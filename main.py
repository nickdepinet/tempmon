"""
Temperature monitoring using Dallas DS18B20 sensors
"""
import time
import threading

class sensor():
	def __init__(self, idNumber):
		self.id = idNumber

	def getTemp(self):
		try:
			file = open(''.join(['/sys/bus/w1/devices/', self.id, '/w1_slave']))
			text = file.read()
			file.close()
			temperature = (float(text.split('\n')[1].split(' ')[9][2:]) / 1000) * (9/5) + 32
		except IOError:
			return -1
		return temperature


class readThread(threading.Thread):
	def __init__(self, sensors, limit):
		threading.Thread.__init__(self)
		self.sensors = sensors
	def run(self):
		while(True):
			for ds in sensors:
				temp = ds.getTemp()
				print temp + ' degrees Fahrenheit'
				if temp > limit:
					alert(temp)
					break
			time.sleep(1800)


def getSensors(config):
	sensors = []
	for item in open(config):
		sensors.append(item.rstrip())
	return sensors


