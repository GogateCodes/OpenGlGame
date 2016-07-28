
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import * # trigonometry
from PIL import Image
import pygame # just to get a display
from pygame.locals import *
import Image
import sys
import time
import math
# import numpy as np
from scipy.interpolate import LinearNDInterpolator
# import psutil

# get an OpenGL surface

pygame.init() 
pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
glEnable(GL_DEPTH_TEST)


glNewList(1,GL_COMPILE)

glBegin(GL_QUADS)

glColor3f(1,1,1)

glNormal3f(0,0,-1)
# glNormal3f(-1,-1,-1)
glVertex3f( -1, -1, -1)
# glNormal3f(1,-1,-1)
glVertex3f(  1, -1, -1)
# glNormal3f(1,1,-1)
glVertex3f(  1,  1, -1)
# glNormal3f(-1,1,-1)
glVertex3f( -1,  1, -1)

glNormal3f(0,0,1)
# glNormal3f(-1,-1,1)
glVertex3f( -1, -1,  1)
# glNormal3f(1,-1,1)
glVertex3f(  1, -1,  1)
# glNormal3f(1,1,1)
glVertex3f(  1,  1,  1)
# glNormal3f(-1,1,1)
glVertex3f( -1,  1,  1)

glNormal3f(0,-1,0)
# glNormal3f(-1,-1,-1)
glVertex3f( -1, -1, -1)
# glNormal3f(1,-1,-1)
glVertex3f( 1, -1, -1)
# glNormal3f(1,-1,1)
glVertex3f(  1, -1,  1)
# glNormal3f(-1,-1,1)
glVertex3f( -1, -1,  1)

glNormal3f(0,1,0)
# glNormal3f(-1,1,-1) 
glVertex3f( -1,  1, -1)
# glNormal3f(1,1,-1)
glVertex3f(  1,  1, -1)
# glNormal3f(1,1,1)
glVertex3f(  1,  1,  1)
# glNormal3f(-1,1,1)
glVertex3f( -1,  1,  1)

glNormal3f(-1,0,0)
# glNormal3f(-1,-1,-1)    
glVertex3f( -1, -1, -1)
# glNormal3f(-1,1,-1)
glVertex3f( -1,  1, -1)
# glNormal3f(-1,1,1)
glVertex3f( -1,  1,  1)
# glNormal3f(-1,-1,1)
glVertex3f( -1, -1,  1)                      

glNormal3f(1,0,0)
# glNormal3f(1,-1,-1)        
glVertex3f(  1, -1, -1)
# glNormal3f(1,1,-1)
glVertex3f(  1,  1, -1)
# glNormal3f(1,1,1)
glVertex3f(  1,  1,  1)
# glNormal3f(1,-1,1)
glVertex3f(  1, -1,  1)

glEnd()
glEndList()

def LoadTerrain(Mesh,NormalData):
	for list in range(0,(len(Mesh))-1):
		for point in range(0,(len(Mesh[list]))-1):

			glBegin(GL_TRIANGLES)

			glNormal3f(NormalData[list][point][0],NormalData[list][point][1],NormalData[list][point][2])
			glVertex3f(list,Mesh[list][point],point)
			glNormal3f(NormalData[list+1][point][0],NormalData[list+1][point][1],NormalData[list+1][point][2])
			glVertex3f((list+1),Mesh[list+1][point],(point))
			glNormal3f(NormalData[list][point+1][0],NormalData[list][point+1][1],NormalData[list][point+1][2])
			glVertex3f(list,Mesh[list][point+1],(point+1))
			
			glNormal3f(NormalData[list+1][point+1][0],NormalData[list+1][point+1][1],NormalData[list+1][point+1][2])
			glVertex3f((list+1),Mesh[list+1][point+1],(point+1))
			glNormal3f(NormalData[list+1][point][0],NormalData[list+1][point][1],NormalData[list+1][point][2])
			glVertex3f((list+1),Mesh[list+1][point],point)
			glNormal3f(NormalData[list][point+1][0],NormalData[list][point+1][1],NormalData[list][point+1][2])
			glVertex3f(list,Mesh[list][point+1],(point+1))
			glEnd()

