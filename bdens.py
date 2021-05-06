import Metashape
import os
import sys
import re
import configparser
import subprocess
import glob
import csv

### area name you want to build dense_cloud
ffname = "plant10"

doc = Metashape.app.document
cur_file = os.getcwd() + os.sep + os.path.basename(os.getcwd()) +".psx"
doc.clear()
doc.open(cur_file)

chunk = doc.chunk
camera = chunk.cameras

fpath = os.path.dirname(doc.path)
fnamesp = os.path.splitext(os.path.basename(doc.path))[0]


maskf = glob.glob(fpath + os.sep + "mask" + os.sep+ ffname + os.sep + "DJI*mask.jpg")
#print(maskf)
print(camera[0].label)

maskl = []
for i in range(len(maskf)):
	#print(os.path.basename(maskf[i]))
	#print(os.path.basename(maskf[i]).split("_"))
	smname = os.path.basename(maskf[i]).split("_")
	#print(smname[0] +"_"+smname[1])
	maskl.append(smname[0] +"_"+smname[1])
mskcam = []
for i in range(len(camera)):
	camera[i].enabled = False	
	if camera[i].label in maskl:
		camera[i].enabled = True
		mskcam.append(i)


#for i in range(len(camera)):
#	if camera[i].label in maskl:

chunk.generateMasks(path = os.path.join(fpath, 'mask',ffname, '{filename}_mask.jpg' ),masking_mode=Metashape.MaskingMode.MaskingModeFile,cameras = mskcam,mask_operation=Metashape.MaskOperation.MaskOperationReplacement,tolerance=100  )
chunk.buildDepthMaps(downscale =2 , filter_mode =Metashape.MildFiltering ,reuse_depth=False)
chunk.buildDenseCloud()

doc.save(fpath + os.sep + "mask" + os.sep+ ffname+ os.sep +   ffname +'.psx',chunks = [chunk])
