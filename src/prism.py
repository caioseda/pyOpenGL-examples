from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

### INTERACTION
# UP ARROW : Increase number of sides
# DOWN ARROW : Descrease number of sides
N_SIDES = 3

HEIGHT = 5
RADIUS = 2

def prism_base(height=0, n_sides=3, radius = 1):
    vertices = []
    
    d_angle = 2*np.pi / n_sides
    p0 = np.array([radius,height,0])

    angle = 0
    glBegin(GL_LINE_STRIP)
    glVertex3fv(p0)
    for i in range(n_sides):
        # (x,z) 
        # y -> z
        angle += d_angle

        x = np.cos(angle)*p0[0] - np.sin(angle)*p0[2]
        z = np.sin(angle)*p0[0] + np.cos(angle)*p0[2]
        
        new_p = np.array([x, height, z])
        glVertex3fv(new_p)
        vertices.append(new_p)
    
    # if n_sides is odd, complete base
    if n_sides % 2 == 1:
        glVertex3fv(p0)
    glEnd()

    return vertices

def draw_prism(height, n_sides, radius):
    
    bottom_base = prism_base(-height/2,n_sides,radius)
    upper_base = prism_base(height/2,n_sides,radius)

    for p1,p2 in zip(bottom_base, upper_base):
        glBegin(GL_LINES)
        glVertex3fv(p1)
        glVertex3fv(p2)
        glEnd()

a = 0
def draw():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    draw_prism(height=HEIGHT,n_sides=N_SIDES,radius=RADIUS)

    glutSwapBuffers()
    a = 1
    glRotatef(a,1,1,0)
    # a += .5
 
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def keyPressed(key, x, y):
    global N_SIDES
    if key == GLUT_KEY_UP:
        N_SIDES += 1

    elif key == GLUT_KEY_DOWN:
        if N_SIDES > 3:
            N_SIDES -= 1

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800,800)
glutCreateWindow("Prism")
glutDisplayFunc(draw)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,800.0/800.0,0.1,100.0)
glutSpecialFunc(keyPressed)
glTranslatef(0.0,0.0,-15)
glutTimerFunc(50,timer,1)
glutMainLoop()


