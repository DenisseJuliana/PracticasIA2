import numpy as np  # Para cálculos matemáticos
import matplotlib.pyplot as plt  # Para gráficos
import matplotlib.animation as animation  # Para animaciones
from matplotlib.patches import Rectangle  # Para dibujar los objetos
import csv  # Para guardar datos en un archivo CSV
import os  # Para manejar rutas de archivos

class SensorAnimado:
    """
    Simula el movimiento de un objeto (azul) en relación con un sensor fijo (rojo)
    y guarda la distancia calculada en un archivo CSV.
    """
    def __init__(self):
        self.fig, self.ax = plt.subplots()  # Crear la figura y los ejes
        self.ax.set_xlim(0, 10)  # Limitar el área en X
        self.ax.set_ylim(0, 10)  # Limitar el área en Y
        self.ax.set_aspect('equal', adjustable='box') # Mantener la proporción
        
        # Cuadrado-sensor (fijo)
        self.sensor = Rectangle((1, 1), 1, 1, color='r')  # Sensor en posición fija
        self.ax.add_patch(self.sensor)
        
        # Cuadrado-objeto (móvil)
        self.objeto = Rectangle((8, 7), 1, 1, color='b')  # Objeto que se moverá
        self.ax.add_patch(self.objeto)
        
        # Texto de distancia en la pantalla
        self.dist_text = self.ax.text(0.5, 9.5, "Distancia: 0.00", fontsize=12)
        
        # Configuración del archivo CSV
        self.csv_file = 'datos_sensor.csv'
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Frame', 'Pos_X', 'Pos_Y', 'Distancia'])
            
        # Inicializar la animación
        self.anim = animation.FuncAnimation(
            self.fig, self.actualizar, frames=60, interval=100, blit=False
        )

    def actualizar(self, frame):
        """
        Función de actualización llamada en cada fotograma de la animación.
        Mueve el objeto, calcula la distancia y guarda los datos.
        """
        # Mover el objeto en círculos (basado en el seno y coseno)
        angle = frame * 0.1  # Ángulo para el movimiento
        x = 5 + 3 * np.cos(angle)  # Nueva posición X
        y = 5 + 3 * np.sin(angle)  # Nueva posición Y
        
        self.objeto.set_xy((x, y))  # Actualizar posición del objeto (esquina inferior izquierda)
        
        # Calcular distancia. El sensor está centrado en (1.5, 1.5)
        distancia = np.sqrt((x - 1.5)**2 + (y - 1.5)**2)
        
        self.dist_text.set_text(f"Distancia: {distancia:.2f}")
        
        # Guardar datos en CSV
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([frame, x, y, distancia])
            
        return self.objeto, self.dist_text, self.dist_text

# --- Ejecución principal ---
if __name__ == "__main__":
    sensor = SensorAnimado()
    plt.show()
    
    # Muestra la ruta del archivo CSV al finalizar
    print(f"Datos guardados en: {os.path.abspath(sensor.csv_file)}")