import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import time
import customtkinter as ctk
"""
Descripcion: Implementación de algoritmos de fuerza bruta, programación dinámica y voraz para el problema de la subasta publica con interfaz.
Fecha: 21 / 10 / 2024
Ultima modificacion: 25 / 11 / 2024

"""

def interfaz():
    global entry_total_acciones, entry_precio_minimo, entry_gob_precio, combo_algoritmo, resultado_text, entry_oferentes, frame_oferentes, frame_acciones, frame_precio_minimo, frame_gobierno, frame_algoritmo,algoritmito,tiempito
    
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Asignación de Acciones")
    root.geometry("1200x800")  # Increased window size
    root.resizable(False, False)  # Make the window non-resizable

    # Main frame to hold all content
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Left frame
    frame_izquierda = ctk.CTkFrame(main_frame, width=300)
    frame_izquierda.pack(side="left", fill="y", padx=10, pady=10)
    frame_izquierda.pack_propagate(False)  # Prevent frame from shrinking

    # Middle frame
    frame_medio = ctk.CTkFrame(main_frame, width=500)
    frame_medio.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    frame_medio.pack_propagate(False)  # Prevent frame from shrinking

    # Right frame
    frame_derecha = ctk.CTkFrame(main_frame, width=300)
    frame_derecha.pack(side="left", fill="y", padx=10, pady=10)
    frame_derecha.pack_propagate(False)  # Prevent frame from shrinking

    # --- Left Section: Inputs and Controls ---
    ctk.CTkLabel(frame_izquierda, text="Configuración", font=("Arial", 20, "bold")).pack(pady=20)

    # Total shares input
    ctk.CTkLabel(frame_izquierda, text="Total de acciones:").pack(pady=(10, 0))
    entry_total_acciones = ctk.CTkEntry(frame_izquierda, placeholder_text="Ingrese el total")
    entry_total_acciones.pack(pady=(0, 10), padx=20, fill="x")

    # Minimum price input
    ctk.CTkLabel(frame_izquierda, text="Precio mínimo:").pack(pady=(10, 0))
    entry_precio_minimo = ctk.CTkEntry(frame_izquierda, placeholder_text="Ingrese el precio mínimo")
    entry_precio_minimo.pack(pady=(0, 10), padx=20, fill="x")

    # Government price input
    ctk.CTkLabel(frame_izquierda, text="Precio Gobierno:").pack(pady=(10, 0))
    entry_gob_precio = ctk.CTkEntry(frame_izquierda, placeholder_text="Ingrese el precio del gobierno")
    entry_gob_precio.pack(pady=(0, 10), padx=20, fill="x")

    # Algorithm selection
    ctk.CTkLabel(frame_izquierda, text="Algoritmo:").pack(pady=(10, 0))
    combo_algoritmo = ctk.CTkOptionMenu(frame_izquierda, values=["Fuerza Bruta", "Programación Dinámica", "Voraz"])
    combo_algoritmo.pack(pady=(0, 20), padx=20, fill="x")

    # Calculate button
    btn_calcular = ctk.CTkButton(frame_izquierda, text="Calcular", command=calcular_resultados_subasta, height=40)
    btn_calcular.pack(pady=10, padx=20, fill="x")

    # Add bidder button
    btn_agregar_oferente = ctk.CTkButton(frame_izquierda, text="Agregar Oferente", command=agregar_oferente, height=40)
    btn_agregar_oferente.pack(pady=10, padx=20, fill="x")

    
    # --- Middle Section: Bidders ---
    ctk.CTkLabel(frame_medio, text="Oferentes", font=("Arial", 24, "bold")).pack(pady=30)

    frame_oferentes = ctk.CTkScrollableFrame(frame_medio, width=580, height=650)
    frame_oferentes.pack(fill="both", expand=True, padx=10, pady=10)

    headers = ["Oferente", "Pago por acción", "Mínimo compra", "Máximo compra  "]
    for col, header in enumerate(headers):
        ctk.CTkLabel(frame_oferentes, text=header, font=("Arial", 14, "bold")).grid(row=0, column=col, padx=8, pady=10)

    entry_oferentes = []  # List for dynamic entries

    # --- Right Section: Results ---
    ctk.CTkLabel(frame_derecha, text="Resultados", font=("Arial", 20, "bold")).pack(pady=20)

    resultado_text = tk.StringVar()
    resultado_label = ctk.CTkLabel(frame_derecha, textvariable=resultado_text, wraplength=250, font=("Arial", 12))
    resultado_label.pack(pady=10, fill="x")

    algoritmito = tk.StringVar()
    algoritmo_label = ctk.CTkLabel(frame_derecha, textvariable=algoritmito, font=("Arial", 12))
    algoritmo_label.pack(pady=5, fill="x")

    tiempito = tk.StringVar()
    tiempo_label = ctk.CTkLabel(frame_derecha, textvariable=tiempito, font=("Arial", 12))
    tiempo_label.pack(pady=5, fill="x")

    # Graph button
    btn_grafico = ctk.CTkButton(frame_derecha, text="Mostrar Gráfico", command=dibujar_grafica_subasta, height=40)
    btn_grafico.pack(pady=20, padx=20, fill="x")

    root.mainloop()


