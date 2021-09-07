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
R = 1.5
r = 0.7

n = 35
halfpi = math.pi/2


def f(u, v):
    theta = v*(2*np.pi)/(n-1)
    phi = u*(2*np.pi)/(n-1)

    x = R*np.cos(phi) + r*np.cos(theta)*np.cos(phi)
    y = R*np.sin(phi) + r*np.cos(theta)*np.sin(phi)
    z = r*np.sin(theta)
    return x, y, z

def draw_torus():
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(n):
        for j in range(n):
            glColor3fv(COLORS[j])
            glVertex3fv(f(i,j))
            glVertex3fv(f(i+1,j))
    glEnd()

def gen_color_list(n_colors, min_value=0, max_value=1):
    colors = []
    for n in range(n_colors):
        colors.append(get_colors(n, min_value, max_value)[:3])
    return colors        

def get_colors(value, min_value=0, max_value=1):
    norm = mpl.colors.Normalize(vmin=0, vmax=max_value)
    # sample the colormaps that you want to use. Use 128 from each so we get 256
    # colors in total
    
    colors2 = cm.get_cmap('plasma').reversed()(np.linspace(0., 1, 128))
    colors1 = cm.get_cmap('plasma')(np.linspace(0., 1, 128))
    
    # combine them and build a new colormap
    colors = np.vstack((colors1, colors2))
    mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
    
    m = cm.ScalarMappable(norm=norm, cmap=mymap)


    vec_color = m.to_rgba(value, alpha=1)
    return vec_color

a = 0
COLORS = gen_color_list(n, 0, n-1)

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


