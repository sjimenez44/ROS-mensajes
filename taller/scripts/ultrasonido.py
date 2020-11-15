#!/usr/bin/env python

import rospy
#from sensor_msgs.msg import Range
from robot_msgs.msg import ultrasonico
from std_srvs.srv import Trigger
from random import randrange

class UltrasonidoSensor():
	def __init__(self, sensor_min, sensor_max):
		rospy.init_node('ultrasonido')
		rospy.loginfo('Se ha inicializado sensor de ultrasonido')
		rospy.logdebug('Se inicia en SI')
		self.ultrasonido_pub = rospy.Publisher('/ultrasonido', ultrasonico, queue_size = 3)
		rospy.Service('cambio_unidades', Trigger, self.callback_metrico)
		self.rate = rospy.Rate(1.0) #-- 1 Hz

		self.metrico = True

#		self.sensor_info = Range()
		self.sensor_info = ultrasonico()
		self.sensor_info.ultrasonico.header.frame_id = 'Sensor 1'
		self.sensor_info.ultrasonico.radiation_type = self.sensor_info.ultrasonico.ULTRASOUND
		self.sensor_info.ultrasonico.field_of_view = 0.5
		self.sensor_info.ultrasonico.min_range = sensor_min
		self.sensor_info.ultrasonico.max_range = sensor_max

	def leer_ultrasonido(self):
		if (self.metrico):
			self.sensor_info.ultrasonico.range =  randrange(self.sensor_info.ultrasonico.min_range, self.sensor_info.ultrasonico.max_range) / 100.0
		else:
			self.sensor_info.ultrasonico.range =  randrange(self.sensor_info.ultrasonico.min_range, self.sensor_info.ultrasonico.max_range) / 2.54
		self.sensor_info.metrico.data = self.metrico

	def pub_info(self):
		while not rospy.is_shutdown():
			self.sensor_info.ultrasonico.header.stamp = rospy.Time.now()
			self.leer_ultrasonido()
			self.ultrasonido_pub.publish(self.sensor_info)
			self.rate.sleep()

	def callback_metrico(self, req):
		if (self.metrico):
			self.metrico = False
			rospy.loginfo('Se han cambiado las unidades del sensor a pulgadas')
			return {'success': True, 'message': 'El cambio se ha realizado con exito a pulgadas'}
		else:
			self.metrico = True
			rospy.loginfo('Se han cambiado las unidades del sensor a metros')
			return {'success': True, 'message': 'El cambio se ha realizado con exito a metros'}

if __name__ == '__main__':
	try:
		ultra = UltrasonidoSensor(2, 240)
		ultra.pub_info()
	except rospy.ROSInterruptException:
		print('Error')