# Implementación de la solución por fuerza bruta
def fuerza_bruta(oferentes, A, min_precio):
    # Filtrar oferentes válidos
    oferentes_validos = [
        (precio, min_acciones, max_acciones) 
        for precio, min_acciones, max_acciones in oferentes 
        if precio >= min_precio
    ]
    n = len(oferentes_validos)  # Número de oferentes válidos

    mejor_asignacion = None
    max_valor = 0

    # Función recursiva para generar combinaciones
    def generar_asignaciones(index, acciones_restantes, asignacion_actual):
        nonlocal mejor_asignacion, max_valor

        # Caso base: Se recorrieron todos los oferentes válidos
        if index == n:
            if acciones_restantes == 0:  # Todas las acciones fueron asignadas
                valor_actual = sum(
                    asignacion_actual[i] * oferentes_validos[i][0] 
                    for i in range(n)
                )
                if valor_actual > max_valor:
                    max_valor = valor_actual
                    # Asignar resultados para todos los oferentes (incluyendo inválidos)
                    resultado_final = [0] * len(oferentes)
                    j = 0
                    for i in range(len(oferentes)):
                        if oferentes[i][0] >= min_precio:
                            resultado_final[i] = asignacion_actual[j]
                            j += 1
                    mejor_asignacion = resultado_final
            return

        # Obtener información del oferente actual
        precio, min_acciones, max_acciones = oferentes_validos[index]

        # Probar todas las cantidades posibles de acciones para este oferente
        for x in range(min_acciones, min(max_acciones, acciones_restantes) + 1):
            generar_asignaciones(index + 1, acciones_restantes - x, asignacion_actual + [x])

        # Caso donde no se asignan acciones a este oferente
        generar_asignaciones(index + 1, acciones_restantes, asignacion_actual + [0])

    # Iniciar la generación de asignaciones
    generar_asignaciones(0, A, [])

    return mejor_asignacion, max_valor

