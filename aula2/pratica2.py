import glfw
from OpenGL.GL import *
import math

# (Função draw_circle permanece igual)
def draw_circle(x_central, y_central, raio_x, raio_y, r, g, b, a=1.0, segmentos=64):
    glColor4f(r, g, b, a) # glColor4f em vez de 3f para usar transparência
    glBegin(GL_POLYGON)
    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        x = x_central + math.cos(angulo) * raio_x
        y = y_central + math.sin(angulo) * raio_y
        glVertex2f(x, y)
    glEnd()

def main():
    if not glfw.init(): return
    window = glfw.create_window(800, 800, "Ovo de Pascoa com Sombra", None, None)
    glfw.make_context_current(window)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while not glfw.window_should_close(window):
        glClearColor(0.9, 0.9, 0.9, 1) # Fundo cinza claro
        glClear(GL_COLOR_BUFFER_BIT)

        # Deslocamento: x=0.03, y=-0.03 (para a direita e para baixo)
        # Cor: r=0, g=0, b=0 (preto) e a=0.3 (30% de opacidade/transparência)
        draw_circle(0.03, -0.03, 0.4, 0.5, 0.0, 0.0, 0.0, 0.3) 

        # --- O CORPO DO OVO (Rosa, inalterado) ---
        draw_circle(0.0, 0.0, 0.4, 0.5, 1.0, 0.4, 0.6)

        # --- O BRILHO (Rosa Claro) ---
        draw_circle(-0.15, 0.25, 0.12, 0.12, 1.0, 0.6, 0.7)
        # --- AS BOLINHAS BRANCAS (Base) ---
        draw_circle(-0.2, -0.25, 0.03, 0.03, 1.0, 1.0, 1.0)
        draw_circle(0.0, -0.35, 0.03, 0.03, 1.0, 1.0, 1.0)
        draw_circle(0.2, -0.25, 0.03, 0.03, 1.0, 1.0, 1.0)
        # --- ONDA AMARELA ---
        glLineWidth(3)
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 0.8, 0.0) # Amarelo
        for x in [i/100 for i in range(-32, 33)]:
            y = 0.05 + 0.03 * math.sin(x * 15) 
            glVertex2f(x, y)
        glEnd()
        # --- ONDA AZUL ---
        glBegin(GL_LINE_STRIP)
        glColor3f(0.0, 0.5, 1.0) # Azul
        for x in [i/100 for i in range(-32, 33)]:
            y = -0.05 + 0.03 * math.sin(x * 15) 
            glVertex2f(x, y)
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()