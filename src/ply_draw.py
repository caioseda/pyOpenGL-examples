from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from util.PlyReader import Ply

x = 20
a = 0
def display():
    global ply, x, a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    
    glPushMatrix()
    glRotatef(a-10,0,1,1)
    ply.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslate(15,0,0)
    glRotatef(a,1,0,1)
    ply.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslate(-15,0,0)
    glRotatef(a+10,1,1,0)
    ply.draw()
    glPopMatrix()


    glutSwapBuffers()


    a += 2
    x = x-1

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,200.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,1,40,0,0,0,0,1,0)

def init():
    global ply

    glLightfv(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.6, 0.6, 0.6, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    ply = Ply("../assets/banana.ply")

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Ply")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()
