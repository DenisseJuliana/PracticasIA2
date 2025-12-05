import tkinter as tk # Para la interfaz gráfica
import math # Para cálculos matemáticos (distancia)

class SensorInteractivo:
    """
    Simula la interacción entre un sensor fijo (rojo) y un objeto movible (azul)
    en un lienzo (Canvas) de Tkinter, calculando y mostrando la distancia entre ellos.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sensor")  # Título de la ventana
        
        # Canvas (área de dibujo)
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()
        
        # Sensor (cuadrado rojo fijo) - Coordenadas (x1, y1, x2, y2)
        self.sensor = self.canvas.create_rectangle(50, 50, 100, 100, fill="red", tags="sensor")
        
        # Objeto (cuadrado azul movible)
        self.objeto = self.canvas.create_rectangle(300, 300, 350, 350, fill="blue", tags="objeto")
        
        # Etiqueta de distancia
        self.label_distancia = tk.Label(root, text="Distancia: 0 píxeles", font=("Arial", 14))
        self.label_distancia.pack()
        
        # 🔑 Conectar las teclas de flecha al método mover_objeto
        # Se necesita un 'focus' para que el evento de teclado sea capturado
        self.root.bind("<Key>", self.mover_objeto)
        
        # Inicializar la distancia
        self.actualizar_distancia()

    def mover_objeto(self, event):
        """
        Maneja el evento de teclado (flechas) para mover el objeto.
        """
        x, y = 0, 0
        
        if event.keysym == "Up":
            y = -10  # Mover arriba
        elif event.keysym == "Down":
            y = 10   # Mover abajo
        elif event.keysym == "Left":
            x = -10  # Mover izquierda
        elif event.keysym == "Right":
            x = 10   # Mover derecha
            
        self.canvas.move("objeto", x, y)  # Actualiza posición en el canvas
        self.actualizar_distancia()      # Recalcula distancia

    def actualizar_distancia(self):
        """
        Calcula la distancia euclidiana entre el centro del sensor y el centro del objeto.
        """
        # 1. Obtener coordenadas del sensor [x1, y1, x2, y2]
        sensor_coords = self.canvas.coords("sensor")
        # Calcular el centro del sensor
        sensor_cx = (sensor_coords[0] + sensor_coords[2]) / 2
        sensor_cy = (sensor_coords[1] + sensor_coords[3]) / 2

        # 2. Obtener coordenadas del objeto [x1, y1, x2, y2]
        objeto_coords = self.canvas.coords("objeto")
        # Calcular el centro del objeto
        objeto_cx = (objeto_coords[0] + objeto_coords[2]) / 2
        objeto_cy = (objeto_coords[1] + objeto_coords[3]) / 2

        # 3. Aplicar la fórmula de la distancia euclidiana
        # Distancia = sqrt((x2 - x1)^2 + (y2 - y1)^2)
        distancia = math.sqrt((objeto_cx - sensor_cx)**2 + (objeto_cy - sensor_cy)**2)
        
        # 4. Actualizar la etiqueta
        self.label_distancia.config(text=f"Distancia: {int(distancia)} píxeles")

# --- Bloque principal de ejecución ---
if __name__ == "__main__":
    root = tk.Tk()           # Crear ventana principal
    app = SensorInteractivo(root)  # Iniciar el simulador
    root.mainloop()          # Mantener la ventana abierta