#coding:utf-8
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def display():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    gluLookAt(0,4,10,  0,0,0,  0,1,0)
    glRotatef(-40, 0.0, 1.0, 0.0)
    glColor3f(float(0xbb)/0xff, float(0xdd)/0xff, 0xff/0xff)
    glutSolidCube(3.5)
    glPopMatrix()
    glFlush()

def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(200, 200)
    glutCreateWindow('pyopengl')
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutMainLoop()


reshape(20, 30)