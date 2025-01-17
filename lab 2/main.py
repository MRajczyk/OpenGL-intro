import sys
import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

m_transX = 0
m_transY = 0
m_angle1 = 0
m_angle2 = 0
ArmPart = 0

RedSurface = [1.0, 0.0, 0.0, 1.0]
GreenSurface = [0.0, 1.0, 0.0, 1.0]
BlueSurface = [0.0, 0.0, 1.0, 1.0]
LightAmbient = [0.2, 0.2, 0.2, 1.0]
LightDiffuse = [0.7, 0.7, 0.7, 1.0]
LightSpecular = [0.0, 0.0, 0.0, 0.1]
LightPosition = [5.0, 5.0, 0.0, 1.0]


def myPaint():
    #Example 1
    # glColor4f(1.0, 0.0, 0.0, 1.0)
    # glCallList(ArmPart)
    #Example 2
    # glPushMatrix()
    # glTranslated( m_transX, m_transY, 0)
    # glRotated( m_angle1, 0, 0, 1)
    # glColor4f(1.0, 0.0, 0.0, 1.0)
    # glCallList(ArmPart)
    # glPopMatrix()
    #Example 3
    # glPushMatrix()
    #
    # glTranslated( m_transX, m_transY, 0)
    # glRotated( m_angle1, 0, 0, 1)
    # glColor4f(1.0, 0.0, 0.0, 1.0)
    # glCallList(ArmPart)
    #
    # glPushMatrix()
    # glTranslated( 90, 0, 0)
    # glRotated( m_angle2, 0, 0, 1)
    # glColor4f(0.0, 1.0, 0.0, 1.0)
    # glCallList(ArmPart)
    # glPopMatrix()
    #
    # glPopMatrix()

    #Example 3 CUBE
    glPushMatrix()

    glTranslated( m_transX, m_transY, 0)
    glRotated( m_angle1, 0, 1, 0)
    glRotated( m_angle2, 1, 0, 0)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, RedSurface)
    glBegin(GL_POLYGON)
    glVertex3f(-50.0, -50.0, 50.0)
    glVertex3f(50.0, -50.0, 50.0)
    glVertex3f(50.0, 50.0, 50.0)
    glVertex3f(-50.0, 50.0, 50.0)
    glEnd()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, GreenSurface)
    glBegin(GL_POLYGON)
    glVertex3f(-50.0, -50.0, -50.0)
    glVertex3f(-50.0, 50.0, -50.0)
    glVertex3f(50.0, 50.0, -50.0)
    glVertex3f(50.0, -50.0, -50.0)
    glEnd()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, BlueSurface)
    glBegin(GL_POLYGON)
    glVertex3f(-50.0, -50.0, -50.0)
    glVertex3f(-50.0, -50.0, 50.0)
    glVertex3f(-50.0, 50.0, 50.0)
    glVertex3f(-50.0, 50.0, -50.0)
    glEnd()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, RedSurface)
    glBegin(GL_POLYGON)
    glVertex3f(50.0, -50.0, -50.0)
    glVertex3f(50.0, 50.0, -50.0)
    glVertex3f(50.0, 50.0, 50.0)
    glVertex3f(50.0, -50.0, 50.0)
    glEnd()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, GreenSurface)
    glBegin(GL_POLYGON)
    glVertex3f(-50.0, -50.0, -50.0)
    glVertex3f(50.0, -50.0, -50.0)
    glVertex3f(50.0, -50.0, 50.0)
    glVertex3f(-50.0, -50.0, 50.0)
    glEnd()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, BlueSurface)
    glBegin(GL_POLYGON)
    glVertex3f(-50.0, 50.0, -50.0)
    glVertex3f(50.0, 50.0, -50.0)
    glVertex3f(50.0, 50.0, 50.0)
    glVertex3f(-50.0, 50.0, 50.0)
    glEnd()

    glPopMatrix()


pygame.init()
display = (1600, 1200)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)
glTranslatef(0.0,0.0, -200)
# gluOrtho2D(0.0, 500.0*(display[0]/display[1]), 0.0, 500.0)

# ArmPart=glGenLists(1)
# glNewList(ArmPart, GL_COMPILE)
# glBegin(GL_POLYGON)
# glVertex2f(-10.0, 10.0)
# glVertex2f(-10.0, -10.0)
# glVertex2f(100.0, -10.0)
# glVertex2f(100.0, 10.0)
# glEnd()
# glEndList()

m_RightDownPos=(0,0)
m_LeftDownPos=(0,0)
m_RightButtonDown=False
m_LeftButtonDown=False

glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmbient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDiffuse)
glLightfv(GL_LIGHT0, GL_SPECULAR, LightSpecular)
glLightfv(GL_LIGHT0, GL_POSITION, LightPosition)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_DEPTH_TEST)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEMOTION:
            if m_LeftButtonDown:
                m_angle1 += m_LeftDownPos[0] - event.pos[0]
                m_angle2 += m_LeftDownPos[1] - event.pos[1]
                m_LeftDownPos = event.pos
            elif m_RightButtonDown:
                m_transX -= m_RightDownPos[0] - event.pos[0]
                m_transY += m_RightDownPos[1] - event.pos[1]
                m_RightDownPos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_LeftButtonDown = True
                m_LeftDownPos=event.pos
            elif event.button == 3:
                m_RightButtonDown = True
                m_RightDownPos=event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                m_LeftButtonDown = False
            elif event.button == 3:
                m_RightButtonDown = False

    # glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    myPaint()
    pygame.display.flip()
    pygame.time.wait(10)
