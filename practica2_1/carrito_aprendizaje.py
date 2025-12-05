import tkinter as tk  # Para crear la interfaz gráfica de usuario
from tkinter import messagebox  # Para mostrar cuadros de mensaje de advertencia o información
import csv  # Para leer y escribir datos en archivos CSV (en este caso, los movimientos del carrito)
import time  # Para agregar pausas entre movimientos al reproducir la ruta

# --- Variables Globales (según la estructura original) ---
ruta = []  # Lista donde guardaremos los movimientos del carrito
archivo_csv = "ruta_carrito.csv"  # Nombre del archivo CSV donde se guardarán los movimientos
root = None  # Se inicializará más tarde con tk.Tk()
canvas = None  # Se inicializará más tarde con tk.Canvas
carrito = None  # Se inicializará más tarde con canvas.create_rectangle

def iniciar_aprendizaje(event):
    """Limpia la ruta anterior, crea el archivo CSV y notifica al usuario."""
    global ruta, archivo_csv, canvas, carrito
    
    # Muestra instrucciones al usuario
    messagebox.showinfo("Instrucciones", "Vamos a enseñarle a la IA a caminar. Presiona 'A' para comenzar.")
    
    ruta.clear()  # Limpiar la lista de movimientos para empezar un nuevo aprendizaje
    
    # Reinicia la posición del carrito a la posición inicial
    canvas.coords(carrito, 230, 230, 270, 270)
    
    try:
        # Crea y sobrescribe el archivo CSV con el encabezado
        with open(archivo_csv, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Movimiento", "X", "Y"])  # Escribir la cabecera del CSV
    except Exception as e:
        messagebox.showerror("Error de Archivo", f"No se pudo crear el archivo CSV: {e}")

def mover_carrito(event):
    """Mueve el carrito en el canvas y registra el movimiento en la lista y el archivo CSV."""
    global ruta, archivo_csv, canvas, carrito
    
    movimiento = event.keysym  # Obtiene la tecla presionada (Up, Down, Left, Right)
    
    # Mueve el carrito según la tecla presionada
    if movimiento == "Up":
        canvas.move(carrito, 0, -10)  # Mueve el carrito 10 píxeles hacia arriba
    elif movimiento == "Down":
        canvas.move(carrito, 0, 10)  # Mueve el carrito 10 píxeles hacia abajo
    elif movimiento == "Left":
        canvas.move(carrito, -10, 0)  # Mueve el carrito 10 píxeles hacia la izquierda
    elif movimiento == "Right":
        canvas.move(carrito, 10, 0)  # Mueve el carrito 10 píxeles hacia la derecha 
    else:
        return # Ignora otras teclas
        
    # Después de mover el carrito, obtenemos sus nuevas coordenadas (solo x1, y1)
    x1, y1, x2, y2 = canvas.coords(carrito)
    
    ruta.append((movimiento, x1, y1))  # Guardamos el movimiento y las nuevas coordenadas en la lista
    
    # Escribimos el movimiento en el archivo CSV (añadiendo)
    try:
        with open(archivo_csv, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Escribe el movimiento y la coordenada superior izquierda (redondeada para mejor lectura)
            writer.writerow([movimiento, round(x1, 2), round(y1, 2)])
    except Exception as e:
        # Imprime un error, pero no detiene la ejecución del movimiento
        print(f"Error al escribir en CSV: {e}")
        
def repetir_movimientos(event):
    """Reproduce los movimientos guardados en el archivo CSV."""
    global ruta, root, canvas, carrito
    
    if not ruta:  # Si no hay movimientos guardados, muestra un error
        messagebox.showerror("Error", "No hay movimientos guardados.")
        return
        
    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro que es todo por enseñarle?")
    
    if respuesta:  # Si el usuario confirma, reproduce los movimientos guardados
        try:
            ruta_reproducir = []
            
            # 1. Leer la ruta completa desde el archivo CSV
            with open(archivo_csv, "r", encoding="utf-8") as file:  # Abre el archivo CSV en modo lectura
                reader = csv.reader(file)
                next(reader)  # Salta el encabezado
                
                # Almacena solo el movimiento (primera columna)
                for row in reader:
                    ruta_reproducir.append(row[0])
            
            # 2. Reinicia la posición del carrito a la posición inicial
            canvas.coords(carrito, 230, 230, 270, 270)
            root.update()  # Actualiza la ventana para mostrar el reinicio
            
            # 3. Reproduce los movimientos guardados uno por uno
            for mov in ruta_reproducir:
                time.sleep(0.05)  # Pausa de 0.05 segundos entre movimientos
                root.update()  # Actualiza la ventana para ver el movimiento
                
                # Aplica el movimiento
                if mov == "Up":
                    canvas.move(carrito, 0, -10)
                elif mov == "Down":
                    canvas.move(carrito, 0, 10)
                elif mov == "Left":
                    canvas.move(carrito, -10, 0)
                elif mov == "Right":
                    canvas.move(carrito, 10, 0)
                    
            messagebox.showinfo("Éxito", "¡El carrito ha repetido la ruta aprendida!")

        except FileNotFoundError:
            messagebox.showerror("Error", "No hay ruta guardada para reproducir (archivo no encontrado).")
        except Exception as e:
             messagebox.showerror("Error de Reproducción", f"Ocurrió un error: {e}")

# --- Bloque Principal de Ejecución ---

# 1. Crea la ventana principal e inicializa las variables globales
root = tk.Tk()  # Crea la ventana principal
root.title("Simulación de Carrito IA")  # Asigna el título a la ventana

# 2. Crea el lienzo
canvas = tk.Canvas(root, width=500, height=500, bg="white")  # Crea un lienzo de 500x500 píxeles
canvas.pack()  # Añade el lienzo a la ventana

# 3. Crea el carrito (posición inicial 230, 230, 270, 270 es el centro para un lienzo de 500x500)
carrito = canvas.create_rectangle(230, 230, 270, 270, fill="blue")

# 4. Enlaza los eventos del teclado
root.bind("a", iniciar_aprendizaje)  # Al presionar "A", comienza el aprendizaje
root.bind("<Up>", mover_carrito)  # Al presionar "Up", mueve el carrito hacia arriba
root.bind("<Down>", mover_carrito)  # Al presionar "Down", mueve el carrito hacia abajo
root.bind("<Left>", mover_carrito)  # Al presionar "Left", mueve el carrito hacia la izquierda
root.bind("<Right>", mover_carrito)  # Al presionar "Right", mueve el carrito hacia la derecha
root.bind("i", repetir_movimientos)  # Al presionar "I", repite los movimientos guardados

# 5. Inicia el ciclo de la interfaz gráfica
root.mainloop()  # Inicia el ciclo de la interfaz 