##20201106 -- calculate image plane coord, like a collision test
#20210114 -- crossing test
#20210201 -- add sql part
#20210428 --- hydro side pilene version
#20210502 -- limited function 

##this script test target area is inside of each camera cone or not
## target areas are imported from csv file
## adjust to test for surfaces facing to the front

import Metashape

import json
import csv
import os
import os.path
import sys
import re
import configparser
import subprocess
import math
import glob
import time
import csv
import pathlib
from PIL import Image, ImageDraw 
######
Target_area = False
######

def crosspx(a,b,c,d,f):
	if(a==c):
		return [a,f]
	elif(b==d or (b -f)*(d-f) > 0 ): 
		return None
	elif(a==c and b==d):
		return None
	else:
		ansx = ( f - d + ((d-b)/(c-a))*c)*((c-a)/(d-b))
		if( ansx > 0 and ansx < 4000):
			return [ansx, f]
		else:
			return None

def crosspy(a,b,c,d,f):
	if(a==c or (a-f)*(c-f)> 0):
		return None
	elif(b==d  ): 
		return[f,b]
	elif(a==c and b==d):
		return None
	else:
		ansy = ((d-b)/(c-a))*f + d-((d-b)/(c-a))*c 
		if(ansy > 0 and ansy < 3000):
			return [f, ansy]
		else:
			return None


#######

doc = Metashape.app.document
cur_file = os.getcwd() + os.sep + os.path.basename(os.getcwd()) +".psx"

doc.clear()
doc.open(cur_file)

this_path = Metashape.app.document.path
cur_folder = os.getcwd()
filename = os.path.basename(os.getcwd())

this_file1 = os.path.splitext(this_path)[0]
print(os.path.dirname(this_file1))

chunk = doc.chunk
camera = Metashape.Camera

invm = Metashape.Matrix.inv(chunk.transform.matrix)

date = chunk.cameras[0].photo.meta["Exif/DateTime"]
datedate = str(date.split()[0])
date2 = datedate.split(":")
datesp = date2[0] + date2[1] + date2[2]

header = ["date","flightID","side","image_name","plant","comm"]
csv_name = os.path.dirname(this_path) + os.sep + "area.csv"

if not os.path.exists('mask'):
	os.mkdir('mask')

flightid = "a"
pbed = "a"
pcenter = []
pname = []
boxx = []
boxy = []
boxz = []

#### plant center setup: case 1
################################
mk_id1 = 0
mk_id2 = 0
scale = 14.4
pnum = 0

for i in range(len(chunk.markers)):
	if chunk.markers[i].label == "target 122":
		mk_id1 = i
	if chunk.markers[i].label == "target 126":
		ma_id2 = i

if Target_area == False:
	pnum = 35
	psep = scale/(pnum + 1)
	boxx = [-0.25,-0.25,-0.25,-0.25,0.25,0.25,0.25,0.25]
	boxy = [0,0,2,2,0,0,2,2]
	boxz = [-0.25,0.25,-0.25,0.25,-0.25,0.25,-0.25,0.25]
	for i in range(pnum):
		pcenter.append(psep*(i + 1))
		pname.append("plant" + str(i + 1))
		if not os.path.exists('mask' + os.sep+ pname[i]):
			os.mkdir('mask' + os.sep+pname[i])
else:
	print("s")
	#ff= open(csv_name + ".csv", 'w', newline = '')
	#writer = csv.writer(ff,lineterminator='\n')
	#writer.writerow(header)
print(pcenter)

################################

cam_num = 0
count = 0

csv_name = datesp  + '_camtest'
ff= open(csv_name + ".csv", 'w', newline = '')
writer = csv.writer(ff,lineterminator='\n')
writer.writerow(header)

