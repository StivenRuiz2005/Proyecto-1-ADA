import tkinter as tk
import sys
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt

"""
Nombre: Carlos Stiven Ruiz Rojas
Descripcion: Implementación de algoritmos de fuerza bruta, programación dinámica y voraz para el problema de la terminal inteligente con interfaz.
Fecha: 21 / 10 / 2024
Ultima modificacion: 21 / 10 / 2024

"""
#FUNCIONALIDADES
def main():
    # Crear la ventana principal
    global palabra_inicial_entry, palabra_objetivo_entry, advance_entry, delete_entry, replace_entry, insert_entry, kill_entry, metodo_combobox, resultado_text
    root = tk.Tk()
    root.title("Transformación de Palabras")
    root.geometry("800x375")  # Ancho extendido para acomodar el Text al lado
    root.configure(bg="#223843")  # Fondo claro
    root.resizable(False, False)  # No permitir redimensionar la ventana

    # Estilos
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10, "bold"), foreground="black", background="#007BFF")
    style.configure("TLabel", font=("Helvetica", 10), background="#F4F4F9", foreground="#223843")
    style.configure("TEntry", foreground="#333", fieldbackground="#EAEAEA")
    style.configure("TCombobox", background="#F4F4F9", foreground="#333")
    style.map("TButton", background=[("active", "#0056b3")])

    # Crear un Frame contenedor para los campos y el Text a su lado
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    root.grid_columnconfigure(0, weight=1)  # Permitir crecimiento horizontal de la columna
    root.grid_rowconfigure(0, weight=1)  # Permitir crecimiento vertical de la fila

    # Agregar configuración para que las columnas dentro del frame crezcan adecuadamente
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=3)  # Para darle más espacio al Text

    # Crear un frame para los inputs y labels
    input_frame = ttk.Frame(main_frame)
    input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10, )

    # Crear otro frame para el Text (a la derecha del input_frame)
    text_frame = ttk.Frame(main_frame)
    text_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Crear etiquetas y campos de entrada dentro del input_frame
    tk.Label(input_frame, text="Palabra inicial:", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    palabra_inicial_entry = ttk.Entry(input_frame)
    palabra_inicial_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Palabra objetivo:", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    palabra_objetivo_entry = ttk.Entry(input_frame)
    palabra_objetivo_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Costo Advance:", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    advance_entry = ttk.Entry(input_frame)
    advance_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Costo Delete:", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="e")
    delete_entry = ttk.Entry(input_frame)
    delete_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Costo Replace:", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky="e")
    replace_entry = ttk.Entry(input_frame)
    replace_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Costo Insert:", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=5, column=0, padx=5, pady=5, sticky="e")
    insert_entry = ttk.Entry(input_frame)
    insert_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Costo Kill:", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=6, column=0, padx=5, pady=5, sticky="e")
    kill_entry = ttk.Entry(input_frame)
    kill_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="-------------------------------------------------------------------------------", bg="#F4F4F9", fg="#333", font=("Helvetica", 10, "bold")).grid(row=7, column=0, columnspan=2 ,padx=5, pady=5, sticky="ew")

    # Combobox para seleccionar el método
    tk.Label(input_frame, text="Método:", bg="#89959B", fg="#333", font=("Helvetica", 13, "bold")).grid(row=8, column=0, padx=5, pady=5, sticky="e")
    metodo_combobox = ttk.Combobox(input_frame, values=["Fuerza Bruta", "Greedy", "DP"])
    metodo_combobox.grid(row=8, column=1, padx=5, pady=5)
    metodo_combobox.current(0)  # Selección predeterminada

    # Botón para ejecutar el cálculo
    calcular_button = ttk.Button(input_frame, text="Calcular", command=calcular_transformacion)
    calcular_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    # TextField para mostrar el resultado dentro del text_frame
    resultado_text = tk.Text(text_frame, height=18, width=40, bg="#BCC3C7", fg="#333", font=("Helvetica", 10))
    resultado_text.pack(fill=tk.BOTH, expand=True)
    
    mostrar_tiempo = ttk.Button(text_frame, text="Mostrar Tiempo", command=dibujar_grafica)
    mostrar_tiempo.pack(pady=14)

    # Ejecutar la aplicación
    root.mainloop()