def programacion_dinamica(oferentes, A, min_precio):
    # Filtrar oferentes válidos por precio mínimo
    oferentes_validos = [of for of in oferentes if of[0] >= min_precio]
    n = len(oferentes_validos)
    
    # Crear tabla de programación dinámica
    dp = [[float('-inf')] * (A + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    # Matriz para rastrear asignaciones
    asignaciones = [[[] for _ in range(A + 1)] for _ in range(n + 1)]
    
    # Llenar la tabla de programación dinámica
    for i in range(1, n + 1):
        precio, min_acciones, max_acciones = oferentes_validos[i-1]
        
        for j in range(A + 1):
            # No tomar este oferente
            if dp[i-1][j] > dp[i][j]:
                dp[i][j] = dp[i-1][j]
                asignaciones[i][j] = asignaciones[i-1][j].copy()
            
            # Intentar tomar acciones de este oferente
            for x in range(min_acciones, min(max_acciones, j) + 1):
                if j >= x:
                    valor_actual = dp[i-1][j-x] + precio * x
                    
                    if valor_actual > dp[i][j]:
                        dp[i][j] = valor_actual
                        asignaciones[i][j] = asignaciones[i-1][j-x].copy() + [(i-1, x)]
    
    # Buscar la mejor solución que sume exactamente A
    mejor_valor = float('-inf')
    mejor_asignacion = None
    
    if dp[n][A] > float('-inf'):
        mejor_valor = dp[n][A]
        mejor_asignacion = asignaciones[n][A]
    
    # Completar la asignación con ceros para todos los oferentes
    if mejor_asignacion is not None:
        resultado_final = [0] * len(oferentes)
        asignaciones_dict = {idx: x for idx, x in mejor_asignacion}
        
        for i, of in enumerate(oferentes):
            if of[0] >= min_precio and i in asignaciones_dict:
                resultado_final[i] = asignaciones_dict[i]
        
        return resultado_final, mejor_valor
    
    return None, 0

def algoritmo_voraz(oferentes, A, min_precio):
    # Filtrar y ordenar oferentes por precio de mayor a menor
    oferentes_validos = sorted(
        [(precio, min_acciones, max_acciones, idx) for idx, (precio, min_acciones, max_acciones) in enumerate(oferentes) if precio >= min_precio],
        key=lambda x: x[0],
        reverse=True
    )
    
    asignacion = [0] * len(oferentes)
    acciones_restantes = A

    for precio, min_acciones, max_acciones, idx in oferentes_validos:
        # Calcular cuántas acciones puede tomar este oferente
        acciones_comprar = min(
            max_acciones, 
            min(acciones_restantes, max_acciones)
        )
        
        # Ajustar si no cumple el mínimo
        if acciones_comprar < min_acciones and acciones_restantes >= min_acciones:
            acciones_comprar = min(min_acciones, acciones_restantes)
        
        # Asignar acciones a este oferente
        asignacion[idx] = acciones_comprar
        acciones_restantes -= acciones_comprar
        
        # Terminar si ya no hay acciones restantes
        if acciones_restantes == 0:
            break

    # Calcular valor total
    valor_total = sum(
        oferentes[idx][0] * asignacion[idx] for idx in range(len(oferentes))
    )
    
    return asignacion, valor_total

# Función que recoge los datos de la interfaz y ejecuta los algoritmos
def calcular_resultados_subasta():
    oferentes = []
    try:
        total_acciones = int(entry_total_acciones.get())
        precio_minimo = int(entry_precio_minimo.get())

        if total_acciones <= 0 or precio_minimo < 0:
            raise ValueError("El total de acciones debe ser mayor a 0 y el precio mínimo no puede ser negativo.")

        for i in range(len(entry_oferentes)):
            precio = int(entry_oferentes[i][0].get())
            min_acc = int(entry_oferentes[i][1].get())
            max_acc = int(entry_oferentes[i][2].get())

            if min_acc < 0 or max_acc < min_acc:
                raise ValueError(f"Oferente {i + 1}: Valores inválidos. Las acciones mínimas no pueden exceder las máximas.")

            if precio < precio_minimo:
                oferentes.append((0, min_acc, max_acc))  # Ignorar oferente
            else:
                oferentes.append((precio, min_acc, max_acc))

        # Incluir al gobierno como oferente
        precio_gob = int(entry_gob_precio.get())
        oferentes.append((precio_gob, 0, total_acciones))

        # Seleccionar el algoritmo
        algoritmo = combo_algoritmo.get()
        if algoritmo == "Fuerza Bruta":
            start = time.perf_counter()
            asignacion, valor = fuerza_bruta(oferentes, total_acciones, precio_minimo)
            tiempo = time.perf_counter() - start
            promedio_bruta.append(tiempo)         
        elif algoritmo == "Programación Dinámica":
            start = time.perf_counter()
            asignacion, valor = programacion_dinamica(oferentes, total_acciones, precio_minimo)
            tiempo = time.perf_counter() - start
            promedio_dp.append(tiempo)
        else:
            start = time.perf_counter()
            asignacion, valor = algoritmo_voraz(oferentes, total_acciones, precio_minimo)
            tiempo = time.perf_counter() - start
            promedio_greedy.append(tiempo)
            
        # Generar el texto de resultados
        resultado = f"Ganancia total: {valor}\n"
        for idx, asign in enumerate(asignacion[:-1]):  # Último es gobierno
            resultado += f"Oferente {idx + 1}: Compró {asign} acciones\n"
        resultado += f"Gobierno: Compró {asignacion[-1]} acciones\n"  # Gobierno separado

        resultado_text.set(resultado)
        algoritmito.set(f"Algoritmo: {algoritmo}")
        tiempito.set(f"Tiempo de ejecución: {tiempo:.6f} segundos")
        

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Función para agregar oferentes dinámicamente
def agregar_oferente():
    fila = len(entry_oferentes)
    lbl = tk.Label(frame_oferentes, text=f"Oferente {fila + 1}")
    lbl.grid(row=fila+1, column=0)

    entry_precio = tk.Entry(frame_oferentes)
    entry_precio.grid(row=fila+1, column=1)
    entry_min = tk.Entry(frame_oferentes)
    entry_min.grid(row=fila+1, column=2)
    entry_max = tk.Entry(frame_oferentes)
    entry_max.grid(row=fila+1, column=3)

    entry_oferentes.append((entry_precio, entry_min, entry_max))

def dibujar_grafica_subasta(): 
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
        else:
            messagebox.showerror("Error", "No se han realizado cálculos con todos los métodos.")
    except:
        messagebox.showerror("Error", "No se han realizado cálculos aún.")        
if __name__ == "__main__":
    global promedio_bruta, promedio_greedy, promedio_dp
    promedio_bruta = []
    promedio_greedy = []
    promedio_dp = []
    interfaz()