for cam_index in range(len(chunk.cameras)):
	camerasp = chunk.cameras[cam_index]
	print(cam_index,camerasp)
	sensorsp = camerasp.sensor
	calibrationsp = sensorsp.calibration
	#### image plane pixel borader
	i4v = [[0,0],[0,sensorsp.height],[sensorsp.width,0],[sensorsp.width,sensorsp.height]]
	inout1 = 0
	inout2 = 0
	inout3 = 0
	
	for i in range(len(pcenter)):
		inout1 = 0
		inout2 = 0
		inout3 = 0
		box3Dlist = []
		im = Image.new('RGB', (4000, 3000), (0, 0, 0))
		draw = ImageDraw.Draw(im)
		for k in range(len(boxx)):
			boxsp = invm.mulp( Metashape.Vector([pcenter[i] + boxx[k] ,   boxy[k],   boxz[k] ]) )
			if(camerasp.project(boxsp) != None):
				tesd1 = camerasp.project( boxsp)[0]
				tesd2 = camerasp.project( boxsp)[1]
				box3Dlist.append( [tesd1,tesd2 ]  )
			elif(camerasp.project(boxsp) == None):
				box3Dlist.append( [-1000000,-1000000 ]  )
		vuse = [[1,5,3,7],[0,3,2,6]]
		combl = [[0,1],[2,3],[4,5],[6,7],[0,2],[1,3],[4,6],[5,7],[0,4],[1,5],[2,6],[3,7]]
		
		for vn in range(len(boxx)):			
			################ 
			################ type1
			projp = []
			if(inout1 == 1):
				#print(i,vn)
				break
			boxsp =  invm.mulp( Metashape.Vector([pcenter[i] + boxx[vn] ,   boxy[vn], boxz[vn] ]) )
			if(camerasp.project(boxsp) != None):
				if (camerasp.project(boxsp)[0] < sensorsp.width and camerasp.project(boxsp)[0] > 0 and camerasp.project(boxsp)[1] < sensorsp.height and camerasp.project(boxsp)[1] > 0 ):
					inout1 = 1
					print(camerasp.label, "test1",pname[i], "point" ,vn,"is in" ,camerasp.project(boxsp) )
					#whne include-flag is on, all vertex point are calc.
					#writer.writerow([datesp, flightid,pbed, camerasp.label, pname[i], "test1", "proj_point", box3Dlist ])
					writer.writerow([datesp, flightid,pbed, camerasp.label, pname[i], "test1"])
					draw.polygon((*box3Dlist[1],*box3Dlist[5],*box3Dlist[7],*box3Dlist[3]), fill=(255, 255, 255), outline=(255, 255, 255))
					draw.polygon((*box3Dlist[0],*box3Dlist[3],*box3Dlist[6],*box3Dlist[2]), fill=(255, 255, 255), outline=(255, 255, 255))
					draw.polygon((*box3Dlist[0],*box3Dlist[1],*box3Dlist[3],*box3Dlist[2]), fill=(255, 255, 255), outline=(255, 255, 255))
					draw.polygon((*box3Dlist[4],*box3Dlist[5],*box3Dlist[7],*box3Dlist[6]), fill=(255, 255, 255), outline=(255, 255, 255))
					im.save('mask'+os.sep+ pname[i] + os.sep + camerasp.label +'_mask.jpg', quality=95)
		###########
		###########		
		## typy2 callculation
		for ss in range(len(combl)):
			if (inout1 ==1 or inout2 ==1):
				break
			
			px1 = box3Dlist[combl[ss][0]]
			px2 = box3Dlist[combl[ss][1]]
			
			if (px1[0] == -1000000 or px2[0] == -1000000):
				test1 = None
				test2 = None
				test3 = None
				test4 = None
			else:
				test1 = crosspx(*px1,*px2,0)
				test2 = crosspx(*px1,*px2,3000)
				test3 = crosspy(*px1,*px2,0)
				test4 = crosspy(*px1,*px2,4000)
						
			if(test1 != None or test2 != None or test3 != None or test4 != None): 
				print(test1,test2,test3,test4 , camerasp.label,pname[i],"line", ss ,"test2","vertex is in")
				inout2 = 1
				writer.writerow([datesp, flightid,pbed, camerasp.label,pname[i], "test2", "proj_point", box3Dlist])
				draw.polygon((*box3Dlist[1],*box3Dlist[5],*box3Dlist[7],*box3Dlist[3]), fill=(255, 255, 255), outline=(255, 255, 255))
				draw.polygon((*box3Dlist[0],*box3Dlist[3],*box3Dlist[6],*box3Dlist[2]), fill=(255, 255, 255), outline=(255, 255, 255))
				draw.polygon((*box3Dlist[0],*box3Dlist[1],*box3Dlist[3],*box3Dlist[2]), fill=(255, 255, 255), outline=(255, 255, 255))
				draw.polygon((*box3Dlist[4],*box3Dlist[5],*box3Dlist[7],*box3Dlist[6]), fill=(255, 255, 255), outline=(255, 255, 255))
				im.save('mask'+os.sep+ pname[i] + os.sep + camerasp.label +'_mask.jpg', quality=95)
			#else:
				#print(test1,test2,test3,test4,camerasp.label,pname[i],"line",ss,"test2","vertex is out")
				
		## typy3 callculation
		for suf in range(len(vuse)):
			if (inout1 == 1 or inout2 == 1 or inout3 ==1):
				break
			#roop for target sueface
			p1 = box3Dlist[vuse[suf][0]]
			p2 =box3Dlist[vuse[suf][1]]
			p3 = box3Dlist[vuse[suf][2]]
			p4 = box3Dlist[vuse[suf][3]]
			for ipn in range(4):
				#roop for image plane's 4vertex
				pasx1 = p2[0]- p1[0]
				pasy1 = p2[1]- p1[1]
				pasxp1 = i4v[suf][0] - p2[0]
				pasyp1 = i4v[suf][1] - p2[1]
				
				sp1 = pasx1 * pasyp1 - pasy1*pasxp1
				
				pasx2 = p3[0]- p2[0]
				pasy2 = p3[1]- p2[1]
				pasxp2 = i4v[suf][0] - p3[0]
				pasyp2 = i4v[suf][1] - p3[1]

				sp2 = pasx2 * pasyp2 - pasy2*pasxp2
				
				pasx3 = p1[0]- p3[0]
				pasy3 = p1[1]- p3[1]
				pasxp3 = i4v[suf][0] - p1[0]
				pasyp3 = i4v[suf][1] - p1[1]
				
				sp3 = pasx3 * pasyp3 - pasy3*pasxp3
				
				if( (sp1 > 0 and sp2 > 0 and sp3 > 0) or (sp1 < 0 and sp2 < 0 and sp3 < 0)):
					inout3 = 1
					writer.writerow([datesp, flightid,pbed, camerasp.label, pname[i], "test3" , "proj_point", box3Dlist])
				pasx4 = p3[0]- p2[0]
				pasy4 = p3[1]- p2[1]
				pasxp4 = i4v[suf][0] - p3[0]
				pasyp4 = i4v[suf][1] - p3[1]
				
				sp4 = pasx4 * pasyp4 - pasy4*pasxp4
				
				pasx5 = p4[0]- p3[0]
				pasy5 = p4[1]- p3[1]
				pasxp5 = i4v[suf][0] - p4[0]
				pasyp5 = i4v[suf][1] - p4[1]
				
				sp5 = pasx5 * pasyp5 - pasy5*pasxp5
				
				pasx6 = p2[0]- p4[0]
				pasy6 = p2[1]- p4[1]
				pasxp6 = i4v[suf][0] - p2[0]
				pasyp6 = i4v[suf][1] - p2[1]
				
				sp6 = pasx6 * pasyp6 - pasy6*pasxp6
				
				if( (sp4 > 0 and sp5 > 0 and sp6 > 0) or (sp4 < 0 and sp5 < 0 and sp6 < 0) and inout3 != 1 ):
					inout3 = 1
					writer.writerow([datesp, flightid,pbed, camerasp.label, pname[i], "test", "proj_point", box3Dlist])
					print(camerasp.label,pname[i],"test3","vertex is in")
				if inout3 == 1:
					draw.polygon((*box3Dlist[1],*box3Dlist[5],*box3Dlist[7],*box3Dlist[3]), fill=(255, 255, 255), outline=(255, 255, 255))
					draw.polygon((*box3Dlist[0],*box3Dlist[3],*box3Dlist[6],*box3Dlist[2]), fill=(255, 255, 255), outline=(255, 255, 255))
					draw.polygon((*box3Dlist[0],*box3Dlist[1],*box3Dlist[3],*box3Dlist[2]), fill=(255, 255, 255), outline=(255, 255, 255))
					draw.polygon((*box3Dlist[4],*box3Dlist[5],*box3Dlist[7],*box3Dlist[6]), fill=(255, 255, 255), outline=(255, 255, 255))
					im.save('mask'+os.sep+ pname[i] + os.sep + camerasp.label +'_mask.jpg', quality=95)
					
ff.close()
print("error = ", count)
print("export finish")
