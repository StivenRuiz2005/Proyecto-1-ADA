import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np

# Implementación de la solución por fuerza bruta
def fuerza_bruta(oferentes, A):
    n = len(oferentes)
    max_valor = 0
    mejor_asignacion = None

    # Generar combinaciones de asignaciones para cada oferente
    rangos = [range(oferente[1], oferente[2] + 1) for oferente in oferentes]

    # Función recursiva para generar combinaciones
    def generar_asignaciones(asignacion_actual, nivel, acciones_asignadas):
        nonlocal max_valor, mejor_asignacion

        # Si hemos asignado más acciones de las permitidas, volvemos
        if acciones_asignadas > A:
            return

        # Si hemos llegado al último nivel, verificamos si esta combinación es válida
        if nivel == n:
            if acciones_asignadas == A:  # Verificamos si la suma de asignaciones es A
                valor = 0
                for i in range(n):
                    p = oferentes[i][0]
                    x = asignacion_actual[i]
                    valor += p * x

                if valor > max_valor:
                    max_valor = valor
                    mejor_asignacion = list(asignacion_actual)
            return

        # Probar todas las asignaciones posibles para el oferente actual
        for x in rangos[nivel]:
            asignacion_actual[nivel] = x
            generar_asignaciones(asignacion_actual, nivel + 1, acciones_asignadas + x)

    # Inicializar asignación actual y llamar a la función recursiva
    asignacion_actual = [0] * n
    generar_asignaciones(asignacion_actual, 0, 0)  # Nivel inicial y acciones asignadas = 0

    return mejor_asignacion, max_valor


import numpy as np

def programacion_dinamica(oferentes, A):
    n = len(oferentes)
    dp = np.full((n + 1, A + 1), -np.inf)  # Inicializamos la matriz con -inf para evitar valores incorrectos
    seleccion = np.zeros((n + 1, A + 1), dtype=int)

    # Caso base: 0 acciones restantes implica 0 valor, sin importar el oferente
    dp[0, :] = 0

    # Llenado de la matriz dp
    for i in range(1, n + 1):
        precio, min_acc, max_acc = oferentes[i - 1]
        for acciones_restantes in range(A + 1):
            # Caso donde no asignamos acciones al oferente actual
            dp[i, acciones_restantes] = dp[i - 1, acciones_restantes]
            seleccion[i, acciones_restantes] = 0

            # Caso donde asignamos acciones al oferente actual
            for x in range(min_acc, min(max_acc, acciones_restantes) + 1):
                # Si es posible asignar 'x' acciones a este oferente
                if acciones_restantes - x >= 0:
                    valor = dp[i - 1, acciones_restantes - x] + x * precio
                    if valor > dp[i, acciones_restantes]:
                        dp[i, acciones_restantes] = valor
                        seleccion[i, acciones_restantes] = x

    # Reconstrucción de la solución óptima
    acciones_restantes = A
    asignacion = np.zeros(n, dtype=int)
    for i in range(n, 0, -1):
        asignacion[i - 1] = seleccion[i, acciones_restantes]
        acciones_restantes -= seleccion[i, acciones_restantes]

    # Si dp[n, A] sigue siendo -inf, no hay solución válida
    if dp[n, A] == -np.inf:
        return None, 0  # No hay asignación posible

    return asignacion.tolist(), int(dp[n, A])

