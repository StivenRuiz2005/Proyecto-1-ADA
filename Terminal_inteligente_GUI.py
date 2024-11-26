import tkinter as tk
import sys
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
import numpy as np
import customtkinter as ctk

"""
Descripcion: Implementación de algoritmos de fuerza bruta, programación dinámica y voraz para el problema de la terminal inteligente con interfaz.
Fecha: 21 / 10 / 2024
Ultima modificacion: 24 / 11 / 2024

"""
def main():
    global palabra_inicial_entry, palabra_objetivo_entry, advance_entry, delete_entry, replace_entry, insert_entry, kill_entry, metodo_combobox, resultado_text
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Transformación de Palabras")
    root.geometry("1200x700")
    root.resizable(False, False)

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    input_frame = ctk.CTkFrame(main_frame, width=400)
    input_frame.pack(side="left", fill="y", padx=10, pady=10)
    input_frame.pack_propagate(False)

    text_frame = ctk.CTkFrame(main_frame, width=700)
    text_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    text_frame.pack_propagate(False)

    # Input fields
    ctk.CTkLabel(input_frame, text="Palabra inicial:", font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
    palabra_inicial_entry = ctk.CTkEntry(input_frame, font=("Helvetica", 14), width=200)
    palabra_inicial_entry.pack(pady=(0, 5))

    ctk.CTkLabel(input_frame, text="Palabra objetivo:", font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
    palabra_objetivo_entry = ctk.CTkEntry(input_frame, font=("Helvetica", 14), width=200)
    palabra_objetivo_entry.pack(pady=(0, 5))

    ctk.CTkLabel(input_frame, text="Costo Advance:", font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
    advance_entry = ctk.CTkEntry(input_frame, font=("Helvetica", 14), width=200)
    advance_entry.pack(pady=(0, 5))

    ctk.CTkLabel(input_frame, text="Costo Delete:", font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
    delete_entry = ctk.CTkEntry(input_frame, font=("Helvetica", 14), width=200)
    delete_entry.pack(pady=(0, 5))

    ctk.CTkLabel(input_frame, text="Costo Replace:", font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
    replace_entry = ctk.CTkEntry(input_frame, font=("Helvetica", 14), width=200)
    replace_entry.pack(pady=(0, 5))

    ctk.CTkLabel(input_frame, text="Costo Insert:", font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
    insert_entry = ctk.CTkEntry(input_frame, font=("Helvetica", 14), width=200)
    insert_entry.pack(pady=(0, 5))

    ctk.CTkLabel(input_frame, text="Costo Kill:", font=("Helvetica", 14, "bold")).pack(pady=(10, 2))
    kill_entry = ctk.CTkEntry(input_frame, font=("Helvetica", 14), width=200)
    kill_entry.pack(pady=(0, 5))

    ctk.CTkLabel(input_frame, text="", height=1).pack(pady=5)

    ctk.CTkLabel(input_frame, text="Método:", font=("Helvetica", 16, "bold")).pack(pady=(5, 2))
    metodo_combobox = ctk.CTkOptionMenu(input_frame, values=["Fuerza Bruta", "Greedy", "DP"], 
                                        font=("Helvetica", 14), width=200)
    metodo_combobox.pack(pady=(0, 5))

    calcular_button = ctk.CTkButton(input_frame, text="Calcular", command=calcular_transformacion, 
                                    font=("Helvetica", 16, "bold"), height=40, width=200)
    calcular_button.pack(pady=(5, 10))

    resultado_text = ctk.CTkTextbox(text_frame, font=("Helvetica", 14), width=680, height=500)
    resultado_text.pack(pady=20, padx=20, fill="both", expand=True)

    mostrar_tiempo = ctk.CTkButton(text_frame, text="Mostrar Tiempo", command=dibujar_grafica_terminal, 
                                   font=("Helvetica", 16, "bold"), height=40, width=200)
    mostrar_tiempo.pack(pady=20)

    root.mainloop()

def brute_force_transform(x, y, a, d, r, i, k):
    def rec_transform(x_i, y_i, x, y):
    
        if x_i == len(x) and y_i == len(y):
            return 0, []

       
        if x_i == len(x):
            return (len(y) - y_i) * i, ['insert'] * (len(y) - y_i)  

        
        if y_i == len(y):
            return k, ['kill']  

        
        min_cost = sys.maxsize
        operations = []

        
        if x[x_i] == y[y_i]:
            cost, ops = rec_transform(x_i + 1, y_i + 1, x, y)
            cost += a
            if cost < min_cost:
                min_cost = cost
                operations = ['advance'] + ops

        
        cost, ops = rec_transform(x_i + 1, y_i + 1, x, y)
        cost += r
        if cost < min_cost:
            min_cost = cost
            operations = ['replace'] + ops

        
        cost, ops = rec_transform(x_i + 1, y_i, x, y)
        cost += d
        if cost < min_cost:
            min_cost = cost
            operations = ['delete'] + ops

        
        cost, ops = rec_transform(x_i, y_i + 1, x, y)
        cost += i
        if cost < min_cost:
            min_cost = cost
            operations = ['insert'] + ops

        return min_cost, operations

    
    min_cost, operations = rec_transform(0, 0, x, y)
    return min_cost, operations

def greedy_transform(x, Y, a, d, r, i, k):
    n = len(x)
    m = len(Y)

    
    cost = 0
    x_idx = 0  
    Y_idx = 0  
    
    operations = []
    while x_idx < n and Y_idx < m:
        if x[x_idx] == Y[Y_idx]:
            x_idx += 1
            Y_idx += 1
            cost += a  
            operations.append('advance')
        else:
            
            cost += r
            x_idx += 1
            Y_idx += 1
            operations.append('replace')

    while x_idx < n:
        
        if n - x_idx > 1: 
            cost += k
            operations.append('kill')
            break
        else:
            cost += d 
            operations.append('delete')
            x_idx += 1

    while Y_idx < m:
        cost += i 
        operations.append('insert')
        Y_idx += 1

    return cost, operations

def dp_transform(source, target, a, d, r, i, k):  
    n = len(source)
    m = len(target)
    
    
    dp = np.full((n + 1, m + 1, 2), float('inf'))
    operation_trace = [[[] for _ in range(m + 1)] for _ in range(n + 1)]
    
    # Caso base
    dp[n][m][0] = 0
    dp[n][m][1] = 0
    operation_trace[n][m] = []

    def min_cost(x, y, cursor):
        if dp[x][y][cursor] != float('inf'):
            return dp[x][y][cursor]
            
        cost = float('inf')
        best_operations = None
        
        if x < n:
            # ADVANCE
            if y < m and source[x] == target[y] and cursor == 0:
                next_cost = min_cost(x + 1, y + 1, 0) + a
                if next_cost < cost:
                    cost = next_cost
                    best_operations = operation_trace[x + 1][y + 1] + ['advance']
            
            # DELETE
            if cursor == 0:
                next_cost = min_cost(x + 1, y, 0) + d
                if next_cost < cost:
                    cost = next_cost
                    best_operations = operation_trace[x + 1][y] + ['delete']
            
            # REPLACE
            if y < m and cursor == 0:
                next_cost = min_cost(x + 1, y + 1, 0) + r
                if next_cost < cost:
                    cost = next_cost
                    best_operations = operation_trace[x + 1][y + 1] + ['replace']
            
            # KILL
            if cursor == 0:
                remaining = m - y
                next_cost = k + remaining * i
                if next_cost < cost:
                    cost = next_cost
                    best_operations = ['kill'] + ['insert'] * remaining
        
        # INSERT
        if y < m:
            next_cost = min_cost(x, y + 1, cursor) + i
            if next_cost < cost:
                cost = next_cost
                best_operations = operation_trace[x][y + 1] + ['insert']
        
        dp[x][y][cursor] = cost
        operation_trace[x][y] = best_operations
        return cost
    
    # Calcular el costo mínimo
    total_cost = min_cost(0, 0, 0)
    sequence = operation_trace[0][0][::-1]  # Invertimos el orden de las operaciones al final

    return total_cost, sequence

def dibujar_grafica_terminal(): 
    try:
        if promedio_bruta.__len__()  == 0 and promedio_greedy.__len__() == 0 and promedio_dp.__len__() == 0:
            messagebox.showerror("Error", "No se han realizado cálculos aún.")
            return
        if promedio_greedy.__len__() == promedio_bruta.__len__() and promedio_dp.__len__() == promedio_bruta.__len__():
            n = promedio_bruta.__len__()
            tamanos = [2**i for i in range(1, n+1)]
            plt.figure(figsize=(10, 6))
            plt.plot(tamanos, promedio_bruta, label="Fuerza Bruta", marker="o")
            plt.plot(tamanos, promedio_greedy, label="Greedy", marker="s")
            plt.plot(tamanos, promedio_dp, label="Dinámico", marker="^")

            plt.xscale("log")
            plt.yscale("log")

            plt.xlabel("Tamaño de la entrada (longitud de las cadenas)")
            plt.ylabel("Tiempo de ejecución (segundos)")
            plt.title("Comparación de tiempos de ejecución por método")
            plt.legend()
            plt.grid(True, which="both", linestyle="--", linewidth=0.5)
            plt.show()
        else:
            messagebox.showerror("Error", "No se han realizado cálculos con todos los métodos.")
    except:
        messagebox.showerror("Error", "No se han realizado cálculos aún.")

def calcular_transformacion():
    x = palabra_inicial_entry.get()
    y = palabra_objetivo_entry.get()

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
        start_time = time.perf_counter()
        costo, operaciones= brute_force_transform(x, y, a, d, r, i, k)
        tiempo = time.perf_counter() - start_time
        promedio_bruta.append(tiempo)
    elif metodo == "Greedy":
        start_time = time.perf_counter()
        costo, operaciones = greedy_transform(x, y, a, d, r, i, k)
        tiempo = time.perf_counter() - start_time
        promedio_greedy.append(tiempo)
    elif metodo == "DP":
        start_time = time.perf_counter()
        costo, operaciones = dp_transform(x, y, a, d, r, i, k)
        tiempo = time.perf_counter() - start_time
        promedio_dp.append(tiempo)
    else:
        messagebox.showerror("Error", "Método no válido.")
        return


    resultado_text.delete(1.0, tk.END)
    resultado_text.insert(tk.END, f"Costo mínimo: {costo}\n")
    resultado_text.insert(tk.END, "Operaciones: \n" + ", \n".join(operaciones))
    resultado_text.insert(tk.END, f"\nTiempo de ejecución: {tiempo:.20f} segundos")

if __name__ == "__main__":
    global promedio_bruta, promedio_greedy, promedio_dp
    promedio_bruta = []
    promedio_greedy = []
    promedio_dp = []
    main()