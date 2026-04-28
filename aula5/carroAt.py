import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# --- Variáveis de Estado do Carro ---
car_pos_x = 0.0
car_pos_z = 0.0
car_angle = 0.0    # Orientação do chassi
wheel_rot = 0.0    # Giro das rodas (rolagem)
speed = 0.2        # Velocidade de deslocamento
turn_speed = 5.0   # Velocidade da curva

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

def resize(window, w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def load_obj(path):
    vertices = []
    faces = []
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif line.startswith('f '):
                    parts = line.strip().split()[1:]
                    face = [int(p.split('/')[0]) - 1 for p in parts]
                    faces.append(face)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path} não encontrado!")
    return vertices, faces

def draw_obj(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glVertex3f(*vertices[idx])
    glEnd()

def draw_axes():
    glBegin(GL_LINES)
    glColor3f(1, 0, 0); glVertex3f(0, 0, 0); glVertex3f(5, 0, 0) # X
    glColor3f(0, 1, 0); glVertex3f(0, 0, 0); glVertex3f(0, 5, 0) # Y
    glColor3f(0, 0, 1); glVertex3f(0, 0, 0); glVertex3f(0, 0, 5) # Z
    glEnd()

def display(carro_v, carro_f, roda_v, roda_f):
    global car_pos_x, car_pos_z, car_angle, wheel_rot

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Câmera posicionada para ver o cenário
    gluLookAt(15, 15, 20, 0, 0, 0, 0, 1, 0)

    draw_axes()

    # --- HIERARQUIA DO CARRO ---
    glPushMatrix()
    
    # 1. Posiciona o carro no mundo
    glTranslatef(car_pos_x, 0, car_pos_z)
    
    # 2. Gira o carro na direção atual
    glRotatef(car_angle, 0, 1, 0)
    
    glScalef(0.5, 0.5, 0.5)

    # Desenha o Chassi
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(1.2, 1.1, 1.3)
    glColor3f(0.1, 0.3, 1.0) # Azul
    glRotatef(180, 0, 1, 0) # Gira o modelo 180 graus sobre o próprio eixo Y
    draw_obj(carro_v, carro_f)
    glPopMatrix()

    # Desenha as Rodas
    # Posições relativas ao centro do carro
    posicoes_rodas = [(1.2, 0.5, 2), (-1.2, 0.5, 2), (1.2, 0.5, -2), (-1.2, 0.5, -2)]
    
    for x, y, z in posicoes_rodas:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(wheel_rot, 1, 0, 0) # Rotação da roda ao andar
        glColor3f(1, 0.2, 0.2)        # Vermelho
        draw_obj(roda_v, roda_f)
        glPopMatrix()

    glPopMatrix() 

def process_input(window):
    global car_pos_x, car_pos_z, car_angle, wheel_rot

    rad = math.radians(car_angle)

    up = glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS
    down = glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS
    left = glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS
    right = glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS

    # --- ROTAÇÃO (Agora fora dos blocos Up/Down para girar no próprio eixo) ---
    if left:
        car_angle += turn_speed
    if right:
        car_angle -= turn_speed

    # --- MOVIMENTAÇÃO ---
    if up: # 
        car_pos_x -= math.sin(rad) * speed
        car_pos_z -= math.cos(rad) * speed
        wheel_rot -= 10
    elif down: # Agora DOWN vai para trás (subtrai do deslocamento)
        car_pos_x += math.sin(rad) * speed
        car_pos_z += math.cos(rad) * speed
        wheel_rot += 10

    # MOVIMENTO PARA TRÁS (Tecla UP)
    elif up:
        # Invertido: Ajustado para a lógica de ré
        if left: car_angle += turn_speed 
        if right: car_angle -= turn_speed
        
        car_pos_x -= math.sin(rad) * speed
        car_pos_z -= math.cos(rad) * speed
        wheel_rot -= 8

def main():
    if not glfw.init():
        return

    window = glfw.create_window(1280, 720, "Computação Gráfica - Carro 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, resize)
    
    init()

    # Carregamento dos modelos
    carro_v, carro_f = load_obj("Car.obj")
    roda_v, roda_f = load_obj("roda2.obj")

    # Loop Principal
    while not glfw.window_should_close(window):
        # 1. Processa entradas (movimento e curva)
        process_input(window)
        
        # 2. Renderiza a cena
        display(carro_v, carro_f, roda_v, roda_f)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()