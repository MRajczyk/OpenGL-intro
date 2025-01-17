import sys
import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *


def myPaint():
    glBegin(GL_POLYGON)
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glVertex2f(100.0, 50.0)
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glVertex2f(450.0, 450.0)
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glVertex2f(450.0, 50.0)
    glEnd()


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
# gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
gluOrtho2D(0.0, 500.0 * (display[0] / display[1]), 0.0, 500.0)
# glTranslatef(0.0, 0.0, -5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    # glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    myPaint()
    pygame.display.flip()
    pygame.time.wait(10)

# Jako wierzchołki trójkąta zdefiniowane zostały węzły z kolorami czerwony, niebieski, zielony,
# Kolor innych punktów należących do trójkąta jest mieszaniną barw wierzchołków,
# w efekcie tworząc gradient
