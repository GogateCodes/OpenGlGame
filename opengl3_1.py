from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import * # trigonometry

import pygame # just to get a display
from pygame.locals import *
import Image
import sys
import time

# get an OpenGL surface

pygame.init() 
pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
glEnable(GL_DEPTH_TEST)
# glEnable(GL_NORMALIZE)

def createAndCompileShader(type,source):
    shader=glCreateShader(type)
    glShaderSource(shader,source)
    glCompileShader(shader)

    # get "compile status" - glCompileShader will not fail with 
    # an exception in case of syntax errors

    result=glGetShaderiv(shader,GL_COMPILE_STATUS)

    if (result!=1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
    return shader

glShadeModel(GL_SMOOTH)
vertex_shader=createAndCompileShader(GL_VERTEX_SHADER,"""
varying vec3 N;
varying vec3 v;

void main(void)
{

   v = vec3(gl_ModelViewMatrix * gl_Vertex);       
   N = normalize(gl_NormalMatrix * gl_Normal);
   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
""");
fragment_shader=createAndCompileShader(GL_FRAGMENT_SHADER,"""
varying vec3 N;
varying vec3 v;

void main(void)
{
   vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
   vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(N,L), 0.0);  
   Idiff = clamp(Idiff, 0.0, 1.0); 

   gl_FragColor = Idiff;
}
""");

#program=glCreateProgram()
#glAttachShader(program,vertex_shader)
#glAttachShader(program,fragment_shader)
#glLinkProgram(program)

#try:
#    glUseProgram(program)   
#except OpenGL.error.GLError:
#    print glGetProgramInfoLog(program)
#    raise

glNewList(1,GL_COMPILE)

glBegin(GL_QUADS)

glColor3f(1,1,1)

glNormal3f(0,0,-1)
glVertex3f( -1, -1, -1)
glVertex3f(  1, -1, -1)
glVertex3f(  1,  1, -1)
glVertex3f( -1,  1, -1)

glNormal3f(0,0,1)
glVertex3f( -1, -1,  1)
glVertex3f(  1, -1,  1)
glVertex3f(  1,  1,  1)
glVertex3f( -1,  1,  1)

glNormal3f(0,-1,0) 
glVertex3f( -1, -1, -1)
glVertex3f(  1, -1, -1)
glVertex3f(  1, -1,  1)
glVertex3f( -1, -1,  1)

glNormal3f(0,1,0) 
glVertex3f( -1,  1, -1)
glVertex3f(  1,  1, -1)
glVertex3f(  1,  1,  1)
glVertex3f( -1,  1,  1)

glNormal3f(-1,0,0)     
glVertex3f( -1, -1, -1)
glVertex3f( -1,  1, -1)
glVertex3f( -1,  1,  1)
glVertex3f( -1, -1,  1)                      

glNormal3f(1,0,0)        
glVertex3f(  1, -1, -1)
glVertex3f(  1,  1, -1)
glVertex3f(  1,  1,  1)
glVertex3f(  1, -1,  1)

glEnd()
glEndList()

Mesh = [[1.0,0.1,0.2,0.3,0.2,0.2,0.3,1.2,1.5],
        [0.1,0.2,0.3,0.4,0.5,0.4,0.3,0.2,1.1],
        [0.1,0.1,0.2,0.2,0.3,0.2,0.3,0.2,0.1],
        [0.0,0.0,0.1,0.1,0.2,0.1,0.2,0.1,0.1],
        [0.1,0.0,0.1,0.2,0.2,0.3,0.3,1.2,1.0],
        [0.0,0.1,0.2,0.3,0.2,1.2,1.3,1.2,1.1],
        [1.0,0.1,0.2,0.3,1.2,1.2,1.3,1.2,2.1],
        [1.2,1.3,0.2,0.3,1.3,1.4,1.3,2.2,2.0],
        [2.4,1.5,0.3,0.4,1.2,1.2,1.5,2.2,2.1]]

t = 0
global viewangle
viewangle = 0
t = 0
done = False
dist = 4
while not done:
	t += .1
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(90,1,0.01,1000)
	
	gluLookAt(dist*sin(viewangle),4*dist*sin(0.3),dist*cos(viewangle),0,0,0,0,1,0)
    
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)

    # calculate light source position

	ld=[-2,5,-2]

    # pass data to fragment shader
	# glMatrixMode(GL_PROJECTION)
	# glLoadIdentity()
	# gluPerspective(31, float(screen_px[0])/screen_px[1],0.1, 1000)
	# glMatrixMode(GL_MODELVIEW)
	# glLoadIdentity()
	# gluLookAt(0,0,0,0,0,-1,0,1,0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glDepthFunc(GL_LESS)
	glShadeModel(GL_SMOOTH)
	glClearColor(0.5, 0.5, 1, 1)
	glMaterial(GL_FRONT, GL_AMBIENT,  (0.5, 0.5, 0.5, 1))
	glMaterial(GL_FRONT, GL_DIFFUSE,  (0.8,0.8,0.8,0.8))
	glMaterial(GL_FRONT, GL_SPECULAR, (0.4, 0.4, 0.4, 1))
	glMaterial(GL_FRONT, GL_SHININESS, (128))
	glLight(GL_LIGHT0, GL_POSITION,  (100, 100, 0, 10))
	glLight(GL_LIGHT0, GL_AMBIENT,  (0.4,0.4,0.4,0.4))
	glLight(GL_LIGHT0, GL_DIFFUSE,  (0.4,0.4,0.4,0.4))
	# glLight(GL_LIGHT0, GL_SPECULAR, (0.4,0.4,0.4,0.4))
    # fallback
	glLoadIdentity()
	
	glTranslate(len(Mesh)/-2,-1,len(Mesh)/-2)
	
	for list in range((len(Mesh))-1):
		for point in range((len(Mesh[list]))-1):

			glBegin(GL_TRIANGLES)

			A = [list,Mesh[list][point],point]
			B = [list+1,Mesh[list+1][point],point]
			C = [list,Mesh[list][point+1],point+1]
			
			U = [B[0]-A[0],B[1]-A[1],B[2]-A[2]]
			V = [C[0]-A[0],C[1]-A[1],C[2]-A[2]]
			Normal = [(U[1]*V[2])-(U[2]*V[1]),(U[2]*V[0])-(U[0]*V[2]),(U[0]*V[1])-(U[1]*V[0])]
			glNormal3f(-1*Normal[0],-1*Normal[1],-1*Normal[2])
			glVertex3f(list,Mesh[list][point],point)
			glVertex3f(list+1,Mesh[list+1][point],point)
			glVertex3f(list,Mesh[list][point+1],point+1)
			
			A = [list+1,Mesh[list+1][point+1],point+1]
			B = [list+1,Mesh[list+1][point],point]
			C = [list,Mesh[list][point+1],point+1]
			
			U = [B[0]-A[0],B[1]-A[1],B[2]-A[2]]
			V = [C[0]-A[0],C[1]-A[1],C[2]-A[2]]
			Normal = [(U[1]*V[2])-(U[2]*V[1]),(U[2]*V[0])-(U[0]*V[2]),(U[0]*V[1])-(U[1]*V[0])]
			glNormal3f(Normal[0],Normal[1],Normal[2])
			glVertex3f(list+1,Mesh[list+1][point+1],point+1)
			glVertex3f(list+1,Mesh[list+1][point],point)
			glVertex3f(list,Mesh[list][point+1],point+1)
			glEnd()
			
	
	glColor3f(1,1,1)
	
	glLoadIdentity()
    # if pygame.event.get() == 

    
	glPushMatrix()
    
	glTranslate(0,0,0)
	# glScale(0.1,0.1,0.1)
	glCallList(1)
	glPopMatrix()
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
	keypress = pygame.key.get_pressed()		
	if keypress[pygame.K_LEFT]:
		viewangle -= .01
	if keypress[pygame.K_RIGHT]:
		viewangle += .01
	
	# scroll = pygame.event.poll()
	# #print scroll
	# if scroll.type == pygame.MOUSEBUTTONDOWN:
		
		# if scroll.button == 4:
			# dist += 1
		# if scroll.button ==5:
			# dist -= 1
	pygame.display.flip()
