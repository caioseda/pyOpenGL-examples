from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

class Ply:
    def __init__(self, filename):
        self.filename = filename
        self.n_vertex = 0
        self.n_face = 0
        self.property_names = []
        self.property_types = []
        self.end_of_header = 0
        self.vertices = []
        self.faces = []
        
        self.read_ply()

    def show_header(self):
        print(f'Header {self.filename} read.')
        print(f'properties:  {" ".join(self.property_names)}')

    def read_header(self):
        with open(self.filename, 'r') as f:
            line = ''
            linecount = 0
            flag_vertex = False
            while not line.startswith('end_header'):
                line = f.readline()
                linecount += 1
                
                if line.startswith('comment'): continue
                
                if line.startswith('element vertex'):
                    self.n_vertex = int(line.split(' ')[-1])
                    flag_vertex = True

                if flag_vertex and line.startswith('property'):
                    splitted = line.strip('\n').split(' ')
                    self.property_names.append(splitted[-1])
                    self.property_types.append(splitted[1])

                if line.startswith('element face'):
                    self.n_face = int(line.split(' ')[-1])
                    flag_vertex = False
            
            self.end_of_header = linecount
            self.show_header()

    def read_vertices(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()

            begin = self.end_of_header
            end = self.end_of_header + self.n_vertex

            for line in lines[begin:end]:
                properties = {}
                properties_values = line.split(' ')
                for i, prop in enumerate(self.property_names):
                    
                    if self.property_types[i] == 'float':
                        cast = float
                    else:
                        cast = int

                    properties[prop] = cast(properties_values[i])
                
                self.vertices.append(properties)
            print(f'Read {len(self.vertices)} vertices.')

    def read_faces(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()

            begin = self.end_of_header + self.n_vertex
            end = self.end_of_header + self.n_vertex + self.n_face

            for line in lines[begin:end]:
                faces_coord = line.split(' ')
                self.faces.append([*map(int, faces_coord[1:])])
            self.vertices_per_face = int(faces_coord[0])
            print(f'Read {len(self.faces)} faces.')

    def read_ply(self):
        self.read_header()
        self.read_vertices()
        self.read_faces()

    def draw(self):
        if self.vertices_per_face == 2:
            primitive = GL_LINES
        elif self.vertices_per_face == 3:
            primitive = GL_TRIANGLES
        elif self.vertices_per_face == 4:
            primitive = GL_QUADS
        elif self.vertices_per_face > 4:
            primitive = GL_POLYGON
        
        for face in self.faces:
            glBegin(primitive)
            for vertice in face:
                v = self.vertices[vertice]
                glNormal3f(v['nx'], v['ny'], v['nz'])
                glColor3f(v['red']/255, v['green']/255, v['blue']/255)
                glVertex3f(v['x'], v['y'], v['z'])
            glEnd()

