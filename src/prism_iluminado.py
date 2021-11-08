from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

### INTERACTION
# UP ARROW : Increase number of sides
# DOWN ARROW : Descrease number of sides
N_SIDES = 16

HEIGHT = 4
RADIUS = 1.5

def calculaNormalFace(vertices):
    x = 0
    y = 1
    z = 2
    v0 = vertices[0]
    v1 = vertices[1]
    v2 = vertices[2]
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = np.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)


def prism_base(height=0, n_sides=3, radius = 1):
    vertices = []
    
    d_angle = 2*np.pi / n_sides
    p0 = np.array([radius,height,0])

    angle = 0
    for i in range(n_sides):
        # (x,z) 
        # y -> z
        angle += d_angle

        x = np.cos(angle)*p0[0] - np.sin(angle)*p0[2]
        z = np.sin(angle)*p0[0] + np.cos(angle)*p0[2]
        
        new_p = np.array([x, height, z])
        vertices.append(new_p)

    return vertices

def draw_base(face):
    glNormal3fv(calculaNormalFace(face))
    glBegin(GL_POLYGON)
    for vertice in face:
        glVertex3fv(vertice)
    glEnd()

def draw_prism(height, n_sides, radius):

    bottom_base = prism_base(-height/2,n_sides,radius)
    upper_base = prism_base(height/2,n_sides,radius)
    faces = []
    
    #draw top and bottom base
    draw_base(bottom_base)
    draw_base(upper_base)

    # draw sides
    for i in range(n_sides):

        glBegin(GL_QUADS)
        p0 = bottom_base[i]
        p1 = bottom_base[(-n_sides + (i+1))]
        p2 = upper_base[(-n_sides + (i+1))]
        p3 = upper_base[i]

        faces.append([p0, p1, p2, p3])

        glNormal3fv(calculaNormalFace(faces[i]))

        for vertice in faces[i]:
            glVertex3fv(vertice)

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
        print(f'CIMA - N LADOS : {N_SIDES}')

    elif key == GLUT_KEY_DOWN:
        if N_SIDES > 3:
            N_SIDES -= 1
            print(f'BAIXO - N LADOS : {N_SIDES}')

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
    mat_ambient = (0.3, 0.1, 0.6, 1.0)
    mat_diffuse = (0.6, 0.0, 1, 1.0)
    mat_specular = (0.8, 0.5, 1, 1.0)
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
    print('Use SETA CIMA e SETA BAIXO para alterar o número de faces.')
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Prisma iluminado")
    glutReshapeFunc(reshape)
    glutDisplayFunc(draw)
    glutSpecialFunc(keyPressed)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()

