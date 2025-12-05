import tkinter as tk
from queue import PriorityQueue, Queue
from datetime import datetime # Agregado para usar datetime si fuera necesario (aunque no se usa en este código final)

# --- 1. Configuración Global ---
ROWS = 20
COLS = 20
CELL_SIZE = 30 # Tamaño de cada celda en píxeles

# --- 2. Clase de la Celda (Nodo) ---
class Cell:
    """Representa un nodo en la cuadrícula."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.color = "white"

    def draw(self, canvas):
        """Dibuja la celda en el canvas de Tkinter."""
        x1 = self.col * CELL_SIZE
        y1 = self.row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline="gray")

    def __lt__(self, other):
        """Método de comparación para la PriorityQueue. Siempre False para evitar errores, ya que la prioridad se maneja con la tupla (score, cell)."""
        return False

# --- 3. Funciones de Utilidad de la Cuadrícula ---
def create_grid():
    """Crea la cuadrícula (matriz 2D) de objetos Cell."""
    return [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]

def draw_grid(canvas, grid):
    """Dibuja todo el grid en el canvas, limpiando el anterior."""
    canvas.delete("all")
    for row in grid:
        for cell in row:
            cell.draw(canvas)

def get_cell(event):
    """Obtiene la celda en la que se hizo clic."""
    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return grid[row][col]
    return None

def clear_paths():
    """Limpia los colores de los caminos encontrados, dejando solo inicio, fin y paredes."""
    for row in grid:
        for cell in row:
            if not (cell.is_start or cell.is_end or cell.is_wall):
                cell.color = "white"
                
# --- 4. Funciones de Interacción y Lógica Común ---
def on_click(event):
    """Maneja el clic del ratón para establecer inicio, fin o paredes."""
    global start_cell, end_cell
    cell = get_cell(event)
    if cell:
        # Establecer Inicio (Verde)
        if not start_cell and not cell.is_wall:
            cell.is_start = True
            cell.color = "green"
            start_cell = cell
        # Establecer Fin (Rojo)
        elif not end_cell and not cell.is_wall and cell != start_cell:
            cell.is_end = True
            cell.color = "red"
            end_cell = cell
        # Establecer/Quitar Pared (Negro/Blanco)
        elif cell != start_cell and cell != end_cell:
            cell.is_wall = not cell.is_wall
            cell.color = "black" if cell.is_wall else "white"
            
        clear_paths() # Limpiar caminos al cambiar obstáculos
        draw_grid(canvas, grid)

def h(a, b):
    """Función heurística de Distancia Manhattan (para A*)."""
    return abs(a.row - b.row) + abs(a.col - b.col)

def get_neighbors(cell):
    """Retorna los vecinos válidos (no paredes) de una celda."""
    neighbors = []
    # Movimiento en las 4 direcciones (arriba, abajo, izquierda, derecha)
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        r, c = cell.row + dr, cell.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            neighbor = grid[r][c]
            if not neighbor.is_wall:
                neighbors.append(neighbor)
    return neighbors

def reconstruct_path(came_from, current, color):
    """Traza el camino desde el final hasta el inicio y cuenta los pasos."""
    steps = 0
    while current in came_from:
        current = came_from[current]
        if not current.is_start:
            current.color = color
        steps += 1
    return steps

# --- 5. Algoritmos de Búsqueda ---

def run_a_star():
    """Ejecuta el algoritmo de búsqueda A*."""
    if not start_cell or not end_cell:
        return # No ejecutar si no hay inicio/fin
        
    clear_paths()
    open_set = PriorityQueue()
    open_set.put((0, start_cell))
    came_from = {}
    
    # Inicialización de scores y el conjunto abierto
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start_cell] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start_cell] = h(start_cell, end_cell)
    open_set_hash = {start_cell} # Conjunto para verificar rápidamente si un nodo está en la cola de prioridad
    
    explored = 0
    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)
        explored += 1

        if current == end_cell:
            steps = reconstruct_path(came_from, end_cell, "lightseagreen")
            draw_grid(canvas, grid)
            stats_astar.config(text=f"A*: Nodos Explorados: {explored}, Pasos del Camino: {steps}")
            return

        for neighbor in get_neighbors(current):
            # El coste de moverse a un vecino es 1 (g_score[current] + 1)
            temp_g_score = g_score[current] + 1 
            
            if temp_g_score < g_score[neighbor]:
                # Se encontró un camino mejor
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                # f_score = g_score + h (costo real + costo estimado)
                f_score[neighbor] = temp_g_score + h(neighbor, end_cell) 
                
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

def run_dijkstra():
    """Ejecuta el algoritmo de Dijkstra."""
    if not start_cell or not end_cell:
        return
        
    clear_paths()
    queue = PriorityQueue()
    queue.put((0, start_cell)) # Prioridad es la distancia
    came_from = {}
    distance = {cell: float("inf") for row in grid for cell in row}
    distance[start_cell] = 0
    visited = set()
    explored = 0
    
    while not queue.empty():
        dist, current = queue.get()
        
        if current in visited:
            continue
        
        visited.add(current)
        explored += 1

        if current == end_cell:
            steps = reconstruct_path(came_from, end_cell, "purple")
            draw_grid(canvas, grid)
            stats_dijkstra.config(text=f"Dijkstra: Nodos Explorados: {explored}, Pasos del Camino: {steps}")
            return

        for neighbor in get_neighbors(current):
            new_dist = distance[current] + 1 # Costo a vecino es 1
            
            if new_dist < distance[neighbor]:
                # Se encontró un camino más corto
                distance[neighbor] = new_dist
                came_from[neighbor] = current
                queue.put((new_dist, neighbor)) # Agregar/actualizar en la cola

def run_bfs():
    """Ejecuta el algoritmo de Búsqueda en Amplitud (BFS)."""
    if not start_cell or not end_cell:
        return
        
    clear_paths()
    queue = Queue() # Usamos la Queue estándar (FIFO)
    queue.put(start_cell)
    came_from = {}
    visited = set([start_cell])
    explored = 0
    
    while not queue.empty():
        current = queue.get()
        explored += 1
        
        if current == end_cell:
            steps = reconstruct_path(came_from, end_cell, "skyblue")
            draw_grid(canvas, grid)
            stats_bfs.config(text=f"BFS: Nodos Explorados: {explored}, Pasos del Camino: {steps}")
            return

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)

# --- 6. Funciones de Control de la Interfaz ---
def reset_grid():
    """Reinicia la cuadrícula y las estadísticas."""
    global start_cell, end_cell
    start_cell = None
    end_cell = None
    
    for row in grid:
        for cell in row:
            cell.is_start = False
            cell.is_end = False
            cell.is_wall = False
            cell.color = "white"
            
    draw_grid(canvas, grid)
    stats_astar.config(text="A*: ")
    stats_dijkstra.config(text="Dijkstra: ")
    stats_bfs.config(text="BFS: ")

# --- 7. Interfaz Tkinter ---
root = tk.Tk()
root.title("Comparación de Algoritmos de Búsqueda de Caminos")

# Crear el Canvas y la Cuadrícula
canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
canvas.pack()
grid = create_grid()
start_cell = None
end_cell = None

# Configurar eventos y dibujo inicial
canvas.bind("<Button-1>", on_click) # Clic izquierdo para configurar
draw_grid(canvas, grid)

# Marco para los botones
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

# Botones de Algoritmos
btn_astar = tk.Button(btn_frame, text="Ejecutar A*", command=run_a_star)
btn_astar.pack(side="left", padx=5)

btn_dijkstra = tk.Button(btn_frame, text="Ejecutar Dijkstra", command=run_dijkstra)
btn_dijkstra.pack(side="left", padx=5)

btn_bfs = tk.Button(btn_frame, text="Ejecutar BFS", command=run_bfs)
btn_bfs.pack(side="left", padx=5)

# Botón de Reinicio
reset_button = tk.Button(btn_frame, text="Reiniciar", command=reset_grid)
reset_button.pack(side="left", padx=5)

# Etiquetas de Estadísticas
stats_astar = tk.Label(root, text="A*: ")
stats_astar.pack()

stats_dijkstra = tk.Label(root, text="Dijkstra: ")
stats_dijkstra.pack()

stats_bfs = tk.Label(root, text="BFS: ")
stats_bfs.pack()

# Iniciar el bucle principal de la aplicación
root.mainloop()