# Implementación de la solución voraz - Esta bien implementada
def voraz(oferentes, A):
    n = len(oferentes)
    asignacion = [0] * n
    valor_total = 0
    acciones_restantes = A

    while acciones_restantes > 0:
        max_precio = -1
        max_index = -1

        for i in range(n):
            if oferentes[i][0] is None:
                continue
            precio, min_acc, max_acc = oferentes[i]
            if asignacion[i] == 0 and precio > max_precio:
                max_precio = precio
                max_index = i

        if max_index == -1:
            break

        precio, min_acc, max_acc = oferentes[max_index]
        asignar = min(max_acc, acciones_restantes)

        if asignar >= min_acc:
            asignacion[max_index] = asignar
            valor_total += asignar * precio
            acciones_restantes -= asignar

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
            asignacion, valor = fuerza_bruta(oferentes, total_acciones)
        elif algoritmo == "Programación Dinámica":
            asignacion, valor = programacion_dinamica(oferentes, total_acciones)
        else:  # Voraz
            asignacion, valor = voraz(oferentes, total_acciones)

        # Generar el texto de resultados
        resultado = f"Ganancia total: {valor}\n"
        for idx, asign in enumerate(asignacion[:-1]):  # Último es gobierno
            resultado += f"Oferente {idx + 1}: Compró {asign} acciones\n"
        resultado += f"Gobierno: Compró {asignacion[-1]} acciones\n"  # Gobierno separado

        resultado_text.set(resultado)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Función para agregar oferentes dinámicamente
def agregar_oferente():
    fila = len(entry_oferentes)
    lbl = tk.Label(frame_oferentes, text=f"Oferente {fila + 1}")
    lbl.grid(row=fila, column=0)

    entry_precio = tk.Entry(frame_oferentes)
    entry_precio.grid(row=fila, column=1)
    entry_min = tk.Entry(frame_oferentes)
    entry_min.grid(row=fila, column=2)
    entry_max = tk.Entry(frame_oferentes)
    entry_max.grid(row=fila, column=3)

    entry_oferentes.append((entry_precio, entry_min, entry_max))

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Asignación de Acciones")

frame_oferentes = tk.Frame(root)
frame_oferentes.pack(pady=10)

# Entradas para los oferentes
entry_oferentes = []

tk.Label(frame_oferentes, text="Oferente").grid(row=0, column=0)
tk.Label(frame_oferentes, text="Pago por acción").grid(row=0, column=1)
tk.Label(frame_oferentes, text="Mínimo a comprar").grid(row=0, column=2)
tk.Label(frame_oferentes, text="Máximo a comprar").grid(row=0, column=3)

# Botón para agregar oferentes
btn_agregar_oferente = tk.Button(root, text="Agregar Oferente", command=agregar_oferente)
btn_agregar_oferente.pack()

# Entrada para el total de acciones
frame_acciones = tk.Frame(root)
frame_acciones.pack(pady=10)

tk.Label(frame_acciones, text="Total de acciones:").grid(row=0, column=0)
entry_total_acciones = tk.Entry(frame_acciones)
entry_total_acciones.grid(row=0, column=1)

# Entrada para el precio mínimo por acción
frame_precio_minimo = tk.Frame(root)
frame_precio_minimo.pack(pady=10)

tk.Label(frame_precio_minimo, text="Precio mínimo por acción:").grid(row=0, column=0)
entry_precio_minimo = tk.Entry(frame_precio_minimo)
entry_precio_minimo.grid(row=0, column=1)

# Entrada para el precio del gobierno
frame_gobierno = tk.Frame(root)
frame_gobierno.pack(pady=10)

tk.Label(frame_gobierno, text="Precio por acción (Gobierno):").grid(row=0, column=0)
entry_gob_precio = tk.Entry(frame_gobierno)
entry_gob_precio.grid(row=0, column=1)

# Selección del algoritmo
frame_algoritmo = tk.Frame(root)
frame_algoritmo.pack(pady=10)

tk.Label(frame_algoritmo, text="Seleccione el algoritmo:").grid(row=0, column=0)
combo_algoritmo = ttk.Combobox(frame_algoritmo, values=["Fuerza Bruta", "Programación Dinámica", "Voraz"])
combo_algoritmo.grid(row=0, column=1)
combo_algoritmo.current(0)

# Botón para calcular resultados
btn_calcular = tk.Button(root, text="Calcular", command=calcular_resultados)
btn_calcular.pack(pady=10)

# Campo de texto para mostrar resultados
resultado_text = tk.StringVar()
resultado_label = tk.Label(root, textvariable=resultado_text)
resultado_label.pack(pady=10)

root.mainloop()
