import Metashape
import os
import sys
import re
import configparser
import subprocess
import glob



doc = Metashape.app.document

doc.addChunk()
chunk = doc.chunk

#cur_dir = os.getcwd()
cur_dir = "C:/Users/kkoda/Desktop/rename"

list_file = glob.glob(cur_dir + os.sep + '*.jpg')
#log_path = os.path.join(cur_dir, 'test_log.tsv')
chunk.addPhotos(list_file)

for camera in list(chunk.cameras):
		camera.reference.location = None	
		camera.reference.rotation = None

for sensor in chunk.sensors:
	sensor.rolling_shutter = True
	
#chunk.matchPhotos(downscale = 1,generic_preselection=True  ,keypoint_limit=50000,tiepoint_limit=1000)
chunk.matchPhotos(downscale = 1,generic_preselection=True, reference_preselection=True, reference_preselection_mode=Metashape.ReferencePreselectionSequential  ,keypoint_limit=50000,tiepoint_limit=1000)
#Reference preselection mode in [ReferencePreselectionSource, ReferencePreselectionEstimated, ReferencePreselectionSequential]
chunk.alignCameras()

doc.save(cur_dir + os.sep + 'test.psx',chunks = [chunk])

