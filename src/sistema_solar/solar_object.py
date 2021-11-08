from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import util.png as png
import numpy as np


class SolarObject():
    def __init__(self, texture, radius, rotation_speed=1, rotation_vector=[0,1,0], n_points=50, clockwise=True) -> None:
        self.radius = radius
        self.n_points = n_points
        self.in_orbit = []
        self.texture = texture

        self.rotation_vector = rotation_vector
        self.rotation_speed = rotation_speed
        self.clockwise = clockwise

        self.angle_rotation = 0
        self.angle_revolution = 0

    def sphere(self, u: int, v: int):
        theta = v*(np.pi)/(self.n_points-1) - np.pi/2
        phi = u*(2*np.pi)/(self.n_points-1)

        x = self.radius*np.cos(theta)*np.cos(phi)
        y = self.radius*np.cos(theta)*np.sin(phi)
        z = self.radius*np.sin(theta)
        return x, y, z

    def draw(self):
        glPushMatrix()
        glRotatef(self.angle_rotation, *self.rotation_vector)
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(self.n_points):
            for j in range(self.n_points):
                # N-POINTS - i serve para compensar o texto ao contrário
                # que ocorre devido a forma como a textura é aplicada.
                # Dessa forma, os textos não ficam invertidos.
                glTexCoord2f((self.n_points-i)/(self.n_points-1), j/(self.n_points-1))
                glVertex3fv(self.sphere(i,j))
                glTexCoord2f((self.n_points-(i+1))/(self.n_points-1), j/(self.n_points-1))
                glVertex3fv(self.sphere(i+1,j))
        glEnd()
        glPopMatrix()
        if self.clockwise:
            self.angle_rotation += self.rotation_speed
        else:
            self.angle_rotation -= self.rotation_speed

    def draw_in_orbit(self):
        # TODO: implement only distance
        if self.in_orbit:
            for each in self.in_orbit:
                glPushMatrix()
                glRotatef(self.angle_revolution,*[0,1,0,])
                glTranslatef(each['distance'],0,0)
                each['object'].play()
                glPopMatrix()

                self.angle_revolution += each['speed']
                

    def add_in_orbit(self, object, speed=1, distance=None):
            self.in_orbit.append({
                    'object': object,
                    'distance': distance,
                    'speed': speed
                })

    def play(self):
        self.draw()
        self.draw_in_orbit()