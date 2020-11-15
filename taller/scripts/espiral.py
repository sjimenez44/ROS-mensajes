#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
import math

class Espiral:
	def __init__(self):
		rospy.init_node('espiral')
		rospy.loginfo('Se inicio nodo espiral')
		self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
		rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
		self.posx = 5.54
		self.posy = 5.54
		self.cmd_vel = Twist()
		self.rate = rospy.Rate(1)

	def update_pose(self, data):
		self.posx = data.x
		self.posy = data.y

	def service(self):
		rospy.wait_for_service('/turtle1/teleport_absolute')
		try:
			teleport = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
			resp = teleport(5.54, 5.54, math.pi)
			return resp
		except rospy.ServiceException, e:
			rospy.loginfo("Fallo: {}".format(e))

	def gen_espiral(self):
		self.cmd_vel.linear.x = 0.5
		self.cmd_vel.angular.z = 4.0
		while not rospy.is_shutdown():
			if (self.posx < 6.5) or (self.posy < 6.5):
				self.cmd_vel.linear.x += 0.5
				self.pub.publish(self.cmd_vel)
				self.rate.sleep()
			else:
				self.cmd_vel.linear.x = 0.0
				self.pub.publish(self.cmd_vel)
				self.rate.sleep()
				self.service()
				rospy.logwarn('La tortuga se salio de los limites [x:6.5, y:6.5]')

if __name__ == '__main__':
	try:
		pub = Espiral()
		pub.gen_espiral()
	except rospy.ROSInterruptException:
		print('Error')

