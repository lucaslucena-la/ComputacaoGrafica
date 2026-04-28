import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# =========================
# VARIÁVEIS GLOBAIS
# =========================
car_x = 0
car_z = 0
car_angle = 0
wheel_rotation = 0

keys = {}

# =========================
# CÂMERA (INALTERADA)
# =========================
eye = [8.0, 10.0, 20.0]
center = [0.0, 0.0, 0.0]
up = [0.0, 1.0, 0.0]

camera_speed = 0.5

def normalize(v):
    mag = math.sqrt(sum(i*i for i in v))
    return [i/mag for i in v]

def cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

# =========================
# OPENGL
# =========================
def init():
    glClearColor(0.6, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def resize(window, w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# =========================
# LAYOUT (NOVO SOLO)
# =========================
def draw_ground():
    size = 60

    # GRAMA
    glColor3f(0.2, 0.6, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-size, 0, -size)
    glVertex3f(-size, 0, size)
    glVertex3f(size, 0, size)
    glVertex3f(size, 0, -size)
    glEnd()

    road_width = 6

    # ASFALTO
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(-road_width/2, 0.01, -size)
    glVertex3f(-road_width/2, 0.01, size)
    glVertex3f( road_width/2, 0.01, size)
    glVertex3f( road_width/2, 0.01, -size)
    glEnd()

    # BORDAS BRANCAS
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    # esquerda
    glVertex3f(-road_width/2, 0.02, -size)
    glVertex3f(-road_width/2 + 0.2, 0.02, -size)
    glVertex3f(-road_width/2 + 0.2, 0.02, size)
    glVertex3f(-road_width/2, 0.02, size)

    # direita
    glVertex3f(road_width/2 - 0.2, 0.02, -size)
    glVertex3f(road_width/2, 0.02, -size)
    glVertex3f(road_width/2, 0.02, size)
    glVertex3f(road_width/2 - 0.2, 0.02, size)
    glEnd()

    # FAIXA TRACEJADA
    glColor3f(1, 1, 0)
    glBegin(GL_QUADS)
    for z in range(-size, size, 4):
        glVertex3f(-0.15, 0.03, z)
        glVertex3f(-0.15, 0.03, z + 2)
        glVertex3f(0.15, 0.03, z + 2)
        glVertex3f(0.15, 0.03, z)
    glEnd()

# =========================
# OBJ
# =========================
def load_obj(path):
    vertices = []
    objects = {}
    current_object = "default"

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:

            if line.startswith('o '):
                current_object = line.strip().split(maxsplit=1)[1]
                objects[current_object] = []

            elif line.startswith('v '):
                parts = line.strip().split()
                vertices.append(list(map(float, parts[1:4])))

            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                indices = []

                for p in parts:
                    idx = p.split('/')[0]
                    indices.append(int(idx) - 1)

                for i in range(1, len(indices) - 1):
                    face = [indices[0], indices[i], indices[i + 1]]

                    if current_object not in objects:
                        objects[current_object] = []

                    objects[current_object].append(face)

    return vertices, objects

def get_object_center(vertices, faces):
    points = []

    for face in faces:
        for idx in face:
            points.append(vertices[idx])

    x = sum(v[0] for v in points) / len(points)
    y = sum(v[1] for v in points) / len(points)
    z = sum(v[2] for v in points) / len(points)

    return x, y, z

def draw_object(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glVertex3f(*vertices[idx])
    glEnd()

# =========================
# CÂMERA (INALTERADA)
# =========================
def apply_camera():
    gluLookAt(
        eye[0], eye[1], eye[2],
        center[0], center[1], center[2],
        up[0], up[1], up[2]
    )

def update_camera():
    global eye, center, up

    forward = [center[i] - eye[i] for i in range(3)]
    forward = normalize(forward)

    right = normalize(cross(forward, up))

    if keys.get(glfw.KEY_W):
        for i in range(3):
            eye[i] += forward[i] * camera_speed
            center[i] += forward[i] * camera_speed

    if keys.get(glfw.KEY_S):
        for i in range(3):
            eye[i] -= forward[i] * camera_speed
            center[i] -= forward[i] * camera_speed

    if keys.get(glfw.KEY_A):
        for i in range(3):
            eye[i] -= right[i] * camera_speed
            center[i] -= right[i] * camera_speed

    if keys.get(glfw.KEY_D):
        for i in range(3):
            eye[i] += right[i] * camera_speed
            center[i] += right[i] * camera_speed

    if keys.get(glfw.KEY_Q):
        eye[1] += camera_speed
        center[1] += camera_speed

    if keys.get(glfw.KEY_E):
        eye[1] -= camera_speed
        center[1] -= camera_speed

    if keys.get(glfw.KEY_I):
        center[2] -= camera_speed
    if keys.get(glfw.KEY_K):
        center[2] += camera_speed
    if keys.get(glfw.KEY_J):
        center[0] -= camera_speed
    if keys.get(glfw.KEY_L):
        center[0] += camera_speed

    if keys.get(glfw.KEY_Z):
        up[0] += 0.01
    if keys.get(glfw.KEY_X):
        up[0] -= 0.01

# =========================
# MOVIMENTO DO CARRO
# =========================
def update_movement():
    global car_x, car_z, car_angle, wheel_rotation

    speed = 0.1
    rot_speed = 2

    if keys.get(glfw.KEY_LEFT):
        car_angle += rot_speed

    if keys.get(glfw.KEY_RIGHT):
        car_angle -= rot_speed

    rad = math.radians(car_angle)

    if keys.get(glfw.KEY_UP):
        car_x += math.sin(rad) * speed
        car_z += math.cos(rad) * speed
        wheel_rotation += 10

    if keys.get(glfw.KEY_DOWN):
        car_x -= math.sin(rad) * speed
        car_z -= math.cos(rad) * speed
        wheel_rotation -= 10

# =========================
# RENDER
# =========================
def display(vertices, objects):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    apply_camera()

    draw_ground()

    glPushMatrix()

    glTranslatef(car_x, 0.02, car_z)
    glRotatef(car_angle, 0, 1, 0)
    glTranslatef(0, 1, 0)

    for name, faces in objects.items():

        if name in ["Roda_FL", "Roda_FR", "Roda_BL", "Roda_BR"]:
            glColor3f(0.15, 0.15, 0.15)

            cx, cy, cz = get_object_center(vertices, faces)

            glPushMatrix()
            glTranslatef(cx, cy, cz)
            glRotatef(wheel_rotation, 1, 0, 0)
            glTranslatef(-cx, -cy, -cz)
            draw_object(vertices, faces)
            glPopMatrix()

        else:
            glColor3f(0.9, 0.2, 0.2)
            draw_object(vertices, faces)

    glPopMatrix()

# =========================
# TECLADO
# =========================
def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

# =========================
# MAIN
# =========================
def main():
    if not glfw.init():
        return

    window = glfw.create_window(1280, 720, "Carro 3D", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glfw.set_window_size_callback(window, resize)
    glfw.set_key_callback(window, key_callback)

    init()

    vertices, objects = load_obj("LowPolyFiatUNO.obj")

    while not glfw.window_should_close(window):

        update_movement()
        update_camera()

        display(vertices, objects)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()