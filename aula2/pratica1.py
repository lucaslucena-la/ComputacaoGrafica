import glfw
from OpenGL.GL import *

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Coelho de Triângulos", None, None)
    
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
    
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_TRIANGLES)

        glColor3f(0.8, 0.8, 0.8)
        glVertex2f(-0.5, -0.7) # Inferior Esquerdo
        glVertex2f(0.5, -0.7)  # Inferior Direito
        glVertex2f(0.0, 0.0)   # Topo (pescoço)

        # --- CABEÇA 
        glColor3f(0.8, 0.8, 0.8)
        glVertex2f(-0.3, 0.0)  # Base Esquerda
        glVertex2f(0.3, 0.0)   # Base Direita
        glVertex2f(0.0, 0.5)   # Topo da cabeça

        # --- ORELHA ESQUERDA (
        glColor3f(0.9, 0.8, 0.8)
        glVertex2f(-0.25, 0.4) 
        glVertex2f(-0.05, 0.55)
        glVertex2f(-0.2, 1.0)  

        # --- ORELHA DIREITA 
        glColor3f(0.9, 0.8, 0.8)
        glVertex2f(0.05, 0.55)
        glVertex2f(0.25, 0.4)
        glVertex2f(0.2, 1.0)
        
        # --- OLHO ESQUERDO (Preto) ---
        glColor3f(0.0, 0.0, 0.0)    # Cor preta
        glVertex2f(-0.15, 0.35)     # Base Esquerda
        glVertex2f(-0.05, 0.35)     # Base Direita
        glVertex2f(-0.1, 0.45)      # Topo do olho

        # --- OLHO DIREITO (Preto) ---
        glColor3f(0.0, 0.0, 0.0)    # Cor preta
        glVertex2f(0.05, 0.35)      # Base Esquerda
        glVertex2f(0.15, 0.35)      # Base Direita
        glVertex2f(0.1, 0.45)       # Topo do olho

        # --- FOCINHO 
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(-0.08, 0.18) 
        glVertex2f(0.08, 0.18)  
        glVertex2f(0.0, 0.08)
        
        

        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

main()