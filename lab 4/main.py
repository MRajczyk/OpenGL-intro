import sys
import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time

# stałe
k = 10.0
m = 10.0
g = 9.81
L_n = 5.0

# obliczone wartości
A = m * g / k
L_0 = L_n + A
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


def calculate_z_position(t):
    omega = (k / m) ** 0.5
    max_stretch = A
    equilibrium = -L_0

    return equilibrium - max_stretch * (1 + np.cos(omega * t)) / 2


def draw_spring(x, y, z, texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    rows, cols = x.shape
    for i in range(rows - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(cols):
            glTexCoord2f(j / float(cols - 1), i / float(rows - 1))
            glVertex3f(x[i, j], y[i, j], z[i, j])

            glTexCoord2f(j / float(cols - 1), (i + 1) / float(rows - 1))
            glVertex3f(x[i + 1, j], y[i + 1, j], z[i + 1, j])

        glEnd()
    glDisable(GL_TEXTURE_2D)


def generate_spring(radius=3, turns=5, segments=20, top=0, bottom=-20):
    coil_height = (bottom - top) / (2 * np.pi * turns)

    t = np.linspace(0, turns * 2 * np.pi, segments * turns)
    u = np.linspace(0, 2 * np.pi, segments)
    t, u = np.meshgrid(t, u)

    x = np.cos(t) * (radius + np.cos(u))
    y = np.sin(t) * (radius + np.cos(u))
    z = top + coil_height * t + np.sin(u)

    return x, y, z


def draw_cylinder(base_radius, top_radius, height, slices=32, stacks=1, x=0, y=0, z=0, texture=None):
    glPushMatrix()
    glTranslatef(x, y, z)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluCylinder(quadric, base_radius, top_radius, height, slices, stacks)

    glDisable(GL_TEXTURE_2D)

    glPopMatrix()


def myPaint():
    current_time = time.time() - start_time
    bottom_z = calculate_z_position(current_time)

    draw_ceiling(3)

    x, y, z = generate_spring(top=0, bottom=bottom_z)
    draw_spring(x, y, z, steel_texture)

    draw_cylinder(base_radius=1, top_radius=1, height=3, x=3, y=0, z=0, texture=steel_texture)
    draw_cylinder(base_radius=1, top_radius=1, height=3, x=3, y=0, z=bottom_z-3, texture=steel_texture)

    draw_ball(3, 0, bottom_z - 3 - 5, radius=5)


def draw_ball(x, y, z, radius=5):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor4f(0.5, 0.7, 1.0, 0.4)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    gluSphere(gluNewQuadric(), radius, 32, 32)
    glDisable(GL_BLEND)
    glPopMatrix()


def draw_ceiling(z, height=5):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, wood_texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-10, -10, z)
    glTexCoord2f(0.0, 1.0); glVertex3f(-10, 10, z)
    glTexCoord2f(1.0, 1.0); glVertex3f(10, 10, z)
    glTexCoord2f(1.0, 0.0); glVertex3f(10, -10, z)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-10, -10, z + height)
    glTexCoord2f(0.0, 1.0); glVertex3f(-10, 10, z + height)
    glTexCoord2f(1.0, 1.0); glVertex3f(10, 10, z + height)
    glTexCoord2f(1.0, 0.0); glVertex3f(10, -10, z + height)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(10, 10, z)
    glTexCoord2f(0.0, 1.0); glVertex3f(10, 10, z + height)
    glTexCoord2f(1.0, 1.0); glVertex3f(10, -10, z + height)
    glTexCoord2f(1.0, 0.0); glVertex3f(10, -10, z)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-10, 10, z)
    glTexCoord2f(0.0, 1.0); glVertex3f(-10, 10, z + height)
    glTexCoord2f(1.0, 1.0); glVertex3f(10, 10, z + height)
    glTexCoord2f(1.0, 0.0); glVertex3f(10, 10, z)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-10, 10, z)
    glTexCoord2f(0.0, 1.0); glVertex3f(-10, 10, z + height)
    glTexCoord2f(1.0, 1.0); glVertex3f(-10, -10, z + height)
    glTexCoord2f(1.0, 0.0); glVertex3f(-10, -10, z)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-10, -10, z)
    glTexCoord2f(0.0, 1.0); glVertex3f(-10, -10, z + height)
    glTexCoord2f(1.0, 1.0); glVertex3f(10, -10, z + height)
    glTexCoord2f(1.0, 0.0); glVertex3f(10, -10, z)
    glEnd()

    glDisable(GL_TEXTURE_2D)


pygame.init()
display = (1200, 900)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
glTranslatef(0.0, 0.0, -200)
glEnable(GL_DEPTH_TEST)

m_LeftDownPos = (0, 0)
m_LeftButtonDown = False

wood_texture = load_texture("wood_texture.jpg")
steel_texture = load_texture("steel_texture.jpg")

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
