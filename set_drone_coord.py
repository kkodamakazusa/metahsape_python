#hydro

import PhotoScan
import Metashape
import os
import sys
import re
import configparser
import subprocess

import math
import datetime

cur_file = "C:/Users/kkoda/Desktop/rename/test.psx" 


doc = PhotoScan.app.document
doc.clear()
doc.open(cur_file)
chunk = doc.chunk
region = chunk.region

#Camera = PhotoScan.app.document.chunk.camera.Reference

Camera = PhotoScan.Camera

#R = chunk.region.rot		#Bounding box rotation matrix
#C = chunk.region.center		#Bounding box center vector
fpath = os.path.dirname(doc.path)
fnamesp = os.path.splitext(os.path.basename(doc.path))[0]

Tlist = []
for i in range(len(chunk.markers)):
	Tlist.append(chunk.markers[i].label)

for i in range(len(chunk.markers)): 
	ii = i
	if chunk.markers[i].label == "target 122":
		break
		
for k in range(len(chunk.markers)): 
	kk = k
	if chunk.markers[k].label == "target 126":
		break

for m in range(len(chunk.markers)): 
	mm = m
	if chunk.markers[m].label == "target 121":
		break
		
print(ii,chunk.markers[ii].label)
print(kk,chunk.markers[kk].label)
print(mm,chunk.markers[mm].label)

print(chunk.markers[ii].label, "=", chunk.markers[ii].position )
print(chunk.markers[kk].label, "=" ,chunk.markers[kk].position )
print(chunk.markers[mm].label, "=" ,chunk.markers[mm].position )


arr1 = PhotoScan.Vector([0,0,0])
arr2 = PhotoScan.Vector([0,0,0])
arr3 = PhotoScan.Vector([0,0,0])
arr4 = PhotoScan.Vector([0,0,0])

arrmm1 =PhotoScan.Vector([0,0,0])
arrmm2 =PhotoScan.Vector([0,0,0])
arrmm3 =PhotoScan.Vector([0,0,0])
arrmm4 =PhotoScan.Vector([0,0,0])