def CreateMesh():
	# Mesh = [[1.0,0.1,0.2,0.3,0.2,0.2,0.3,1.2,1.5],
			# [0.1,0.2,0.3,0.4,0.5,0.4,0.3,0.2,1.1],
			# [0.1,0.1,0.2,2.2,0.3,0.2,0.3,0.2,0.1],
			# [0.0,0.0,0.1,3.3,3.2,0.1,0.2,0.1,0.1],
			# [0.1,0.0,3.1,3.2,3.2,0.3,0.3,1.2,1.0],
			# [0.0,0.1,0.2,2.3,2.2,1.2,1.3,1.2,1.1],
			# [1.0,0.1,0.2,0.3,1.2,1.2,1.3,1.2,2.1],
			# [1.2,1.3,0.2,0.3,1.3,1.4,1.3,2.2,2.0],
			# [2.4,1.5,0.3,0.4,1.2,1.2,1.5,2.2,2.1]]
	im = Image.open('TerrainTest.jpg','r')		
	pix_val = list(im.getdata())
	flats = []
	scale = 1
	for x in range(len(pix_val)):
		flats.append(pix_val[x][0])
	
	Max = max(flats)
	
	for i in range(len(flats)):
		flats[i] = flats[i]/20
	
	size = sqrt(len(flats))
	
	size = int(size)
	Mesh = []
	count = 0
	for x in range(size):
		Mesh.append([])
	for i in range(size):
		for j in range(size):
			Mesh[i].append(flats[count])
			count += 1
	
	return Mesh 

NormalData = CreateMesh()
Mesh = CreateMesh()


for row in range(0,len(NormalData)):
	for col in range(0,(len(NormalData[row]))):
		NormalData[row][col] = [0,0,0]


for list in range(0,(len(Mesh))-1):
	for point in range(0,(len(Mesh[list]))-1):
		A = [list,Mesh[list][point],point]
		B = [list+1,Mesh[list+1][point],point]
		C = [list,Mesh[list][point+1],point+1]
		
		U = [B[0]-A[0],B[1]-A[1],B[2]-A[2]]
		V = [C[0]-A[0],C[1]-A[1],C[2]-A[2]]
		NormalData[list][point][0] -= (U[1]*V[2])-(U[2]*V[1])
		NormalData[list][point][1] -= (U[2]*V[0])-(U[0]*V[2])
		NormalData[list][point][2] -= (U[0]*V[1])-(U[1]*V[0])
		
		NormalData[list+1][point][0] -= (U[1]*V[2])-(U[2]*V[1])
		NormalData[list+1][point][1] -= (U[2]*V[0])-(U[0]*V[2])
		NormalData[list+1][point][2] -= (U[0]*V[1])-(U[1]*V[0])
		
		NormalData[list][point+1][0] -= (U[1]*V[2])-(U[2]*V[1])
		NormalData[list][point+1][1] -= (U[2]*V[0])-(U[0]*V[2])
		NormalData[list][point+1][2] -= (U[0]*V[1])-(U[1]*V[0])
		
		A = [list+1,Mesh[list+1][point+1],point+1]
		B = [list+1,Mesh[list+1][point],point]
		C = [list,Mesh[list][point+1],point+1]
			
		U = (B[0]-A[0],B[1]-A[1],B[2]-A[2])
		V = (C[0]-A[0],C[1]-A[1],C[2]-A[2])
		# Normal = [(U[1]*V[2])-(U[2]*V[1]),(U[2]*V[0])-(U[0]*V[2]),(U[0]*V[1])-(U[1]*V[0])]
		NormalData[list+1][point+1][0] += (U[1]*V[2])-(U[2]*V[1])
		NormalData[list+1][point+1][1] += (U[2]*V[0])-(U[0]*V[2])
		NormalData[list+1][point+1][2] += (U[0]*V[1])-(U[1]*V[0])
		
		NormalData[list+1][point][0] += (U[1]*V[2])-(U[2]*V[1])
		NormalData[list+1][point][1] += (U[2]*V[0])-(U[0]*V[2])
		NormalData[list+1][point][2] += (U[0]*V[1])-(U[1]*V[0])
		
		NormalData[list][point+1][0] += (U[1]*V[2])-(U[2]*V[1])
		NormalData[list][point+1][1] += (U[2]*V[0])-(U[0]*V[2])
		NormalData[list][point+1][2] += (U[0]*V[1])-(U[1]*V[0])

