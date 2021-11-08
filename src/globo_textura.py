from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import util.png as png
import numpy as np

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = b'\033'

# Path
TEXTURE_PATH = '../assets/mapa_mundi.png'

# Number of the glut window.
window = 0

# Rotations for cube. 
xrot = yrot = zrot = 0
dx = 1
dy = 1
dz = 0

RAIO = 3
N_POINTS = 50
# texture = []

def LoadTextures():
    global texture
    texture = [ glGenTextures(1) ]

    ################################################################################
    glBindTexture(GL_TEXTURE_2D, texture[0])
    reader = png.Reader(filename=TEXTURE_PATH)
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    ################################################################################


def InitGL(Width, Height):             
    LoadTextures()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glShadeModel(GL_SMOOTH)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
    if Height == 0:                        
        Height = 1
    glViewport(0, 0, Width, Height)      
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
    global xrot, yrot, zrot, texture

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()                   
    glClearColor(0,0,0,1.0)

    glTranslatef(0.0,0.0,-10)
    glRotatef(xrot,1.0,0.0,0.0)          
    glRotatef(yrot,0.0,1.0,0.0)           
    glRotatef(zrot,0.0,0.0,1.0) 
    
    glBindTexture(GL_TEXTURE_2D, texture[0])
    
    draw_esfera()
    xrot = xrot + dx                 # X rotation
    yrot = yrot + dy                 # Y rotation
    zrot = zrot + dz                 # Z rotation

    glutSwapBuffers()

def f(u, v):
    theta = v*(np.pi)/(N_POINTS-1) - np.pi/2
    phi = u*(2*np.pi)/(N_POINTS-1)

    x = RAIO*np.cos(theta)*np.cos(phi)
    y = RAIO*np.cos(theta)*np.sin(phi)
    z = RAIO*np.sin(theta)
    return x, y, z


def draw_esfera():
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N_POINTS):
        for j in range(N_POINTS):
            # N-POINTS - i serve para compensar o texto ao contrário
            # que ocorre devido a forma como a textura é aplicada.
            # Dessa forma, os textos não ficam invertidos.
            glTexCoord2f((N_POINTS-i)/(N_POINTS-1), j/(N_POINTS-1))
            glVertex3fv(f(i,j))
            glTexCoord2f((N_POINTS-(i+1))/(N_POINTS-1), j/(N_POINTS-1))
            glVertex3fv(f(i+1,j))
    glEnd()

def keyPressed(tecla, x, y):
    global dx, dy, dz

    if tecla == ESCAPE:
        glutLeaveMainLoop()
    elif tecla == b'x' or tecla == b'X':
        dx = 1.0
        dy = 0
        dz = 0   
    elif tecla == b'y' or tecla == b'Y':
        dx = 0
        dy = 1.0
        dz = 0   
    elif tecla == b'z' or tecla == b'Z':
        dx = 0
        dy = 0
        dz = 1.0

def teclaEspecialPressionada(tecla, x, y):
    global xrot, yrot, zrot, dx, dy, dz
    if tecla == GLUT_KEY_LEFT:
        print ("ESQUERDA")
        yrot -= dy                
    elif tecla == GLUT_KEY_RIGHT:
        print ("DIREITA")
        yrot += dy       
    elif tecla == GLUT_KEY_UP:
        print ("CIMA")
        xrot -= dx
    elif tecla == GLUT_KEY_DOWN:
        print ("BAIXO")
        xrot += dx

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)    
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0,0)
    glutCreateWindow("Globo com textura")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(teclaEspecialPressionada)
    InitGL(640, 480)
    glutMainLoop()


main()
