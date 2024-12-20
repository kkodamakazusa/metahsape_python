#part of script for performing the camera align by Metashape [1.7.0]
#not include special code, just the nominal usage of metashape api
# metashape official forum is good resource tfor scripting
#2021/04/22

import Metashape
import os
import sys
import re
import configparser
import subprocess
import glob

markerl = [121,122,125,126]
scalel = [14.4, 1.484, 1.48]

doc = Metashape.app.document
doc.addChunk()
chunk = doc.chunk #makeing main chunk


cur_dir = "C:/Users/kkoda/Desktop/rename" # input working path( the folder include target images)

list_file = glob.glob(cur_dir + os.sep + '*.jpg') # get all image inside working folder.


chunk.addPhotos(list_file) # add images to the chunk
chunk.analyzePhotos(chunk.cameras) #estimate image quality


for camera in list(chunk.cameras):
		camera.reference.location = None #clear GPS information, drone sometimes catch signal even if indoor
		camera.reference.rotation = None #

for sensor in chunk.sensors:
	sensor.rolling_shutter = True# enable rolling-shutter compensation

# change coordinate to metashape local(non-gsp)
chunk.crs = Metashape.CoordinateSystem('LOCAL_CS["Local Coordinates",LOCAL_DATUM["Local Datum",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]')

for camera in chunk.cameras:# image quality check and unselecte low quality image
	print(camera.meta['Image/Quality'])
	if(camera.meta['Image/Quality'] !=None) :
		if(float(camera.meta['Image/Quality']) < 0.75) :
			camera.enabled = False
			
## ---- image matching section
#chunk.matchPhotos(downscale = 1,generic_preselection=True, reference_preselection=True, reference_preselection_mode=Metashape.ReferencePreselectionSequential  ,keypoint_limit=50000,tiepoint_limit=1000)
chunk.matchPhotos(downscale = 1,generic_preselection=True, reference_preselection=False  ,keypoint_limit=50000,tiepoint_limit=1000)
#chunk.matchPhotos(downscale = 1,generic_preselection=True  ,keypoint_limit=50000,tiepoint_limit=1000)
#downscale 0=highest, 1=high, 2=medium, 4=low, 8=lowest
#Reference preselection mode [ReferencePreselectionSource, ReferencePreselectionEstimated, ReferencePreselectionSequential]

#--- camera align by sfm
chunk.alignCameras()

misscam = []
for camera in chunk.cameras:
	if camera.center == None:
		misscam.append(camera.key)
		
if len(misscam) > 8:#if non-aligned camera are too many, additional alighment will should be perfromed
	chunk.alignCameras(misscam, reset_alignment=False)

#--- marker detection
chunk.detectMarkers()
mList = []
for i in range(len(chunk.markers)):
	mList.append(chunk.markers[i].label)
mindList = []
for i in range(len(markerl)):
	mindList.append(mList.index("target "+ str(markerl[i])))

chunk.addScalebar(chunk.markers[mindList[1] ] ,chunk.markers[mindList[3] ] )
chunk.scalebars[len(chunk.scalebars)-1].reference.distance = scalel[0]

chunk.addScalebar(chunk.markers[mindList[2] ] ,chunk.markers[mindList[3] ] )
chunk.scalebars[len(chunk.scalebars)-1].reference.distance = scalel[1]

chunk.addScalebar(chunk.markers[mindList[0] ] ,chunk.markers[mindList[1] ] )
chunk.scalebars[len(chunk.scalebars)-1].reference.distance = scalel[2]

#---optimaze 
chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, \
fit_k1=True,fit_k2=True, fit_k3=True, fit_k4=True, fit_p1=True, fit_p2=True,fit_corrections=False,\
 adaptive_fitting=False, tiepoint_covariance=False)




#--- save psx file
doc.save(cur_dir + os.sep + 'test.psx',chunks = [chunk])

