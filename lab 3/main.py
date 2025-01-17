import sys
import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

display = (800, 600)
TRIANGLE_SIDE_LENGTH = 50.0
TRANSLATION_RATE_X = (TRIANGLE_SIDE_LENGTH * 3) / (360 * 10) * (display[0] / display[1])
TRANSLATION_RATE_Y = (TRIANGLE_SIDE_LENGTH * 3) / (360 * 10)
ROTATION_RATE = 0.3

outerRotationAngle = 0
innerRotationAngle = 0
innerTranslation = [0.0, 0.0]


def paintBlueTriangle():
    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.0, 1)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 1 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(1 * TRIANGLE_SIDE_LENGTH, 0.0)
    glEnd()


def paintOrangeTriangle():
    glBegin(GL_POLYGON)
    glColor3f(1.0, 0.5, 0.0)
    glVertex2f(1 * TRIANGLE_SIDE_LENGTH, 0.0)
    glVertex2f(1 * TRIANGLE_SIDE_LENGTH, 1 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(2 * TRIANGLE_SIDE_LENGTH, 0.0)
    glEnd()


def paintPinkTriangle():
    glBegin(GL_POLYGON)
    glColor3f(1, 0.11, 0.81)
    glVertex2f(2 * TRIANGLE_SIDE_LENGTH, 0.0)
    glVertex2f(2 * TRIANGLE_SIDE_LENGTH, 1 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(3 * TRIANGLE_SIDE_LENGTH, 0.0)
    glEnd()


def paintGreenTriangle():
    glBegin(GL_POLYGON)
    glColor3f(0.4, 1, 0)
    glVertex2f(0.0, 1 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(0.0, 2 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(1 * TRIANGLE_SIDE_LENGTH, 1 * TRIANGLE_SIDE_LENGTH)
    glEnd()


def paintYellowTriangle():
    glBegin(GL_POLYGON)
    glColor3f(1, 1, 0)
    glVertex2f(1 * TRIANGLE_SIDE_LENGTH, 1 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(2 * TRIANGLE_SIDE_LENGTH, 1 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(1 * TRIANGLE_SIDE_LENGTH, 2 * TRIANGLE_SIDE_LENGTH)
    glEnd()


def paintRedTriangle():
    glBegin(GL_POLYGON)
    glColor3f(1, 0, 0)
    glVertex2f(0.0, 2 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(0.0, 3 * TRIANGLE_SIDE_LENGTH)
    glVertex2f(1 * TRIANGLE_SIDE_LENGTH, 2 * TRIANGLE_SIDE_LENGTH)
    glEnd()


def drawOuterTriangles():
    paintPinkTriangle()
    paintYellowTriangle()
    paintRedTriangle()


def drawInnerTriangles():
    paintBlueTriangle()
    paintOrangeTriangle()
    paintGreenTriangle()


def myPaint():
    global outerRotationAngle
    global innerRotationAngle

    glPushMatrix()
    glRotatef(innerRotationAngle, 0.0, 0.0, 1.0)
    innerRotationAngle += 3 * ROTATION_RATE
    glPushMatrix()
    for i in range(0, 4):
        # glPushMatrix()
        glTranslatef(innerTranslation[0], innerTranslation[1], 0)
        drawInnerTriangles()
        # glPopMatrix()
        glRotate(-90, 0, 0, 1)

    innerTranslation[0] += TRANSLATION_RATE_X
    innerTranslation[1] += TRANSLATION_RATE_Y
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glRotatef(outerRotationAngle, 0.0, 0.0, 1.0)
    outerRotationAngle -= ROTATION_RATE
    glPushMatrix()
    for i in range(0, 4):
        drawOuterTriangles()
        glRotate(-90, 0, 0, 1)
    glPopMatrix()
    glPopMatrix()


pygame.init()
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluOrtho2D(-350.0 * (display[0]/display[1]), 350.0 * (display[0]/display[1]), -350.0, 350.0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    myPaint()
    pygame.display.flip()
    pygame.time.wait(10)
