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
	print("Program is not compatible for Python 3.11,  use 3.10 or 3.9 please")
	# This Program is not compatible for Python 3.11,  use 3.10 or 3.9 please
	exit()


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
BaudRate = 460800  # C1
# 115200  A1
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


		#for i in range(360):
			#print("Angle:" + str(round(m_data[i].angle)) + "  Distance: " + str(m_data[i].distant) + "  Quantity: " + str(m_data[i].quality))

		#count+=1

		#cv2.imshow("pic", img)
		#cv2.waitKey(1)


		#for i in m_data:
		result_ang =[]
		result_dis =[]
		result_ang_int=[]
		for i in range(512):
			#print(i.quality)
		 	#print(m_data[i].angle,m_data[i].distant)
		  	#AngleRange = [0,5]
			#print(m_data[i].angle)
			result_ang.append(m_data[i].angle)
			result_dis.append(m_data[i].distant)
			result_ang_int.append(int(m_data[i].angle))

		#print(result_ang)
		print(result_ang_int)
		print(result_dis)
		index = 0
		pos =[]
		for data in result_ang_int:
			if data == 0:
				pos.append(index)
			index +=1

		print(pos)
		print('-------------After=--------')

		if (len(pos)>1):
			if result_dis[pos[0]]>result_dis[pos[1]]:
				result_ang_int.pop(pos[1])  # remove index    , If Remove Specific cars.remove("Volvo")
				result_dis.pop(pos[1])
			else:
				result_ang_int.pop(pos[0])  # remove index    , If Remove Specific cars.remove("Volvo")
				result_dis.pop(pos[0])

		print(result_ang_int)
		print(result_dis)









