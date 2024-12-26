# -*- coding: UTF-8 -*-
from ctypes import *
import ctypes
import serial
import time
import os, cv2
from math import log
import numpy as np
import threading
import subprocess
import statistics

import sys
if((sys.version)[2:4] == "11"):
	print("程序不兼容python11 请用老版本python运行")
	# This Program is not compatible for Python 3.11,  use 3.10 or 3.9 please
	exit()


#----------以下四种加载DLL方式皆可—————————
# pDLL = WinDLL("./myTest.dll")
# pDll = windll.LoadLibrary("./myTest.dll")
# pDll = cdll.LoadLibrary("./myTest.dll")
rpsdk = CDLL("./RPLidarDLL1.dll")

def OnConnect(channelType, path, portOrBaud):
	# arg1 = c_char_p(bytes(path, 'utf-8'))
	arg1 = c_char_p(path.encode())
	return rpsdk.OnConnect(channelType, arg1, portOrBaud)

def OnDisconnect():
	return rpsdk.OnDisconnect

def StartMotor():
	return rpsdk.StartMotor();

def EndMotor():
	return rpsdk.EndMotor();

def StartScan():
	return rpsdk.StartScan(False, True)

def StartScanExpress(Mode):
	return rpsdk.StartScanExpress(False, Mode)

def setMotorSpeed(speed = 0xFFFF):
	return rpsdk.setMotorSpeed(speed)

def EndScan():
	return rpsdk.EndScan()

def ReleaseDrive():
	return rpsdk.ReleaseDrive()

def GetLidarDataSize():
	return rpsdk.GetLidarDataSize()

def GrabData(m_data):
	return rpsdk.GrabData(byref(m_data))

class LidarData(ctypes.Structure):
    _fields_ = [("angle", ctypes.c_float),
                ("distant", ctypes.c_float),
                ("quality", ctypes.c_int)]

m_data_t = LidarData*(8192*4)


m_data = m_data_t()

channelType = 0 #serial
BaudRate = 460800

LidarCOM = "\\\\.\\COM17"

OnConnect(channelType,LidarCOM,BaudRate)
# StartScan()
StartScanExpress(0)
count = 0



while(count<50000):
	m_data_count = GrabData(m_data)

	if(m_data_count == 0):
		time.sleep(5/1000)
	else:
		#print(m_data_count)
		cntt = 0
		for i in m_data:
			if i.distant != 0:
				cntt+=1

		'''
		img = cv2.imread("background.png")
		h,w,ch = img.shape # check image shape
		
		print(h)
		print(w)
		print(ch)
		cv2.circle(img,(400,400),400,(255,255,255),2)
		'''


		for i in range(360):
			print("Angle:" + str(round(m_data[i].angle)) + "  Distance: " + str(m_data[i].distant) + "  Quantity: " + str(m_data[i].quality))

		count+=1

		#cv2.imshow("pic", img)
		#cv2.waitKey(1)

		'''
		for i in m_data:
			print(i.quality)
		 	print(m_data[0].angle,m_data[0].distant)
		  	AngleRange = [359.5,0.5]
			resultLst = []
		for res in m_data:
		 	if (res.angle > AngleRange[0] or res.angle < AngleRange[1]) and res.distant > 0:
		 	resultLst.append(res.distant)
		 	medianNum =  statistics.median(resultLst)
		 	print("Get a frame with ", m_data_count," points, front distant is ",medianNum)
		 	
		'''