def brute_force_transform(x, y, a, d, r, i, k):
    def rec_transform(x_i, y_i, x, y):
        # Caso base: Si llegamos al final de ambas cadenas
        if x_i == len(x) and y_i == len(y):
            return 0, []

        # Caso base: Si llegamos al final de 'x' y faltan caracteres en 'y', necesitamos insertar
        if x_i == len(x):
            return (len(y) - y_i) * i, ['insert'] * (len(y) - y_i)  # Insertar los caracteres restantes de 'y'

        # Caso base: Si llegamos al final de 'y' y faltan caracteres en 'x', debemos hacer kill
        if y_i == len(y):
            return k, ['kill']  # Borrar todos los caracteres restantes de 'x'

        # Iniciamos el costo con un valor alto y una lista vacía de operaciones
        min_cost = sys.maxsize
        operations = []

        # 1. Advance: Si los caracteres son iguales, avanzamos y sumamos el costo de advance
        if x[x_i] == y[y_i]:
            cost, ops = rec_transform(x_i + 1, y_i + 1, x, y)
            cost += a
            if cost < min_cost:
                min_cost = cost
                operations = ['advance'] + ops

        # 2. Replace: Si los caracteres son diferentes, reemplazamos y sumamos el costo de replace
        cost, ops = rec_transform(x_i + 1, y_i + 1, x, y)
        cost += r
        if cost < min_cost:
            min_cost = cost
            operations = ['replace'] + ops

        # 3. Delete: Borrar el carácter en la posición actual de 'x'
        cost, ops = rec_transform(x_i + 1, y_i, x, y)
        cost += d
        if cost < min_cost:
            min_cost = cost
            operations = ['delete'] + ops

        # 4. Insert: Insertar el carácter de 'y' en 'x'
        cost, ops = rec_transform(x_i, y_i + 1, x, y)
        cost += i
        if cost < min_cost:
            min_cost = cost
            operations = ['insert'] + ops

        return min_cost, operations

    # Llamada inicial a la función recursiva
    min_cost, operations = rec_transform(0, 0, x, y)
    return min_cost, operations

def greedy_transform(x, Y, a, d, r, i, k):
    n = len(x)
    m = len(Y)

    # Variables para los punteros en ambas cadenas
    cost = 0
    x_idx = 0  # Índice para x (cadena original)
    Y_idx = 0  # Índice para Y (cadena destino)
    
    # Lista para almacenar el camino de operaciones
    operations = []
    while x_idx < n and Y_idx < m:
        if x[x_idx] == Y[Y_idx]:
            # Avanzamos si los caracteres coinciden
            x_idx += 1
            Y_idx += 1
            cost += a  # Costo de avanzar
            operations.append('advance')
        else:
            # Reemplazamos si no coinciden
            cost += r
            x_idx += 1
            Y_idx += 1
            operations.append('replace')

    # Si queda algo por eliminar en x (hemos terminado Y)
    while x_idx < n:
        # Decidimos si eliminar los caracteres restantes o hacer kill
        if n - x_idx > 1:  # Si quedan varios caracteres, usamos kill
            cost += k
            operations.append('kill')
            break
        else:
            cost += d  # Si queda solo uno, eliminamos
            operations.append('delete')
            x_idx += 1

    # Si queda algo por insertar en Y (hemos terminado x)
    while Y_idx < m:
        cost += i  # Insertamos caracteres restantes en Y
        operations.append('insert')
        Y_idx += 1

    return cost, operations

def dp_transform(x, y, a, d, r, i, k):
    return None, ['None', 'None', 'None', 'None']

def dibujar_grafica():
    try:
        n = promedio_bruta.__len__()
        tamanos = [2**i for i in range(1, n)]
        plt.figure(figsize=(10, 6))
        print(promedio_bruta)
        plt.plot(tamanos, promedio_bruta, label="Fuerza Bruta", marker="o")
        #plt.plot(tamanos, promedio_bruta, label="Greedy", marker="s")
        #plt.plot(tamanos, promedio_dp, label="Dinámico", marker="^")

        # Configuración de escala logarítmica
        plt.xscale("log")
        plt.yscale("log")

        # Etiquetas y título
        plt.xlabel("Tamaño de la entrada (longitud de las cadenas)")
        plt.ylabel("Tiempo de ejecución (segundos)")
        plt.title("Comparación de tiempos de ejecución por método")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)

        # Mostrar la gráfica
        plt.show()
    except:
        messagebox.showerror("Error", "No se han realizado cálculos aún.")


def calcular_transformacion():
    x = palabra_inicial_entry.get()
    y = palabra_objetivo_entry.get()

    # Obtener los valores de costo
    try:
        a = int(advance_entry.get())
        d = int(delete_entry.get())
        r = int(replace_entry.get())
        i = int(insert_entry.get())
        k = int(kill_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Todos los costos deben ser números enteros.")
        return

    # Selección del método
    metodo = metodo_combobox.get()
    if metodo == "Fuerza Bruta":
        start_time = time.time()
        costo, operaciones= brute_force_transform(x, y, a, d, r, i, k)
        tiempo = time.time() - start_time
        promedio_bruta.append(tiempo)
        print(promedio_bruta)
    elif metodo == "Greedy":
        start_time = time.time()
        costo, operaciones = greedy_transform(x, y, a, d, r, i, k)
        tiempo = time.time() - start_time
        promedio_greedy.append(tiempo)
    elif metodo == "DP":
        start_time = time.time()
        costo, operaciones = dp_transform(x, y, a, d, r, i, k)
        tiempo = time.time() - start_time
        promedio_dp.append(tiempo)
    else:
        messagebox.showerror("Error", "Método no válido.")
        return

    # Mostrar resultado en el text field
    resultado_text.delete(1.0, tk.END)  # Limpiar el campo de texto
    resultado_text.insert(tk.END, f"Costo mínimo: {costo}\n")
    resultado_text.insert(tk.END, "Operaciones: " + ", ".join(operaciones))
    resultado_text.insert(tk.END, f"\nTiempo de ejecución: {tiempo:.6f} segundos")


#INTERFAZ


    
if __name__ == "__main__":
    global promedio_bruta, promedio_greedy, promedio_dp
    promedio_bruta = []
    promedio_greedy = []
    promedio_dp = []
    main()