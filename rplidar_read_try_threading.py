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


		#for i in range(360):
			#print("Angle:" + str(round(m_data[i].angle)) + "  Distance: " + str(m_data[i].distant) + "  Quantity: " + str(m_data[i].quality))

		#count+=1

		#cv2.imshow("pic", img)
		#cv2.waitKey(1)


		#for i in m_data:
		result_ang =[]
		result_dis =[]
		for i in range(530):
			#print(i.quality)
		 	#print(m_data[i].angle,m_data[i].distant)
		  	#AngleRange = [0,5]
			#print(m_data[i].angle)
			result_ang.append(m_data[i].angle)
			result_dis.append(m_data[i].distant)

		print(result_ang)
		print(result_dis)

		print(len(result_ang))

		# Conclude,  there are 604 data Angle inside RPlidar C1.
		# Now we need to Filter Array Angle and Distance to draw a chart


			#resultLst = []
		'''
		[358.011474609375, 358.6981201171875, 359.4012451171875, 0.0933837890625, 0.8404541015625, 1.5435791015625,
		 2.2467041015625, 2.9498291015625, 3.6529541015625, 4.3560791015625, 5.0592041015625, 5.7623291015625,
		 6.448974609375, 7.1356201171875, 7.8387451171875, 8.5308837890625, 9.327392578125, 10.04150390625,
		 10.7611083984375, 11.480712890625, 12.216796875, 12.9364013671875, 13.656005859375, 14.3701171875,
		 15.029296875, 15.732421875, 16.435546875, 17.138671875, 17.8582763671875, 18.5614013671875, 19.2645263671875,
		 19.9676513671875, 20.6982421875, 21.4013671875, 22.1209716796875, 22.8240966796875, 23.5272216796875,
		 24.2303466796875, 24.9334716796875, 25.6365966796875, 26.356201171875, 27.059326171875, 27.762451171875,
		 28.465576171875, 29.1082763671875, 29.794921875, 30.4815673828125, 31.168212890625, 31.9207763671875,
		 32.6239013671875, 33.3270263671875, 34.0301513671875, 34.716796875, 35.4034423828125, 36.1065673828125,
		 36.793212890625, 37.562255859375, 38.265380859375, 38.9794921875, 39.6826171875, 40.3582763671875,
		 41.044921875, 41.748046875, 42.4346923828125, 43.187255859375, 43.890380859375, 44.593505859375,
		 45.296630859375, 46.1700439453125, 46.9061279296875, 47.6531982421875, 48.3892822265625, 49.0155029296875,
		 49.7186279296875, 50.4327392578125, 51.1358642578125, 51.85546875, 52.55859375, 53.2781982421875,
		 53.9813232421875, 54.700927734375, 55.404052734375, 56.1236572265625, 56.8267822265625, 57.54638671875,
		 58.24951171875, 58.963623046875, 59.666748046875, 60.3863525390625, 61.0894775390625, 61.80908203125,
		 62.51220703125, 63.248291015625, 63.951416015625, 64.6710205078125, 65.3741455078125, 65.9344482421875,
		 66.6046142578125, 67.2802734375, 67.950439453125, 68.7469482421875, 69.4500732421875, 70.1531982421875,
		 70.8563232421875, 71.5594482421875, 72.2625732421875, 72.9656982421875, 73.6688232421875, 74.3719482421875,
		 75.0750732421875, 75.7781982421875, 76.4813232421875, 77.200927734375, 77.904052734375, 78.607177734375,
		 79.310302734375, 80.0299072265625, 80.7330322265625, 81.4361572265625, 82.1392822265625, 82.825927734375,
		 83.5125732421875, 84.2156982421875, 84.90234375, 85.6549072265625, 86.3580322265625, 87.0611572265625,
		 87.7642822265625, 88.450927734375, 89.1375732421875, 89.8406982421875, 90.52734375, 91.29638671875,
		 91.99951171875, 92.713623046875, 93.416748046875, 94.0924072265625, 94.779052734375, 95.482177734375,
		 96.1688232421875, 96.932373046875, 97.635498046875, 98.3551025390625, 99.0582275390625, 99.73388671875,
		 100.4205322265625, 101.1236572265625, 101.810302734375, 102.6837158203125, 103.4197998046875,
		 104.1558837890625, 104.886474609375, 105.4962158203125, 106.1993408203125, 106.9024658203125,
		 107.6055908203125, 108.358154296875, 109.061279296875, 109.7808837890625, 110.4840087890625, 111.170654296875,
		 111.873779296875, 112.576904296875, 113.280029296875, 114.0435791015625, 114.76318359375, 115.4827880859375,
		 116.202392578125, 116.8560791015625, 117.5592041015625, 118.2623291015625, 118.9654541015625,
		 119.4818115234375, 120.135498046875, 120.794677734375, 121.4483642578125, 122.27783203125, 122.9644775390625,
		 123.6676025390625, 124.354248046875, 125.1068115234375, 125.8099365234375, 126.5130615234375,
		 127.2161865234375, 127.90283203125, 128.5894775390625, 129.2926025390625, 129.979248046875, 130.6988525390625,
		 131.385498046875, 132.088623046875, 132.78076171875, 133.494873046875, 134.18701171875, 134.89013671875,
		 135.5767822265625, 136.4996337890625, 137.2467041015625, 137.999267578125, 138.746337890625, 139.3231201171875,
		 140.0262451171875, 140.7293701171875, 141.4324951171875, 142.1685791015625, 142.8717041015625, 143.59130859375,
		 144.29443359375, 144.99755859375, 145.70068359375, 146.40380859375, 147.10693359375, 147.843017578125,
		 148.546142578125, 149.26025390625, 149.96337890625, 150.6390380859375, 151.32568359375, 152.02880859375,
		 152.7154541015625, 153.47900390625, 154.18212890625, 154.9017333984375, 155.6048583984375, 156.3079833984375,
		 157.0111083984375, 157.7142333984375, 158.4173583984375, 159.1534423828125, 159.8565673828125, 160.576171875,
		 161.279296875, 161.982421875, 162.685546875, 163.388671875, 164.091796875, 164.827880859375, 165.531005859375,
		 166.2451171875, 166.9482421875, 167.640380859375, 168.343505859375, 169.046630859375, 169.749755859375,
		 170.4638671875, 171.1669921875, 171.8701171875, 172.5732421875, 173.2763671875, 173.9794921875, 174.6826171875,
		 175.3857421875, 176.0888671875, 176.7919921875, 177.4951171875, 178.1982421875, 178.9178466796875,
		 179.6209716796875, 180.3240966796875, 181.0272216796875, 181.7138671875, 182.406005859375, 183.109130859375,
		 183.7957763671875, 184.5758056640625, 185.2789306640625, 185.99853515625, 186.70166015625, 187.371826171875,
		 188.0584716796875, 188.7615966796875, 189.4482421875, 190.3546142578125, 191.0906982421875, 191.84326171875,
		 192.5738525390625, 193.18359375, 193.88671875, 194.58984375, 195.29296875, 196.06201171875, 196.776123046875,
		 197.4957275390625, 198.21533203125, 198.9019775390625, 199.6051025390625, 200.32470703125, 201.02783203125,
		 201.7474365234375, 202.4505615234375, 203.170166015625, 203.873291015625, 204.576416015625, 205.279541015625,
		 205.982666015625, 206.685791015625, 207.421875, 208.125, 208.839111328125, 209.542236328125, 210.1849365234375,
		 210.87158203125, 211.5582275390625, 212.244873046875, 213.013916015625, 213.717041015625, 214.420166015625,
		 215.123291015625, 215.859375, 216.5625, 217.276611328125, 217.979736328125, 218.682861328125, 219.385986328125,
		 220.089111328125, 220.792236328125, 221.495361328125, 222.198486328125, 222.901611328125, 223.604736328125,
		 224.3408203125, 225.0439453125, 225.7635498046875, 226.4666748046875, 227.0599365234375, 227.7301025390625,
		 228.416748046875, 229.0924072265625, 229.85595703125, 230.5426025390625, 231.2457275390625, 231.932373046875,
		 232.66845703125, 233.37158203125, 234.07470703125, 234.77783203125, 235.4644775390625, 236.151123046875,
		 236.854248046875, 237.54638671875, 238.29345703125, 238.99658203125, 239.69970703125, 240.40283203125,
		 241.0894775390625, 241.776123046875, 242.479248046875, 243.17138671875, 243.9019775390625, 244.6051025390625,
		 245.3082275390625, 246.0113525390625, 246.763916015625, 247.467041015625, 248.1866455078125, 248.8897705078125,
		 249.5599365234375, 250.24658203125, 250.94970703125, 251.6363525390625, 252.388916015625, 253.092041015625,
		 253.795166015625, 254.498291015625, 255.2178955078125, 255.9210205078125, 256.6241455078125, 257.3272705078125,
		 258.013916015625, 258.7005615234375, 259.4036865234375, 260.09033203125, 260.8428955078125, 261.5460205078125,
		 262.2491455078125, 262.9522705078125, 263.7322998046875, 264.451904296875, 265.1715087890625,
		 265.8856201171875, 266.5447998046875, 267.2479248046875, 267.9510498046875, 268.6541748046875,
		 269.3902587890625, 270.0933837890625, 270.8074951171875, 271.5106201171875, 272.2027587890625,
		 272.9058837890625, 273.6090087890625, 274.3121337890625, 275.042724609375, 275.745849609375, 276.4654541015625,
		 277.1685791015625, 277.8717041015625, 278.5748291015625, 279.2779541015625, 279.9810791015625,
		 280.6402587890625, 281.326904296875, 282.0135498046875, 282.7001953125, 283.4637451171875, 284.1668701171875,
		 284.8699951171875, 285.5731201171875, 286.292724609375, 286.995849609375, 287.698974609375, 288.402099609375,
		 289.1217041015625, 289.8248291015625, 290.5279541015625, 291.2310791015625, 291.9342041015625,
		 292.6373291015625, 293.3404541015625, 294.0435791015625, 294.7467041015625, 295.4498291015625,
		 296.1529541015625, 296.8560791015625, 297.5592041015625, 298.2623291015625, 298.9654541015625,
		 299.6685791015625, 300.43212890625, 301.1517333984375, 301.871337890625, 302.5909423828125, 303.2611083984375,
		 303.9642333984375, 304.6673583984375, 305.3704833984375, 306.090087890625, 306.793212890625, 307.496337890625,
		 308.199462890625, 308.935546875, 309.638671875, 310.3582763671875, 311.0614013671875, 311.748046875,
		 312.451171875, 313.154296875, 313.857421875, 314.5770263671875, 315.2801513671875, 315.9832763671875,
		 316.6864013671875, 317.3236083984375, 318.01025390625, 318.702392578125, 319.3890380859375, 320.152587890625,
		 320.855712890625, 321.558837890625, 322.261962890625, 322.965087890625, 323.668212890625, 324.371337890625,
		 325.074462890625, 325.7940673828125, 326.4971923828125, 327.2003173828125, 327.9034423828125,
		 328.6065673828125, 329.3096923828125, 330.0128173828125, 330.7159423828125, 331.402587890625,
		 332.0892333984375, 332.7923583984375, 333.47900390625, 334.2645263671875, 334.9676513671875, 335.687255859375,
		 336.390380859375, 337.060546875, 337.7471923828125, 338.4503173828125, 339.136962890625, 339.8895263671875,
		 340.5926513671875, 341.2957763671875, 341.9989013671875, 342.718505859375, 343.421630859375, 344.124755859375,
		 344.827880859375, 345.531005859375, 346.234130859375, 346.937255859375, 347.640380859375, 348.3544921875,
		 349.0576171875, 349.7607421875, 350.4638671875, 351.156005859375, 351.8426513671875, 352.5457763671875,
		 353.232421875, 353.9794921875, 354.6826171875, 355.3857421875, 356.0888671875, 355.2154541015625,
		 355.9185791015625, 356.6217041015625, 357.3248291015625, 355.5450439453125, 356.231689453125, 356.934814453125,
		 357.6214599609375, 355.3582763671875, 356.044921875, 356.748046875, 357.4346923828125, 353.7762451171875,
		 354.451904296875, 355.1220703125, 355.792236328125, 353.6993408203125, 354.3585205078125, 355.0286865234375,
		 355.682373046875, 352.4029541015625, 353.0731201171875, 353.748779296875, 354.4189453125, 355.089111328125,
		 355.7647705078125, 356.4349365234375, 357.1051025390625, 352.8094482421875, 353.4686279296875,
		 354.1387939453125, 354.79248046875, 355.4791259765625, 356.1383056640625, 356.8084716796875, 357.4676513671875,
		 355.9185791015625, 356.5777587890625, 357.2314453125, 357.890625, 321.558837890625, 322.1685791015625,
		 322.7947998046875, 323.404541015625, 324.0142822265625, 324.6240234375, 325.2337646484375, 325.843505859375,
		 326.4971923828125, 327.10693359375, 327.733154296875, 328.3428955078125, 328.9361572265625, 329.5458984375,
		 330.1556396484375, 330.765380859375, 331.402587890625, 332.0123291015625, 332.6385498046875, 333.248291015625,
		 333.885498046875, 334.4952392578125, 335.1214599609375, 335.731201171875, 336.4508056640625, 337.093505859375,
		 337.730712890625, 338.3734130859375, 338.9337158203125, 339.54345703125, 340.169677734375, 340.7794189453125,
		 341.4166259765625, 342.0263671875, 342.652587890625, 343.2623291015625, 343.8720703125, 344.4818115234375,
		 345.091552734375, 345.7012939453125, 346.35498046875, 346.9647216796875, 347.5909423828125, 348.20068359375,
		 348.8433837890625, 349.453125, 350.0738525390625, 350.68359375, 351.309814453125, 351.9195556640625,
		 352.5457763671875, 353.155517578125, 353.8421630859375, 354.4683837890625, 355.1055908203125,
		 355.7318115234375]

		[0.0, 0.0, 81.0, 0.0, 0.0, 0.0, 0.0, 83.0, 85.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 92.25, 0.0,
		 0.0, 0.0, 0.0, 223.5, 0.0, 429.25, 0.0, 0.0, 0.0, 0.0, 0.0, 429.25, 431.75, 428.25, 0.0, 0.0, 127.0, 0.0,
		 433.25, 433.5, 428.0, 426.5, 0.0, 192.5, 0.0, 0.0, 0.0, 189.5, 0.0, 164.5, 0.0, 0.0, 0.0, 167.5, 164.5, 162.0,
		 0.0, 0.0, 144.0, 143.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 444.5, 0.0, 0.0, 0.0, 0.0, 294.0, 290.25, 0.0, 0.0,
		 0.0, 295.5, 296.5, 0.0, 0.0, 0.0, 0.0, 305.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 257.5, 0.0, 312.75, 0.0, 0.0,
		 0.0, 0.0, 329.25, 0.0, 0.0, 0.0, 0.0, 146.5, 0.0, 288.25, 0.0, 0.0, 304.75, 299.25, 0.0, 0.0, 134.25, 136.0,
		 138.5, 140.75, 141.0, 139.0, 135.0, 134.25, 134.25, 134.75, 134.75, 132.0, 129.75, 130.0, 131.75, 132.25,
		 133.25, 132.25, 131.5, 133.25, 135.0, 135.25, 0.0, 128.25, 127.25, 0.0, 0.0, 1122.25, 1157.25, 0.0, 0.0, 0.0,
		 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3816.25, 3848.5,
		 3836.5, 3832.75, 3837.0, 3834.5, 3831.75, 3828.75, 3827.25, 3827.25, 3827.75, 3829.0, 3829.25, 3822.75, 0.0,
		 0.0, 3839.5, 3845.0, 3850.5, 3854.75, 3828.75, 3802.75, 3808.75, 3816.75, 3825.0, 3834.25, 3845.5, 3856.5,
		 3867.25, 0.0, 647.25, 646.0, 644.0, 642.25, 640.25, 639.75, 642.75, 646.0, 649.0, 652.0, 656.75, 660.75, 664.0,
		 668.0, 669.75, 660.75, 650.25, 0.0, 688.75, 693.25, 696.25, 698.75, 700.25, 705.75, 712.25, 716.5, 720.0,
		 727.25, 735.0, 735.25, 730.75, 738.5, 0.0, 783.0, 792.5, 801.25, 810.25, 815.5, 0.0, 0.0, 3975.5, 3929.5,
		 3880.0, 3831.5, 3786.25, 3740.0, 3666.25, 3590.5, 3582.0, 3578.75, 3540.5, 3503.75, 3470.5, 3436.75, 3403.25,
		 3372.0, 3339.75, 3311.25, 3284.25, 3256.75, 3231.5, 3209.0, 3186.0, 0.0, 1202.5, 1213.0, 1228.75, 1241.75,
		 1250.75, 1254.25, 1259.0, 1266.0, 1281.75, 1312.25, 1342.5, 1358.0, 1367.0, 1373.0, 0.0, 2862.5, 2854.5,
		 2842.5, 2833.0, 2823.0, 2813.0, 2805.0, 2797.5, 2791.0, 2784.75, 2777.0, 2769.75, 2763.25, 0.0, 189.75, 189.5,
		 185.75, 187.0, 0.0, 203.5, 204.5, 0.0, 0.0, 0.0, 0.0, 2759.0, 2737.0, 2700.0, 2704.75, 2705.25, 2708.75,
		 2711.5, 2714.25, 2716.75, 2718.0, 2721.75, 2725.75, 2729.75, 2733.5, 2738.0, 2740.0, 2734.5, 0.0, 540.75,
		 546.75, 0.0, 314.5, 309.5, 306.5, 302.75, 300.5, 300.75, 305.25, 312.5, 0.0, 330.75, 339.75, 0.0, 1375.0, 0.0,
		 0.0, 774.5, 0.0, 1094.5, 1088.25, 1088.5, 1094.5, 1109.0, 1133.5, 0.0, 1112.5, 1114.5, 1114.0, 0.0, 0.0,
		 120.25, 119.0, 117.5, 115.75, 113.75, 112.0, 109.25, 106.75, 0.0, 101.25, 101.0, 100.0, 98.5, 98.0, 96.75,
		 96.25, 97.0, 98.75, 101.25, 0.0, 109.0, 109.75, 111.25, 113.0, 0.0, 117.5, 116.75, 116.0, 115.25, 115.75,
		 117.5, 119.25, 120.5, 122.25, 125.25, 127.75, 130.75, 132.75, 0.0, 0.0, 174.0, 178.75, 181.5, 181.75, 182.25,
		 182.5, 180.5, 179.25, 180.5, 182.75, 181.0, 0.0, 0.0, 465.75, 0.0, 616.25, 619.5, 614.75, 614.0, 0.0, 578.5,
		 0.0, 0.0, 0.0, 0.0, 620.0, 0.0, 459.5, 452.0, 450.25, 0.0, 0.0, 211.75, 209.0, 0.0, 216.5, 214.5, 215.5, 0.0,
		 210.5, 208.5, 206.25, 205.5, 206.25, 208.5, 207.0, 201.75, 199.75, 0.0, 220.0, 221.25, 216.75, 217.0, 220.0,
		 222.0, 223.5, 221.5, 222.0, 227.0, 232.0, 0.0, 0.0, 0.0, 398.75, 401.0, 402.0, 403.75, 407.75, 412.5, 415.25,
		 419.5, 425.5, 434.5, 0.0, 0.0, 698.25, 704.25, 713.25, 724.0, 730.5, 735.5, 739.5, 744.5, 752.25, 760.0, 767.5,
		 769.25, 764.75, 765.0, 763.25, 749.0, 731.75, 719.75, 708.5, 695.75, 685.75, 677.75, 668.5, 656.75, 646.75,
		 638.5, 629.75, 620.75, 612.75, 606.0, 598.5, 591.5, 584.75, 577.75, 571.25, 565.5, 560.0, 553.75, 548.75,
		 545.0, 539.75, 538.25, 0.0, 0.0, 96.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 88.5, 0.0, 0.0, 0.0, 0.0,
		 536.75, 543.0, 0.0, 0.0, 537.25, 539.25, 547.5, 0.0, 545.5, 540.5, 536.75, 541.5, 553.25, 0.0, 0.0, 0.0, 541.5,
		 537.0, 537.5, 0.0, 0.0, 0.0, 0.0, 85.75, 0.0, 0.0, 0.0, 0.0, 445.5, 451.0, 458.5, 470.0, 0.0, 716.5, 724.0,
		 727.5, 737.0, 748.0, 753.0, 757.0, 761.5, 766.0, 771.0, 776.0, 781.5, 788.5, 792.0, 789.5, 787.0, 788.0, 778.5,
		 760.5, 747.5, 736.0, 724.5, 715.0, 706.5, 698.0, 690.0, 681.0, 671.5, 663.0, 655.5, 649.5, 642.0, 634.5, 628.0,
		 621.0, 615.5, 609.0, 603.0, 597.5, 592.0, 586.5, 580.5, 575.0, 571.0, 566.5, 561.5, 558.0, 555.5, 560.5, 568.0,
0
		for res in m_data:
		 	if (res.angle > AngleRange[0] or res.angle < AngleRange[1]) and res.distant > 0:
		 	resultLst.append(res.distant)
		 	medianNum =  statistics.median(resultLst)
		 	print("Get a frame with ", m_data_count," points, front distant is ",medianNum)
		 	
		'''


