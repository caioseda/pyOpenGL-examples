from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

x0 = -1
xn = 1

y0 = -1
yn = 1

n = 50
dx = (xn - x0)/n
dy = (yn - y0)/n

color1 = np.array([45,154,248])/255
color2 = np.array([45,248,119])/255

def f2(x,y):
    return 2*x*y

def f(x,y):
    return np.sin(x+y)**3

def get_color(t, c1 = np.array([1,0,0]), c2 = np.array([0,0,1])):
    return c1 + t*(c2 - c1)    

def draw_functions(func = lambda x, y: x+y):
    y = y0

    for i in range(n):
        x = x0
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(n): 

            glColor3fv(get_color(j/(n-1), color1, color2))
            glVertex3f(x, y, func(x, y))
            glVertex3f(x, y + dy, func(x, y + dy))
            x = x0 + j*dx
        
        glEnd()
        y = y0 + i*dx

a = 0
def draw():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    glTranslate(0, 3, 0)
    glRotatef(-a,1,1,0)
    draw_functions(func = f)
    
    glPopMatrix()
    glPushMatrix()

    glTranslate(0, -3, 0)
    glRotatef(-a,-1,-1,0)
    draw_functions(func = f2)
    
    glPopMatrix()
    glutSwapBuffers()
    a += 1
 
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800,800)
glutCreateWindow("Implicit function")
glutDisplayFunc(draw)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,1,0.1,100.0)
glTranslatef(0.0,0.0,-15)
glutTimerFunc(50,timer,1)
glutMainLoop()