thang = PhotoScan.Matrix([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
phang = PhotoScan.Matrix([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
omang = PhotoScan.Matrix([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])

for i in range(3):	
	arr1[i] = chunk.markers[kk].position[i]- chunk.markers[ii].position[i]
	arrmm1[i] = chunk.markers[mm].position[i]- chunk.markers[ii].position[i]


thcos = arr1[0]/(math.sqrt(arr1[0]**2+arr1[1]**2))
thsin = arr1[1]/(math.sqrt(arr1[0]**2+arr1[1]**2))


thang = PhotoScan.Matrix([[thcos,thsin,0.],[-thsin,thcos,0.],[0.,0.,1]])
"""
if thsin >= 0.:
	thang = PhotoScan.Matrix([[thcos,-thsin,0.],[thsin,thcos,0.],[0.,0.,1]])

elif thsin < 0.:
	thang = PhotoScan.Matrix([[thcos,abs(thsin),0.],[-abs(thsin),thcos,0.],[0.,0.,1]])
"""

print(thang)

#print(arr*thang)
arr2 = thang*arr1  
arrmm2 = thang*arrmm1 

phcos = arr2[0]/(math.sqrt(arr2[0]**2+arr2[1]**2+arr2[2]**2)) #math.sqrt(arr[0]**2+arr[1]**2+arr[2]**2)
phsin = arr2[2]/(math.sqrt(arr2[0]**2+arr2[1]**2+arr2[2]**2))

phang = PhotoScan.Matrix([[phcos,0.,phsin],[0.,1.,0.],[-phsin,0.,phcos]])
"""
if phsin >= 0.:
	phang = PhotoScan.Matrix([[phcos,0.,-phsin],[0.,1.,0.],[phsin,0.,phcos]])
	
elif phsin < 0.:
	phang = PhotoScan.Matrix([[phcos,0.,abs(phsin)],[0.,1.,0.],[-abs(phsin),0.,phcos]])	
"""

arr3 = phang * arr2
arrmm3 = phang*arrmm2

omcos = arrmm3[1]/(math.sqrt(arrmm3[1]**2+arrmm3[2]**2))
omsin = arrmm3[2]/(math.sqrt(arrmm3[1]**2+arrmm3[2]**2))

omang = PhotoScan.Matrix([[1,0.,0.],[0.,omcos,omsin],[0.,-omsin,omcos]])

"""
if omsin >= 0.:
	omang = PhotoScan.Matrix([[1,0.,0.],[0.,omcos,-omsin],[0.,omsin,omcos]])

elif omsin < 0.:
	omang = PhotoScan.Matrix([[1,0.,0.],[0.,omcos,abs(omsin)],[0.,-abs(omsin), omcos]])
"""

arr4 = omang*arr3
arrmm4 = omang*arrmm3

R = PhotoScan.Matrix([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
scl = chunk.transform.matrix.scale()

R = omang*phang*thang*scl

"""
print("arr")
print(arr1)
print(arr2)
print(arr3)
print(arr4)

print("arrmm")
print(arrmm1)
print(arrmm2)
print(arrmm3)
print(arrmm4)

print(PhotoScan.Matrix.Rotation(R).scale())

"""
#print(rotang)

"""
if chunk.transform.matrix:
	T = chunk.transform.matrix
	s = math.sqrt(T[0,0] ** 2 + T[0,1] ** 2 + T[0,2] ** 2) 		#scaling
	S = PhotoScan.Matrix().Diag([s, s, s, 1]) #scale matrix
else:
	S = PhotoScan.Matrix().Diag([1, 1, 1, 1])
"""

CC = [0,0,0]
for i in range(3):
	CC[i] = chunk.markers[ii].position[i]

ccx = R[0,0]*CC[0] + R[0,1]*CC[1] + R[0,2]*CC[2]
ccy = R[1,0]*CC[0] + R[1,1]*CC[1] + R[1,2]*CC[2]
ccz = R[2,0]*CC[0] + R[2,1]*CC[1] + R[2,2]*CC[2]

"""
print( R[0,0]*arr1[0] + R[0,1]*arr1[1] + R[0,2]*arr1[2]  )
print( R[1,0]*arr1[0] + R[1,1]*arr1[1] + R[1,2]*arr1[2]  )
print( R[2,0]*arr1[0] + R[2,1]*arr1[1] + R[2,2]*arr1[2]  )

print(arr4)

print( R[0,0]*arrmm1[0] + R[0,1]*arrmm1[1] + R[0,2]*arrmm1[2]  )
print( R[1,0]*arrmm1[0] + R[1,1]*arrmm1[1] + R[1,2]*arrmm1[2]  )
print( R[2,0]*arrmm1[0] + R[2,1]*arrmm1[1] + R[2,2]*arrmm1[2]  )

print(arrmm4)

print(ii,chunk.markers[ii].position)
"""

#T = PhotoScan.Matrix( [[R[0,0], R[0,1], R[0,2], C[0]], [R[1,0], R[1,1], R[1,2], C[1]], [R[2,0], R[2,1], R[2,2], C[2]], [0, 0, 0, 1]])
#CCC = PhotoScan.Matrix( [[R[0,0], R[0,1], R[0,2], -CC[0]], [R[1,0], R[1,1], R[1,2], -CC[1]], [R[2,0], R[2,1], R[2,2],- CC[2]], [0, 0, 0, 1]])
#CCC = PhotoScan.Matrix( [[R[0,0], R[0,1], R[0,2], CC[0]], [R[1,0], R[1,1], R[1,2], CC[1]], [R[2,0], R[2,1], R[2,2],CC[2]], [0, 0, 0, 1]])

CCC = PhotoScan.Matrix( [[R[0,0], R[0,1], R[0,2],-ccx], [R[1,0], R[1,1], R[1,2],-ccy], [R[2,0], R[2,1], R[2,2],-ccz], [0, 0, 0, 1]])

#chunk.transform.matrix = S * T.inv() 
#resulting chunk transformation matrix

print(chunk.transform.matrix)

##############################
# transformation matrix handles local coordinate of every chunks.
# every chunks has the transformation matrix and keeping even after file export.
# point loccations of chunks (x,y,z) are not affected.
# marker's scale set scalar component of transformation matrix.
###############################

chunk.transform.matrix = CCC ### 

###############################

print(PhotoScan.ChunkTransform.matrix)
#print(PhotoScan.ChunkTransform.matrix)
chunk.resetRegion()

M = Metashape.Vector( [7.25, 0.75, 0] )
S = chunk.transform.scale
chunk.region.rot = Metashape.Matrix( [[1.0, 0.0, 0], [0, 1, 0], [0.0, 0, 1]] )
chunk.region.rot = CCC.inv().rotation()

chunk.region.center = CCC.inv().mulp(M)

chunk.region.size =  Metashape.Vector([17/S,3/S,2/S])

chunk.buildModel(surface_type = Metashape.SurfaceType.Arbitrary,\
face_count = Metashape.FaceCount.LowFaceCount, source_data= Metashape.DataSource.PointCloudData)

Box = Metashape.BBox()
Box.max = Metashape.Vector((15.5,2))
Box.min = Metashape.Vector((-1, -0.5))
Box.size = 2

R = Metashape.Matrix( [[1.0, 0.0, 0], [0, 1, 0], [0.0, 0, 1]] )#FrontXY

projection = Metashape.OrthoProjection()
projection.type = Metashape.OrthoProjection.Type.Planar
projection.matrix = Metashape.Matrix.Rotation(R)
projection.crs = chunk.crs
#print(R)
print(projection.matrix)

chunk.buildOrthomosaic(surface_data = Metashape.DataSource.ModelData  ,\
projection= projection,region = Box, resolution_x = 0.001, resolution_y = 0.001)

jnamesp = fpath +os.sep+ fnamesp +  ".jpg"
chunk.exportRaster(path=jnamesp, source_data = Metashape.OrthomosaicData,resolution_x=0.002, resolution_y=0.002,\
region = Box )

doc.save()
"""
path = PhotoScan.app.getSaveFileName("Save Project As")
try:
	doc.save(path)
except RuntimeError:
	PhotoScan.app.messageBox("Can't save project")
"""