import sys
import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import math

# Inicjalizacja czasu
time_start = time.time()
camera_distance = 500
m_angle1 = 0
m_angle2 = -90

# Wczytanie tekstury
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

# Rysowanie kuli z teksturą
def draw_textured_sphere(texture_id, radius=5):
    quad = gluNewQuadric()
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluQuadricTexture(quad, GL_TRUE)
    glEnable(GL_TEXTURE_2D)

    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    gluSphere(quad, radius, 32, 32)
    glPopMatrix()

    glDisable(GL_TEXTURE_2D)
    gluDeleteQuadric(quad)

# Rysowanie pierścieni Saturna
def draw_saturn_rings(inner_radius, outer_radius, num_segments=100):
    glColor3f(0.8, 0.7, 0.5)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(num_segments + 1):
        angle = math.radians(i * 360 / num_segments)
        x = math.cos(angle)
        z = math.sin(angle)
        glVertex3f(x * inner_radius, 0, z * inner_radius)
        glVertex3f(x * outer_radius, 0, z * outer_radius)
    glEnd()

# Rysowanie orbity jako okręgu
def draw_orbit(radius):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex3f(math.cos(angle) * radius, 0, math.sin(angle) * radius)
    glEnd()

pygame.init()
display = (1200, 900)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
glTranslatef(0.0, 0.0, -200)
glEnable(GL_DEPTH_TEST)

sun_texture = load_texture("sun_texture.jpg")  # Wczytaj teksturę Słońca
mercury_texture = load_texture("mercury_texture.jpg")  # Wczytaj teksturę Ziemi
venus_texture = load_texture("venus_texture.jpg")  # Wczytaj teksturę Wenus
earth_texture = load_texture("earth_texture.jpg")  # Wczytaj teksturę Ziemi
mars_texture = load_texture("mars_texture.jpg")  # Wczytaj teksturę Marsa
jupiter_texture = load_texture("jupiter_texture.jpg")  # Wczytaj teksturę Jowisza
saturn_texture = load_texture("saturn_texture.jpg")  # Wczytaj teksturę Saturna
uranus_texture = load_texture("uranus_texture.jpg")  # Wczytaj teksturę Urana
neptune_texture = load_texture("neptune_texture.jpg")  # Wczytaj teksturę Neptuna

# Ustawienie źródła światła
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0])

m_LeftDownPos = (0, 0)
m_LeftButtonDown = False

while True:
    time_elapsed = time.time() - time_start
    planet_rotation = time_elapsed * 10  # Rotacja wokół własnej osi
    sun_rotation = time_elapsed * 5
    orbit_angle_mercury = time_elapsed * 30
    orbit_angle_venus = time_elapsed * 25
    orbit_angle_earth = time_elapsed * 20
    orbit_angle_mars = time_elapsed * 15
    orbit_angle_jupiter = time_elapsed * 8
    orbit_angle_saturn = time_elapsed * 6
    orbit_angle_uranus = time_elapsed * 4
    orbit_angle_neptune = time_elapsed * 2
    orbit_radius_mercury = 30
    orbit_radius_venus = 50
    orbit_radius_earth = 70
    orbit_radius_mars = 90
    orbit_radius_jupiter = 140
    orbit_radius_saturn = 180
    orbit_radius_uranus = 220
    orbit_radius_neptune = 260

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEMOTION:
            if m_LeftButtonDown:
                m_angle1 -= m_LeftDownPos[0] - event.pos[0]
                m_angle2 -= m_LeftDownPos[1] - event.pos[1]
                m_LeftDownPos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_LeftButtonDown = True
                m_LeftDownPos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                m_LeftButtonDown = False
        elif event.type == pygame.MOUSEWHEEL:
            camera_distance -= 5 * event.y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
    glTranslatef(0.0, 0.0, -camera_distance)

    glRotated(m_angle1, 0, 1, 0)
    glRotated(m_angle2, 1, 0, 0)

    # Rysowanie orbit
    glDisable(GL_LIGHTING)
    draw_orbit(orbit_radius_mercury)
    draw_orbit(orbit_radius_venus)
    draw_orbit(orbit_radius_earth)
    draw_orbit(orbit_radius_mars)
    draw_orbit(orbit_radius_jupiter)
    draw_orbit(orbit_radius_saturn)
    draw_orbit(orbit_radius_uranus)
    draw_orbit(orbit_radius_neptune)
    glEnable(GL_LIGHTING)

    # Rysowanie centralnej kuli (Słońce) jako źródło światła
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glRotatef(-sun_rotation, 0, 1, 0)
    draw_textured_sphere(sun_texture, 12)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Rysowanie Merkurego
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_mercury)) * orbit_radius_mercury
    z = math.sin(math.radians(orbit_angle_mercury)) * orbit_radius_mercury
    glTranslatef(x, 0, z)
    glRotatef(planet_rotation, 0, 1, 0)
    draw_textured_sphere(mercury_texture, 3)
    glPopMatrix()

    # Rysowanie Wenus
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_venus)) * orbit_radius_venus
    z = math.sin(math.radians(orbit_angle_venus)) * orbit_radius_venus
    glTranslatef(x, 0, z)
    glRotatef(-planet_rotation, 0, 1, 0)
    draw_textured_sphere(venus_texture, 4)
    glPopMatrix()

    # Rysowanie Ziemi
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_earth)) * orbit_radius_earth
    z = math.sin(math.radians(orbit_angle_earth)) * orbit_radius_earth
    glTranslatef(x, 0, z)
    glRotatef(planet_rotation, 0, 1, 0)
    draw_textured_sphere(earth_texture, 5)
    glPopMatrix()

    # Rysowanie Marsa
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_mars)) * orbit_radius_mars
    z = math.sin(math.radians(orbit_angle_mars)) * orbit_radius_mars
    glTranslatef(x, 0, z)
    glRotatef(planet_rotation, 0, 1, 0)
    draw_textured_sphere(mars_texture, 4)
    glPopMatrix()

    # Rysowanie Jowisza
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_jupiter)) * orbit_radius_jupiter
    z = math.sin(math.radians(orbit_angle_jupiter)) * orbit_radius_jupiter
    glTranslatef(x, 0, z)
    glRotatef(planet_rotation, 0, 1, 0)
    draw_textured_sphere(jupiter_texture, 12)
    glPopMatrix()

    # Rysowanie Saturna
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_saturn)) * orbit_radius_saturn
    z = math.sin(math.radians(orbit_angle_saturn)) * orbit_radius_saturn
    glTranslatef(x, 0, z)
    glRotatef(planet_rotation, 0, 1, 0)
    draw_textured_sphere(saturn_texture, 10)
    draw_saturn_rings(14, 18)
    glPopMatrix()

    # Rysowanie Urana
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_uranus)) * orbit_radius_uranus
    z = math.sin(math.radians(orbit_angle_uranus)) * orbit_radius_uranus
    glTranslatef(x, 0, z)
    glRotatef(-planet_rotation, 0, 1, 0)
    draw_textured_sphere(uranus_texture, 10)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    draw_saturn_rings(13, 14)
    glPopMatrix()
    glPopMatrix()

    # Rysowanie Neptuna
    glPushMatrix()
    x = math.cos(math.radians(orbit_angle_neptune)) * orbit_radius_neptune
    z = math.sin(math.radians(orbit_angle_neptune)) * orbit_radius_neptune
    glTranslatef(x, 0, z)
    glRotatef(planet_rotation, 0, 1, 0)
    draw_textured_sphere(neptune_texture, 10)
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(20)
