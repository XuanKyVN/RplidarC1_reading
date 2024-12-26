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

#--------------PYGAME-----------
from math import pi
import math

yellow = (0, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red =(255,0,0)

#-----------------------


if((sys.version)[2:4] == "11"):
	print("Program is not compatible for Python 3.11,  use 3.10 or 3.9 please")
	# This Program is not compatible for Python 3.11,  use python v3.9 Only please
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


		img = cv2.imread("background.png")
		h,w,ch = img.shape # check image shape

		Cx = 400
		Cy = 400

		cv2.circle(img,(Cx,Cy),350,(255,255,255),2)
		cv2.line(img,(0,400),(800,400),(255,255,255),2)
		cv2.line(img,(400,0),(400,800),(255,255,255),2)
		cv2.putText(img,"0",(730,400),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		cv2.putText(img,"90",(400,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		cv2.putText(img,"180",(5,400),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		cv2.putText(img,"270",(400,740),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		cv2.putText(img,"XuanKyAutomation_RPLIDAR C1",(1,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)



		#for i in range(360):
			#print("Angle:" + str(round(m_data[i].angle)) + "  Distance: " + str(m_data[i].distant) + "  Quantity: " + str(m_data[i].quality))

		#count+=1

		#cv2.imshow("pic", img)
		#cv2.waitKey(1)


		#for i in m_data:
		result_ang =[]
		result_dis =[]
		result_ang_int=[]
		#   Loop in data memory to take data out
		for i in range(530):
			#print(i.quality)
		 	#print(m_data[i].angle,m_data[i].distant)
		  	#AngleRange = [0,5]
			#print(m_data[i].angle)
			result_ang.append(m_data[i].angle)
			result_dis.append(m_data[i].distant)
			result_ang_int.append(int(m_data[i].angle))

		#print(result_ang)
		#print(result_ang_int)
		#print(result_dis)

		# Loop In specific Data collected and slice if 2 items in the matrix and remove one
		for i in range(360):

			index = 0
			pos =[]
			for data in result_ang_int:          # Check each data to find 2 values the same, and index
				if data == i:
					pos.append(index)
				index +=1

			#print(pos)
			#print('-------------After=--------')

			if (len(pos)>1):
				if result_dis[pos[0]]>result_dis[pos[1]]:
					result_ang_int.pop(pos[1])  # remove index    , If Remove Specific cars.remove("Volvo")
					result_dis.pop(pos[1])
				else:
					result_ang_int.pop(pos[0])  # remove index    , If Remove Specific cars.remove("Volvo")
					result_dis.pop(pos[0])
		#print('-------------After=--------')
		#print(result_ang_int)
		#print(result_dis)


		for i in range(len(result_dis)):
			# lineangle = 30 # deg
			X1_line = int(Cx + (result_dis[i] / 20 * math.cos(-result_ang_int[i] / (180 / math.pi)))/1)
			Y1_line = int(Cy + (result_dis[i] / 20 * math.sin(-result_ang_int[i] / (180 / math.pi)))/1)

			cv2.line(img,(Cx,Cy),(X1_line,Y1_line),(0,0,255),1)

		'''
		X1_line1 = int(Cx + (400  * math.cos(-60 / (180 / math.pi)))/1)
		Y1_line1 = int(Cy + (400  * math.sin(-60 / (180 / math.pi))) / 1)
		cv2.line(img, (Cx, Cy), (X1_line1, Y1_line1), (0, 255, 255), 1)
		'''
		cv2.imshow("pic", img)
		cv2.waitKey(1)

''' DATA
[358, 359, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 357]
[0.0, 0.0, 40.5, 43.0, 0.0, 41.5, 0.0, 0.0, 40.0, 32.75, 0.0, 0.0, 0.0, 372.25, 356.0, 354.5, 0.0, 0.0, 123.75, 0.0, 0.0, 0.0, 122.0, 0.0, 0.0, 0.0, 0.0, 100.5, 0.0, 0.0, 0.0, 0.0, 341.75, 340.0, 346.75, 0.0, 0.0, 347.0, 348.5, 352.0, 354.75, 365.75, 361.75, 361.0, 359.75, 0.0, 229.75, 232.25, 0.0, 234.75, 0.0, 0.0, 229.75, 0.0, 386.5, 0.0, 400.5, 396.5, 402.0, 408.75, 413.0, 423.0, 424.25, 424.5, 434.25, 434.75, 447.25, 451.0, 458.25, 461.0, 463.5, 479.0, 488.75, 494.0, 499.0, 516.0, 524.5, 529.75, 543.5, 552.75, 572.5, 577.75, 0.0, 606.75, 0.0, 639.5, 652.0, 677.0, 691.5, 707.25, 739.0, 754.75, 792.0, 812.25, 853.25, 874.75, 899.25, 926.5, 0.0, 0.0, 1000.75, 986.25, 983.0, 983.0, 987.5, 987.25, 989.0, 1019.5, 1039.25, 1056.0, 0.0, 0.0, 0.0, 0.0, 3651.0, 3644.25, 3640.25, 3637.5, 3637.5, 3637.75, 0.0, 1645.0, 1646.5, 1650.25, 1652.0, 1656.5, 1659.25, 1661.0, 1666.0, 1668.0, 1677.75, 1682.0, 1686.5, 1694.0, 1699.75, 1713.25, 1715.5, 0.0, 3198.75, 3205.5, 3244.0, 3266.5, 3266.25, 3287.0, 0.0, 343.75, 338.25, 336.5, 329.5, 326.25, 326.0, 323.25, 321.5, 317.25, 316.75, 315.75, 314.5, 313.25, 312.0, 312.0, 310.75, 310.25, 309.0, 308.5, 308.25, 307.25, 306.25, 306.75, 307.0, 307.0, 306.5, 306.5, 307.0, 308.0, 309.25, 309.75, 314.75, 315.75, 317.0, 321.0, 322.75, 323.75, 326.25, 0.0, 0.0, 348.5, 358.75, 0.0, 333.5, 338.0, 342.5, 349.5, 352.75, 354.5, 358.0, 359.0, 362.75, 365.5, 368.5, 376.0, 381.75, 0.0, 438.5, 453.0, 0.0, 0.0, 51.75, 0.0, 42.75, 0.0, 587.5, 587.5, 0.0, 2788.75, 2792.0, 2810.25, 2814.0, 2815.5, 2827.0, 2831.5, 2840.0, 0.0, 0.0, 556.5, 0.0, 482.25, 467.75, 453.75, 414.25, 0.0, 373.25, 0.0, 0.0, 134.25, 304.25, 307.25, 306.75, 306.75, 341.5, 343.0, 340.25, 338.5, 0.0, 0.0, 0.0, 272.5, 269.25, 268.5, 271.25, 274.75, 291.0, 298.5, 0.0, 332.0, 333.0, 0.0, 113.0, 0.0, 121.0, 122.25, 124.0, 124.75, 124.75, 124.75, 124.75, 125.25, 123.75, 121.5, 125.25, 0.0, 119.0, 123.25, 0.0, 131.25, 0.0, 127.0, 126.0, 0.0, 0.0, 127.0, 0.0, 289.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 137.5, 0.0, 132.5, 0.0, 0.0, 0.0, 0.0, 0.0, 358.0, 0.0, 343.5, 0.0, 361.0, 0.0, 0.0, 158.0, 0.0, 164.75, 0.0, 0.0, 184.0, 0.0, 189.0, 204.25, 206.5, 0.0, 184.75, 182.5, 180.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 143.0, 0.0, 0.0, 0.0, 143.0, 0.0, 0.0, 125.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 33.5, 0.0, 0.0, 0.0, 0.0, 36.75, 0.0, 36.25, 0.0, 0.0, 0.0, 0.0, 39.5, 0.0, 0.0, 0.0, 0.0]

'''

