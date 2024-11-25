import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import time

"""
Descripcion: Implementación de algoritmos de fuerza bruta, programación dinámica y voraz para el problema de la subasta publica con interfaz.
Fecha: 21 / 10 / 2024
Ultima modificacion: 25 / 11 / 2024

"""

def interfaz():
    global entry_total_acciones, entry_precio_minimo, entry_gob_precio, combo_algoritmo, resultado_text, entry_oferentes, frame_oferentes, frame_acciones, frame_precio_minimo, frame_gobierno, frame_algoritmo,algoritmito,tiempito
    root = tk.Tk()
    root.title("Asignación de Acciones")
    root.geometry("800x400")  # Tamaño inicial de la ventana
    root.resizable(False, False)  # Evitar que se pueda cambiar el tamaño de la ventana

    # Frames principales
    frame_izquierda = tk.Frame(root, width=200, bg="#f0f0f0")
    frame_izquierda.pack(side="left", fill="y")

    frame_medio = tk.Frame(root, width=200, bg="#ffffff")
    frame_medio.pack(side="left", fill="both", expand=False)

    frame_derecha = tk.Frame(root, width=150, bg="#f0f0f0")
    frame_derecha.pack(fill="y")

    # --- Sección izquierda: Entradas y controles ---
    tk.Label(frame_izquierda, text="Configuración", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)

    # Entradas para el total de acciones
    frame_acciones = tk.Frame(frame_izquierda, bg="#f0f0f0")
    frame_acciones.pack(pady=10, fill="x")

    tk.Label(frame_acciones, text="Total de acciones:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
    entry_total_acciones = tk.Entry(frame_acciones, width=10)
    entry_total_acciones.grid(row=0, column=1)

    # Entrada para el precio mínimo por acción
    frame_precio_minimo = tk.Frame(frame_izquierda, bg="#f0f0f0")
    frame_precio_minimo.pack(pady=10, fill="x")

    tk.Label(frame_precio_minimo, text="Precio mínimo:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
    entry_precio_minimo = tk.Entry(frame_precio_minimo, width=10)
    entry_precio_minimo.grid(row=0, column=1)

    # Entrada para el precio del gobierno
    frame_gobierno = tk.Frame(frame_izquierda, bg="#f0f0f0")
    frame_gobierno.pack(pady=10, fill="x")

    tk.Label(frame_gobierno, text="Precio Gobierno:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
    entry_gob_precio = tk.Entry(frame_gobierno, width=10)
    entry_gob_precio.grid(row=0, column=1)

    # Selección del algoritmo
    frame_algoritmo = tk.Frame(frame_izquierda, bg="#f0f0f0")
    frame_algoritmo.pack(pady=10, fill="x")

    tk.Label(frame_algoritmo, text="Algoritmo:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
    combo_algoritmo = ttk.Combobox(frame_algoritmo, values=["Fuerza Bruta", "Programación Dinámica", "Voraz"], width=15)
    combo_algoritmo.grid(row=0, column=1)
    combo_algoritmo.current(0)

    # Botón para calcular resultados
    btn_calcular = tk.Button(frame_izquierda, text="Calcular", command=calcular_resultados)
    btn_calcular.pack(pady=20)

    # Botón para agregar oferente
    btn_agregar_oferente = tk.Button(frame_izquierda, text="Agregar Oferente", command=agregar_oferente)
    btn_agregar_oferente.pack(pady=10)

    # --- Sección medio: Oferentes ---
    tk.Label(frame_medio, text="Oferentes", bg="#ffffff", font=("Arial", 12, "bold")).pack(pady=6)
    

    frame_oferentes = tk.Frame(frame_medio, bg="#ffffff")
    frame_oferentes.pack(fill="both", expand=True)

    tk.Label(frame_oferentes, text="Oferente").grid(row=0, column=0)
    tk.Label(frame_oferentes, text="Pago por acción").grid(row=0, column=1)
    tk.Label(frame_oferentes, text="Mínimo a comprar").grid(row=0, column=2)
    tk.Label(frame_oferentes, text="Máximo a comprar").grid(row=0, column=3)

    entry_oferentes = []  # Lista para las entradas dinámicas

    # --- Sección derecha: Resultados ---
    tk.Label(frame_derecha, text="Resultados", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)

    resultado_text = tk.StringVar()
    resultado_label = tk.Label(frame_derecha, textvariable=resultado_text, bg="#f0f0f0", justify="center")
    resultado_label.pack(pady=10, fill="x")

    # Mostrar algoritmo seleccionado
    algoritmito = tk.StringVar()
    algoritmo_label = tk.Label(frame_derecha, textvariable=algoritmito, bg="#f0f0f0", justify="center")
    algoritmo_label.pack(pady=5, fill="x")

    #mostrar tiempo
    tiempito = tk.StringVar()
    tiempo_label = tk.Label(frame_derecha, textvariable=tiempito, bg="#f0f0f0", justify="center")
    tiempo_label.pack(pady=5, fill="x")
    # Botón para mostrar gráfico
    btn_grafico = tk.Button(frame_derecha, text="Mostrar Gráfico", command=dibujar_grafica)
    btn_grafico.pack(pady=20)

    # Ejecutar la interfaz
    root.mainloop()

# Implementación de la solución por fuerza bruta
def fuerza_bruta(oferentes, A):
    n = len(oferentes)
    max_valor = 0
    mejor_asignacion = None

    def generar_asignaciones(asignacion_actual, nivel, acciones_asignadas):
        nonlocal max_valor, mejor_asignacion

        # Verificar límites de asignación
        if acciones_asignadas > A:
            return

        if nivel == n:
            # Verificar suma total y límites mínimos
            if acciones_asignadas == A and all(
                oferentes[i][1] <= asignacion_actual[i] <= oferentes[i][2] 
                for i in range(n)
            ):
                valor = sum(oferentes[i][0] * asignacion_actual[i] for i in range(n))
                
                if valor > max_valor:
                    max_valor = valor
                    mejor_asignacion = list(asignacion_actual)
            return

        # Generar asignaciones considerando límites
        for x in range(oferentes[nivel][1], oferentes[nivel][2] + 1):
            asignacion_actual[nivel] = x
            generar_asignaciones(asignacion_actual, nivel + 1, acciones_asignadas + x)

    asignacion_actual = [0] * n
    generar_asignaciones(asignacion_actual, 0, 0)

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
        [of for of in oferentes if of[0] >= min_precio], 
        key=lambda x: x[0], 
        reverse=True
    )
    
    asignacion = [0] * len(oferentes)
    acciones_restantes = A
    
    for i, (precio, min_acciones, max_acciones) in enumerate(oferentes_validos):
        # Calcular cuántas acciones puede comprar este oferente
        acciones_comprar = min(
            max_acciones, 
            min(acciones_restantes, max_acciones)
        )
        
        # Ajustar si no cumple el mínimo
        if acciones_comprar < min_acciones and acciones_restantes >= min_acciones:
            acciones_comprar = min(min_acciones, acciones_restantes)
        
        # Actualizar asignación y acciones restantes
        for j, of in enumerate(oferentes):
            if of[0] == precio:
                asignacion[j] = acciones_comprar
                break
        
        acciones_restantes -= acciones_comprar
        
        # Terminar si ya no hay acciones
        if acciones_restantes == 0:
            break
    
    # Calcular valor total
    valor_total = sum(
        of[0] * asig for of, asig in zip(oferentes, asignacion)
    )
    
    return asignacion, valor_total

# Función que recoge los datos de la interfaz y ejecuta los algoritmos
def calcular_resultados():
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
            asignacion, valor = [0], 0 
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

def dibujar_grafica(): 
    try:
        if promedio_bruta.__len__()  == 0 and promedio_greedy.__len__() == 0 and promedio_dp.__len__() == 0:
            messagebox.showerror("Error", "No se han realizado cálculos aún.")
            return
        if promedio_greedy.__len__() == promedio_bruta.__len__() and promedio_dp.__len__() == promedio_bruta.__len__():
            n = promedio_bruta.__len__()
            tamanos = [2**i for i in range(1, n+1)]
            plt.title("Comparación de tiempos de ejecución por método")
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