from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

### INTERACTION
# UP ARROW : Increase number of sides
# DOWN ARROW : Descrease number of sides
x0 = -1
xn = 1

y0 = -1
yn = 1

n = 50
dx = (xn - x0)/n
dy = (yn - y0)/n

def f_dx(x, y):
    return 2*x
def f_dy(x, y):
    return 2*y

def f2(x,y):
    return x**3

def f(x,y):
    glNormal3fv(calculaNormalFace(x,y))
    return x**2 + y**2

def calculaNormalFace(xv, yv):
    x=0
    y=1
    z=2
    U = (1, 0, f_dx(xv, yv))
    V = (0, 1, f_dy(xv, yv))
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = np.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)


def draw_functions(func = lambda x, y: x+y):
    y = y0

    for i in range(n):
        x = x0
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(n): 

            # glColor3fv(get_color(j/(n-1), color1, color2))
            
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

    glRotatef(-a,1,1,0)
    draw_functions(func = f)
    
    glPopMatrix()
    glutSwapBuffers()
    a += 1
 
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera Virtual
    #          onde    Pra onde 
    gluLookAt( 10,0,0, 0,0,0,     0,1,0 )

def init():
    mat_ambient = (0.4, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (10, 0, 0)
    glClearColor(0.0,0.0,0.0,0.0)
#    glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Funcao implicita iluminada")
    glutReshapeFunc(reshape)
    glutDisplayFunc(draw)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()

