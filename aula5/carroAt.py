import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# =========================
# VARIÁVEIS DO CARRO
# =========================
car_x = 0
car_z = 0
car_angle = 0
wheel_rotation = 0

keys = {}

# =========================
# VARIÁVEIS DA CÂMERA
# =========================
eye = [8.0, 10.0, 20.0]
center = [0.0, 0.0, 0.0]
up = [0.0, 1.0, 0.0]

camera_speed = 0.5

# =========================
# FUNÇÕES AUXILIARES
# =========================
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
# OPENGL SETUP
# =========================
def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
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
# OBJ
# =========================
def load_obj(path):
    vertices = []
    faces = []

    with open(path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append([
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3])
                ])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = []
                for p in parts:
                    idx = p.split('/')[0]
                    face.append(int(idx) - 1)
                faces.append(face)

    return vertices, faces

def draw_obj(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glVertex3f(*vertices[idx])
    glEnd()

# =========================
# EIXOS
# =========================
def draw_axes():
    glBegin(GL_LINES)

    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 10, 0)

    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 10)

    glEnd()

# =========================
# CÂMERA
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

    # movimento
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

    # olhar (center)
    if keys.get(glfw.KEY_UP):
        center[2] -= camera_speed
    if keys.get(glfw.KEY_DOWN):
        center[2] += camera_speed
    if keys.get(glfw.KEY_LEFT):
        center[0] -= camera_speed
    if keys.get(glfw.KEY_RIGHT):
        center[0] += camera_speed

    # up vector
    if keys.get(glfw.KEY_Z):
        up[0] += 0.01
    if keys.get(glfw.KEY_X):
        up[0] -= 0.01

# =========================
# MOVIMENTO DO CARRO
# =========================
def update_movement():
    global car_x, car_z, car_angle, wheel_rotation

    speed = 0.2
    rot_speed = 2

    if keys.get(glfw.KEY_LEFT):
        car_angle += rot_speed
    if keys.get(glfw.KEY_RIGHT):
        car_angle -= rot_speed

    rad = math.radians(car_angle)

    if keys.get(glfw.KEY_UP):
        car_x -= math.sin(rad) * speed
        car_z -= math.cos(rad) * speed
        wheel_rotation += 8

    if keys.get(glfw.KEY_DOWN):
        car_x += math.sin(rad) * speed
        car_z += math.cos(rad) * speed
        wheel_rotation -= 8

# =========================
# RENDER
# =========================
def display(carro_v, carro_f, roda_v, roda_f):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    apply_camera()

    glScalef(0.5, 0.5, 0.5)

    glPushMatrix()

    glTranslatef(car_x, 0, car_z)
    glRotatef(car_angle, 0, 1, 0)

    glPushMatrix()
    glTranslatef(0, 1, 0)
    glColor3f(0.1, 0.3, 1.0)
    draw_obj(carro_v, carro_f)
    glPopMatrix()

    posicoes = [
        (1.2, 1, 3),
        (-1.2, 1, 3),
        (1.2, 1, -3),
        (-1.2, 1, -3)
    ]

    for x, y, z in posicoes:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(wheel_rotation, 1, 0, 0)
        glColor3f(1, 0.2, 0.2)
        draw_obj(roda_v, roda_f)
        glPopMatrix()

    glPopMatrix()

    draw_axes()

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

    window = glfw.create_window(1280, 720, "Carro 3D com Camera Livre", None, None)
    glfw.make_context_current(window)

    glfw.set_window_size_callback(window, resize)
    glfw.set_key_callback(window, key_callback)

    init()

    carro_v, carro_f = load_obj("carro.obj")
    roda_v, roda_f = load_obj("roda2.obj")

    while not glfw.window_should_close(window):

        update_movement()
        update_camera()  # <<< câmera independente

        display(carro_v, carro_f, roda_v, roda_f)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()