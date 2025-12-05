import tkinter as tk  # Para crear la ventana y los gráficos
import csv  # Para guardar datos en archivos CSV
import heapq  # Para usar colas de prioridad (esencial para A*)

TAM_CELDA = 40  # Cada celda del laberinto será un cuadrado de 40x40 píxeles
# Definición del laberinto (matriz de 19x16)
# (1 = pared, 0 = camino, A = inicio, B = fin)
laberinto = [
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "A", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "B", "1"],
    ["1", "1", "1", "0", "1", "1", "1", "0", "1", "0", "1", "0", "1", "0", "1", "1"],
    ["1", "0", "1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "1"],
    ["1", "0", "1", "1", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1"],
    ["1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "1"],
    ["1", "1", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "0", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "0", "0", "1", "0", "1", "0", "0", "1", "0", "1"],
    ["1", "0", "1", "1", "1", "1", "1", "0", "1", "0", "1", "0", "1", "1", "0", "1"],
    ["1", "0", "1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "1"],
    ["1", "0", "1", "0", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "0", "1", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"],
    ["1", "0", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "0", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0", "0", "0", "1"],
    ["1", "0", "1", "1", "1", "0", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1"],
    ["1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
]

class LaberintoApp:
    def __init__(self, root, lab):
        self.root = root  # Esto es la ventana principal del programa.
        self.laberinto = lab  # Aquí guardamos el laberinto (la matriz de números).
        self.inicio, self.fin = self.encontrar_puntos()  # Busca dónde está A (inicio) y B (meta).
        
        # Tamaño del laberinto (filas y columnas).
        self.alto = len(lab)  # Cuántas filas tiene.
        self.ancho = len(lab[0])  # Cuántas columnas tiene.
        
        # Creamos un “lienzo” (como una hoja de dibujo) donde pondremos el laberinto.
        self.canvas = tk.Canvas(
            root, 
            width=self.ancho * TAM_CELDA,  # Ancho total (columnas * tamaño de cada celda).
            height=self.alto * TAM_CELDA    # Alto total (filas * tamaño de cada celda).
        )
        self.canvas.pack()  # Lo añadimos a la ventana.
        
        # Dibujamos el laberinto por primera vez.
        self.dibujar_laberinto()
        
        # Coordenadas de la celda de inicio
        inicio_i, inicio_j = self.inicio
        
        # Creamos la bolita verde (nuestro “agente inteligente”).
        self.bolita = self.canvas.create_oval(
            inicio_j * TAM_CELDA + 10,  # Posición X
            inicio_i * TAM_CELDA + 10,  # Posición Y
            inicio_j * TAM_CELDA + 30,
            inicio_i * TAM_CELDA + 30,
            fill="green"  # Color verde.
        )
        
        # Buscamos el mejor camino usando el algoritmo A*.
        self.camino = self.buscar_camino()
        
        # Hacemos que la bolita se mueva por ese camino.
        if self.camino:
            self.explorar()
        else:
            print("No se encontró un camino a la meta (B).")

    def dibujar_laberinto(self):
        """Dibuja cada celda del laberinto con colores."""
        for i, fila in enumerate(self.laberinto):  # Recorre cada fila.
            for j, celda in enumerate(fila):  # Recorre cada celda en la fila.
                # Coordenadas de la celda (esquina superior izquierda).
                x1, y1 = j * TAM_CELDA, i * TAM_CELDA
                # Coordenadas de la esquina inferior derecha.
                x2, y2 = x1 + TAM_CELDA, y1 + TAM_CELDA
                
                # Elegimos el color según lo que haya en la celda.
                if celda == "1":
                    color = "black"  # Pared (no se puede pasar).
                elif celda == "A":
                    color = "white"  # Inicio (fondo blanco). 
                elif celda == "B":
                    color = "red"    # Meta (rojo).
                else:
                    color = "white"  # Camino libre (blanco).
                
                # Dibujamos la celda como un rectángulo.
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,  # Color de relleno.
                    outline="gray",  # Borde gris para separar celdas.
                    tags="grid" # Etiqueta para el fondo del laberinto
                )

    def encontrar_puntos(self):
        """Busca y retorna las coordenadas (fila, columna) de 'A' y 'B'."""
        inicio, fin = None, None
        for i, fila in enumerate(self.laberinto):
            for j, celda in enumerate(fila):
                if celda == "A":
                    inicio = (i, j)
                elif celda == "B":
                    fin = (i, j)
        return inicio, fin

    def heuristica(self, nodo):
        """Calcula la distancia de Manhattan (h) desde un nodo hasta la meta."""
        return abs(nodo[0] - self.fin[0]) + abs(nodo[1] - self.fin[1])

    def buscar_camino(self):
        """Implementa el algoritmo A* para encontrar el camino más corto."""
        
        # open_list: (f_score, g_score, nodo)
        open_list = [(0 + self.heuristica(self.inicio), 0, self.inicio)]
        # g_score: costo real desde el inicio hasta el nodo
        g_score = {self.inicio: 0}
        # came_from: guarda el nodo anterior para reconstruir el camino
        came_from = {} 

        while open_list:
            # Obtiene el nodo con el menor f_score (f = g + h)
            _, g_current, current_node = heapq.heappop(open_list)

            if current_node == self.fin:
                # Reconstruir camino:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.append(self.inicio)
                return path[::-1] # Retorna la lista de nodos en orden de inicio a fin

            i, j = current_node
            
            # Explora vecinos (arriba, abajo, izquierda, derecha)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + dx, j + dy
                neighbor = (ni, nj)
                
                # Comprueba límites y si la celda es transitable (0 o B)
                if 0 <= ni < self.alto and 0 <= nj < self.ancho and self.laberinto[ni][nj] in ["0", "B"]:
                    
                    tentative_g_score = g_current + 1
                    
                    # Si encontramos una ruta mejor al vecino
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current_node # Guarda el paso anterior
                        g_score[neighbor] = tentative_g_score # Actualiza el costo real
                        f_score = tentative_g_score + self.heuristica(neighbor)
                        heapq.heappush(open_list, (f_score, tentative_g_score, neighbor))
        
        return []  # No se encontró camino

    def explorar(self):
        """Mueve la bolita a través del camino óptimo, coloreando las celdas."""
        print("Explorando el camino...")
        
        # Crear un archivo CSV para registrar el recorrido
        with open("exploracion.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Fila", "Columna"])
            
            for i, j in self.camino:
                # 1. Mover la bolita a las nuevas coordenadas
                self.canvas.coords(
                    self.bolita,
                    j * TAM_CELDA + 10,
                    i * TAM_CELDA + 10,
                    j * TAM_CELDA + 30,
                    i * TAM_CELDA + 30
                )
                
                # 2. Colorear la celda como camino recorrido (amarillo)
                x1, y1 = j * TAM_CELDA, i * TAM_CELDA
                x2, y2 = x1 + TAM_CELDA, y1 + TAM_CELDA
                
                # Evita recolorear el inicio (A) y la meta (B)
                if self.laberinto[i][j] not in ["A", "B"]:
                    # Dibuja el rectángulo amarillo detrás de la bolita
                    rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="gray", tags="path")
                    self.canvas.lower(rect_id) # CORRECCIÓN: Usar self.canvas.lower(ID)
                
                # 3. Registrar y Pausar
                writer.writerow([i, j])
                self.canvas.update()
                self.canvas.after(200) # Espera 200ms para que sea visible
            
        print("Llegó a la meta")

# --- Bloque de Inicialización y Ejecución ---

# Ejecutar interfaz
root = tk.Tk()
root.title("Laberinto con A* - Camino Óptimo")
app = LaberintoApp(root, laberinto)
root.mainloop()