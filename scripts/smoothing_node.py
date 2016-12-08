#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imagepreprocessing import ImagePreparator
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

NODE_NAME = "smoothing_node"
SUB_TOPIC = "image"
PUB_TOPIC = "image_preproc_smooth"
QUEUE_SIZE = 10

class SmoothingNode:

	def __init__(self, sub_topic, pub_topic):
		self.bridge = CvBridge()
		self.img_prep = ImagePreparator() 
		self.image_sub = rospy.Subscriber(sub_topic, Image, self.callback)
		self.image_pub = rospy.Publisher(pub_topic, Image, queue_size=QUEUE_SIZE)
		rospy.spin()

	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
		except CvBridgeError as e:
			rospy.logerr(e)

		blurred = self.img_prep.blur(cv_image, (5,5), 0)

		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(blurred, "mono8"))
		except CvBridgeError as e:
			rospy.logerr(e)


def main():
	# Initialisiere den Knoten
	rospy.init_node(NODE_NAME, anonymous=True)
	try:
		ld_node = SmoothingNode(SUB_TOPIC, PUB_TOPIC)
	except KeyboardInterrupt:
		rospy.loginfo("Shutting down node %s", NODE_NAME)

if __name__ == '__main__':
	main()
