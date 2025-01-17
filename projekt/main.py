import sys
import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import time


start_time = time.time()
camera_distance = 130
m_angle1 = 0
m_angle2 = -90


def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id


def myPaint():
    current_time = time.time() - start_time


def draw_ball(x, y, z, radius=5):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor4f(0.5, 0.7, 1.0, 0.4)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    gluSphere(gluNewQuadric(), radius, 32, 32)
    glDisable(GL_BLEND)
    glPopMatrix()


pygame.init()
display = (1200, 900)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
glTranslatef(0.0, 0.0, -200)
glEnable(GL_DEPTH_TEST)

m_LeftDownPos = (0, 0)
m_LeftButtonDown = False

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_LeftButtonDown = True
                m_LeftDownPos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                m_LeftButtonDown = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                camera_distance -= 5
            elif event.y < 0:
                camera_distance += 5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
    glTranslatef(0.0, 0.0, -camera_distance)

    glRotated(m_angle1, 0, 1, 0)
    glRotated(m_angle2, 1, 0, 0)

    myPaint()
    pygame.display.flip()
    pygame.time.wait(20)