loop = True
ThirdPerson = True
ToggleJump = False
ice = False

global viewangle
viewangle = 0
vertangle = 1



dist = 5
jumpt = 0
vw = 0
va = 0
vs = 0
vd = 0
vup = 0
prevlookat = [0.1,10,0.1]
lookat = [0.1,10,0.1]
gravity = 0

while loop:
	# prevlookat = lookat
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			# print event.button
			if event.button == 5:
				dist += .5
			if event.button ==4:
				dist -= .5
		if event.type == pygame.K_t:
			ThirdPerson = not ThirdPerson
	keypress = pygame.key.get_pressed()		
	if keypress[pygame.K_LEFT]:
		viewangle += .1
	if keypress[pygame.K_RIGHT]:
		viewangle -= .1
	if keypress[pygame.K_DOWN]:
		if vertangle+0.1 >= (math.pi*0.5):
			vertangle == math.pi*0.5+0.001
		else:
			vertangle += .1
	if keypress[pygame.K_UP]:
		if vertangle-0.1 <= (math.pi*-0.5):
			vertangle == math.pi*-0.5+0.001
		else:
			vertangle -= .1
	
	if keypress[pygame.K_s]:
		vs = 0.25
		lookat[0] += vs*sin(viewangle)
		lookat[2] += vs*cos(viewangle)
	if vs > 0 and ice:
		vs -= 0.01
		lookat[0] += vs*sin(viewangle)
		lookat[2] += vs*cos(viewangle)	
		if abs(vs) <= 0.01:
			vs = 0
	
	if keypress[pygame.K_w]:
		vw = 0.25
		lookat[0] -= vw*sin(viewangle)
		lookat[2] -= vw*cos(viewangle)
	if vw > 0 and ice:
		vw -= 0.01
		lookat[0] -= vw*sin(viewangle)
		lookat[2] -= vw*cos(viewangle)	
		if abs(vw) <= 0.01:
			vw = 0
	
	if keypress[pygame.K_a]:
		va = 0.25
		lookat[0] -= va*sin(viewangle+(math.pi*0.5))
		lookat[2] -= va*cos(viewangle+(math.pi*0.5))
	if va > 0 and ice:
		va -= 0.01
		lookat[0] -= va*sin(viewangle+(math.pi*0.5))
		lookat[2] -= va*cos(viewangle+(math.pi*0.5))
		if abs(va) <= 0.01:
			va = 0
	
	if keypress[pygame.K_d]:
		vd = 0.25
		lookat[0] += vd*sin(viewangle+(math.pi*0.5))
		lookat[2] += vd*cos(viewangle+(math.pi*0.5))
	if vd > 0 and ice:
		vd -= 0.01
		lookat[0] += vd*sin(viewangle+(math.pi*0.5))
		lookat[2] += vd*cos(viewangle+(math.pi*0.5))
		if abs(vd) <= 0.01:
			vd = 0
	
	
	
	if jumpt == 0 and keypress[pygame.K_SPACE]:
		ToggleJump = True
		
	# if ToggleJump:
		gravity = 0
		# gravity = -0.1
		vup = 0.2
		lookat[1] += vup

		ToggleJump = False
		# gravity += 0.01
		vup -= gravity
		lookat[1] += vup		
	else:
		gravity += 0.02 
		vup -= gravity
		lookat[1] += vup
	# if gravity != 0:
		# vup -= 0.1
	
	if keypress[pygame.K_LSHIFT]:
		lookat[1] -= 0.3
	
	xr = [math.floor(lookat[0]),math.ceil(lookat[0])]
	zr = [math.floor(lookat[2]),math.ceil(lookat[2])]
	# print xr,zr
	
	if (lookat[0]-xr[0]) >= (1-(lookat[2]-zr[0])):
		coord = zip([xr[1],xr[1],xr[0]],[zr[1],zr[0],zr[1]])
		ndi = LinearNDInterpolator(coord,[Mesh[int(xr[1])][int(zr[1])],Mesh[int(xr[1])][int(zr[0])],Mesh[int(xr[0])][int(zr[1])]], fill_value=0)
		uv = ndi(lookat[0],lookat[2])
		# print xr[0],zr[0]
		if lookat[1] < uv+0.1:
			lookat[1] = uv+0.1
			gravity = 0
			jumpt = 0
		
			
	else:
		coord = zip([xr[0],xr[1],xr[0]],[zr[0],zr[0],zr[1]])
		ndi = LinearNDInterpolator(coord,[Mesh[int(xr[0])][int(zr[0])],Mesh[int(xr[1])][int(zr[0])],Mesh[int(xr[0])][int(zr[1])]], fill_value=0)
		uv = ndi(lookat[0],lookat[2])
		# print xr[0],zr[0]
		if lookat[1] < uv+0.1:
			lookat[1] = uv+0.1
			gravity = 0
			jumpt = 0
			
			
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(90,1,0.01,1000)
	
	gluLookAt(dist*sin(viewangle)*cos(vertangle)+lookat[0],dist*sin(vertangle)+lookat[1],dist*cos(viewangle)*cos(vertangle)+lookat[2],lookat[0],lookat[1],lookat[2],0,1,0)
    
	glClearColor(0.82, 0.94, 1.0, 0.4)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)
	glColor3f(0.7,0.7,0.7)
	ld=[200,300,400,1]

	glEnable(GL_DEPTH_TEST)
	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_NORMALIZE)
	glDepthFunc(GL_LESS)
	glShadeModel(GL_SMOOTH)
	glClearColor(0.5,0.7, 0.5, 1)
	glMaterial(GL_FRONT, GL_AMBIENT,  [0.2, 0.2, 0.2, 0.2])
	glMaterial(GL_FRONT, GL_DIFFUSE,  [0.8,0.8,0.8,0.2])
	
	glMaterial(GL_FRONT, GL_SPECULAR, (0.4, 0.4, 0.4, 1))
	glMaterial(GL_FRONT, GL_SHININESS, (101))
	
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0.2,0.2,0.2,1])
	glLightfv(GL_LIGHT0, GL_POSITION,  ld)
	
	glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.5, 0.5, 0.5, 1])
	glLight(GL_LIGHT0, GL_AMBIENT,  (0.4,0.4,0.4,0.2))
	glLight(GL_LIGHT0, GL_DIFFUSE,  (0.4,0.4,0.4,0.2))
	glLight(GL_LIGHT0, GL_SPECULAR, (0.4,0.4,0.4,0.2))
    # fallback
	glLoadIdentity()
	
	LoadTerrain(Mesh,NormalData)
	
	if ThirdPerson:
		glColor3f(0.5,1,0)
		glLoadIdentity()
		
		glPushMatrix()
		
		glColor3f(0.5,1,0)	
		glTranslate(lookat[0],lookat[1],lookat[2])
		glRotatef(viewangle*57.2958,0,1,0)
		glScale(0.1,0.1,0.1)
		glCallList(1)
		glPopMatrix()
	elif not ThirdPerson:
		
		dist = 0.1
	

	pygame.display.flip()
