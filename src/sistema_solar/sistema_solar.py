from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import util.png as png
import numpy as np
from solar_object import SolarObject
# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = b'\033'

# Path
TEXTURE_PATHS = {
    'terra': '../assets/2k_earth.png',
    'sol': '../assets/2k_sun.png',
    'lua': '../assets/2k_moon.png',
}

# Number of the glut window.
window = 0

# Rotations for cube. 
xrot = yrot = zrot = 0
dx = 1
dy = 1
dz = 0

def setup_solar_system(textures):
    sol = SolarObject(textures['sol'], 1, rotation_speed=2, clockwise=False)
    terra = SolarObject(textures['terra'], 0.5, rotation_speed=6)
    lua = SolarObject(textures['lua'], 0.2, rotation_speed=10)

    terra.add_in_orbit(lua, distance=2, speed=10)
    sol.add_in_orbit(terra, distance=5, speed=6)
    return sol

def LoadTextures():
    textures_ids = glGenTextures(len(TEXTURE_PATHS)) 

    textures = {}
    for i, (texture_name, texture_path) in enumerate(TEXTURE_PATHS.items()):
        glBindTexture(GL_TEXTURE_2D, textures_ids[i])
        reader = png.Reader(filename=texture_path)
        w, h, pixels, metadata = reader.read_flat()
        if(metadata['alpha']):
            modo = GL_RGBA
        else:
            modo = GL_RGB
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        textures[texture_name] = textures_ids[i]
    return textures

def InitGL(Width, Height):             
    global SOLAR_SYSTEM
    textures =  LoadTextures()
    SOLAR_SYSTEM = setup_solar_system(textures)
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

a = 0
def DrawGLScene():
    global xrot, yrot, zrot

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()                   
    glClearColor(0,0,0,1.0)

    glTranslatef(0.0,0,-15)
    glRotatef(xrot,1.0,0.0,0.0)          
    glRotatef(yrot,0.0,1.0,0.0)           
    glRotatef(zrot,0.0,0.0,1.0) 
    
    # glBindTexture(GL_TEXTURE_2D, texture[0])
    SOLAR_SYSTEM.play()
    glutSwapBuffers()
    # draw_esfera()S
    # xrot = xrot + dx                 # X rotation
    # yrot = yrot + dy                 # Y rotation
    # zrot = zrot + dz                 # Z rotation
    
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
    glutCreateWindow("Sistema Solar")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(teclaEspecialPressionada)
    InitGL(640, 480)
    glutMainLoop()


main()
