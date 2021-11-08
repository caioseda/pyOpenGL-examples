from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import math



### INTERACTION
# UP ARROW : Increase outter circle radius
# DOWN ARROW : Decrease outter circle radius
# RIGHT ARROW : Increase inner circle radius
# LEFT ARROW : Decrease inner circle radius

# outter circle - R
# inner circle - r
n = 50
halfpi = math.pi/2
def f(u, v):
    theta = v*(2*np.pi)/(n-1) - halfpi
    phi = u*(2*np.pi)/(n-1)

    x = np.cos(theta)*np.cos(phi)
    y = np.cos(theta)*np.sin(phi)
    z = np.sin(theta)
    return x, y, z

def draw_torus():
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(n):
        for j in range(n):
            glVertex3fv(f(i,j))
            glVertex3fv(f(i+1,j))
    glEnd()

a = 0
def draw():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a,0,-1,1)
    draw_torus()    
    glPopMatrix()
    glutSwapBuffers()
    a += 2
 
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def keyPressed(key, x, y):
    global R, r
    if key == GLUT_KEY_UP:
        R += .1
        
    elif key == GLUT_KEY_DOWN:
        if R > 0.1:
            R -= .1
    elif key == GLUT_KEY_RIGHT:
        r += .1
        
    elif key == GLUT_KEY_LEFT:
        if r > 0.2:
            r -= .1

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800,800)
glutCreateWindow("Torus")
glutDisplayFunc(draw)
glutSpecialFunc(keyPressed)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,800.0/800.0,0.1,100.0)
glTranslatef(0.0,0.0,-8)
glutTimerFunc(50,timer,1)
glutMainLoop()


