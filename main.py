"""
Temperature monitoring using Dallas DS18B20 sensors
"""
import time

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


