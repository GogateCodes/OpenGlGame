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

# get an OpenGL surface

pygame.init() 
pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
glEnable(GL_DEPTH_TEST)
# glEnable(GL_NORMALIZE)

def create_object(shader):
    # Create a new VAO (Vertex Array Object) and bind it
	vertex_array_object = GL.glGenVertexArrays(1)
	glBindVertexArray( vertex_array_object )
    
    # Generate buffers to hold our vertices
	vertex_buffer = GL.glGenBuffers(1)
	glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)
    
    # Get the position of the 'position' in parameter of our shader and bind it.
	position = glGetAttribLocation(shader, 'position')
	glEnableVertexAttribArray(position)
    
    # Describe the position data layout in the buffer
	glVertexAttribPointer(position, 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))
    
    # Send the data over to the buffer
	glBufferData(GL.GL_ARRAY_BUFFER, 48, vertices, GL.GL_STATIC_DRAW)
    
    # Unbind the VAO first (Important)
	glBindVertexArray( 0 )
    
    # Unbind other stuff
	glDisableVertexAttribArray(position)
	GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
	return vertex_array_object


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

program=glCreateProgram()
glAttachShader(program,vertex_shader)
glAttachShader(program,fragment_shader)
glLinkProgram(program)

# try:
    # glUseProgram(program)   
# except OpenGL.error.GLError:
    # print glGetProgramInfoLog(program)
    # raise

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
glVertex3f(  1, -1, -1)
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

# glNormal3f(1,0,0)
glNormal3f(1,-1,-1)        
glVertex3f(  1, -1, -1)
glNormal3f(1,1,-1)
glVertex3f(  1,  1, -1)
glNormal3f(1,1,1)
glVertex3f(  1,  1,  1)
glNormal3f(1,-1,1)
glVertex3f(  1, -1,  1)

glEnd()
glEndList()

def CreateMesh():
	Mesh = [[1.0,0.1,0.2,0.3,0.2,0.2,0.3,1.2,1.5],
			[0.1,0.2,0.3,0.4,0.5,0.4,0.3,0.2,1.1],
			[0.1,0.1,0.2,2.2,0.3,0.2,0.3,0.2,0.1],
			[0.0,0.0,0.1,3.3,3.2,0.1,0.2,0.1,0.1],
			[0.1,0.0,3.1,3.2,3.2,0.3,0.3,1.2,1.0],
			[0.0,0.1,0.2,2.3,2.2,1.2,1.3,1.2,1.1],
			[1.0,0.1,0.2,0.3,1.2,1.2,1.3,1.2,2.1],
			[1.2,1.3,0.2,0.3,1.3,1.4,1.3,2.2,2.0],
			[2.4,1.5,0.3,0.4,1.2,1.2,1.5,2.2,2.1]]
	im = Image.open('Volcano.jpg','r')		
	pix_val = list(im.getdata())
	# print len(pix_val)
	flats = []
	scale = 1
	for x in range(len(pix_val)):
		flats.append(pix_val[x][0])
	# print len(flats)
	Max = max(flats)
	# print(Max)
	for i in range(len(flats)):
		flats[i] = flats[i]/10
		# flats[i] *= scale
	# print flats
	
	
	size = sqrt(len(flats))
	# print size
	size = int(size)
	Mesh = []
	count = 0
	for x in range(size):
		Mesh.append([])
	for i in range(size):
		for j in range(size):
			Mesh[i].append(flats[count])
			count += 1
	# print max(Mesh)
	return Mesh 

NormalData = CreateMesh()
Mesh = CreateMesh()
# print Mesh
for row in range(0,len(NormalData)):
	for col in range(0,(len(NormalData[row]))):
		NormalData[row][col] = [0,0,0]

# print NormalData
# print len(Mesh[0])
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
	
		
t = 0
global viewangle
viewangle = 0
vertangle = 0
t = 0
done = False
dist = 20
while not done:
	t += .1
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(90,1,0.01,1000)
	
	gluLookAt(dist*sin(viewangle)*cos(vertangle),dist*sin(vertangle),dist*cos(viewangle)*cos(vertangle),0,0,0,0,1,0)
    
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)

    # calculate light source position

	ld=[200,300,400,1]

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
	glEnable(GL_NORMALIZE)
	glDepthFunc(GL_LESS)
	glShadeModel(GL_SMOOTH)
	glClearColor(0.2,0.2, 0.2, 1)
	glMaterial(GL_FRONT, GL_AMBIENT,  [0.2, 0.2, 0.2, 0.4])
	glMaterial(GL_FRONT, GL_DIFFUSE,  [0.8,0.8,0.8,0.4])
	# glMaterial(GL_FRONT, GL_SPECULAR, (0.4, 0.4, 0.4, 1))
	# glMaterial(GL_FRONT, GL_SHININESS, (128))
	
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0.2,0.2,0.2,1])
	# glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.5, 0.5, 0.5, 1])
	glLightfv(GL_LIGHT0, GL_POSITION,  ld)
	# glLight(GL_LIGHT0, GL_AMBIENT,  (0.4,0.4,0.4,0.4))
	# glLight(GL_LIGHT0, GL_DIFFUSE,  (0.4,0.4,0.4,0.4))
	# glLight(GL_LIGHT0, GL_SPECULAR, (0.4,0.4,0.4,0.4))
    # fallback
	glLoadIdentity()
	
	glTranslate(len(Mesh)/-2,0,len(Mesh)/-2)
	
	for list in range(0,(len(Mesh))-1):
		for point in range(0,(len(Mesh[list]))-1):

			glBegin(GL_TRIANGLES)

			glNormal3f(NormalData[list][point][0],NormalData[list][point][1],NormalData[list][point][2])
			glVertex3f(list,Mesh[list][point],point)
			glNormal3f(NormalData[list+1][point][0],NormalData[list+1][point][1],NormalData[list+1][point][2])
			glVertex3f(list+1,Mesh[list+1][point],point)
			glNormal3f(NormalData[list][point+1][0],NormalData[list][point+1][1],NormalData[list][point+1][2])
			glVertex3f(list,Mesh[list][point+1],point+1)
			
			glNormal3f(NormalData[list+1][point+1][0],NormalData[list+1][point+1][1],NormalData[list+1][point+1][2])
			glVertex3f(list+1,Mesh[list+1][point+1],point+1)
			glNormal3f(NormalData[list+1][point][0],NormalData[list+1][point][1],NormalData[list+1][point][2])
			glVertex3f(list+1,Mesh[list+1][point],point)
			glNormal3f(NormalData[list][point+1][0],NormalData[list][point+1][1],NormalData[list][point+1][2])
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
		viewangle -= .1
	if keypress[pygame.K_RIGHT]:
		viewangle += .1
	if keypress[pygame.K_UP]:
		vertangle += .1
		# viewangle += viewangle
	if keypress[pygame.K_DOWN]:
		vertangle -= .1
		# viewangle += viewangle
	# scroll = pygame.event.poll()
	# #print scroll
	# if scroll.type == pygame.MOUSEBUTTONDOWN:
		
		# if scroll.button == 4:
			# dist += 1
		# if scroll.button ==5:
			# dist -= 1
	pygame.display.flip()
