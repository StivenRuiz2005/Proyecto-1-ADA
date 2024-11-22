import numpy as np

# Implementación de la solución por fuerza bruta
def fuerza_bruta(oferentes, A, min_precio_accion):
    n = len(oferentes)
    max_valor = 0
    mejor_asignacion = None

    # Generar todas las combinaciones manualmente (asumiendo que son 3 oferentes)
    for i in range(oferentes[0][1], oferentes[0][2] + 1):
        for j in range(oferentes[1][1], oferentes[1][2] + 1):
            for k in range(oferentes[2][1], oferentes[2][2] + 1):
                asignacion = (i, j, k)
                
                # Filtrar ofertas que no cumplen con el precio mínimo
                if oferentes[0][0] < min_precio_accion or oferentes[1][0] < min_precio_accion or oferentes[2][0] < min_precio_accion:
                    continue
                
                if sum(asignacion) == A:  # Verificamos si la suma de asignaciones es A
                    valor = 0
                    for idx, x in enumerate(asignacion):
                        p = oferentes[idx][0]
                        valor += p * x
                    
                    if valor > max_valor:
                        max_valor = valor
                        mejor_asignacion = asignacion

    return mejor_asignacion, max_valor


def programacion_dinamica(oferentes, A, min_precio_accion):
    n = len(oferentes)
    dp = np.zeros((n + 1, A + 1), dtype=int)
    seleccion = np.zeros((n + 1, A + 1), dtype=int)
    
    for i in range(1, n + 1):
        precio, min_acc, max_acc = oferentes[i - 1]

        # Filtrar oferentes cuyo precio es menor al mínimo aceptado
        if precio < min_precio_accion:
            continue

        for acciones_restantes in range(A + 1):
            dp[i, acciones_restantes] = dp[i - 1, acciones_restantes]  # No asignar acciones a este oferente
            seleccion[i, acciones_restantes] = 0  # No asignar acciones a este oferente

            for x in range(min_acc, min(max_acc, acciones_restantes) + 1):
                valor = dp[i - 1, acciones_restantes - x] + x * precio
                if valor > dp[i, acciones_restantes]:
                    dp[i, acciones_restantes] = valor
                    seleccion[i, acciones_restantes] = x

    acciones_restantes = A
    asignacion = np.zeros(n, dtype=int)
    for i in range(n, 0, -1):
        asignacion[i - 1] = seleccion[i, acciones_restantes]
        acciones_restantes -= seleccion[i, acciones_restantes]

    return asignacion.tolist(), dp


def voraz(oferentes, A, min_precio_accion):
    n = len(oferentes)
    asignacion = [0] * n
    valor_total = 0
    acciones_restantes = A

    while acciones_restantes > 0:
        max_precio = -1
        max_index = -1
        
        for i in range(n):
            precio, min_acc, max_acc = oferentes[i]
            if asignacion[i] == 0 and precio > max_precio and precio >= min_precio_accion: 
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
        else:
            asignacion[max_index] = 0 

    return asignacion, valor_total


def pruebas():
    # Prueba 1 con costo mínimo de 200
    print("Prueba 1:")
    A1 = 1000
    oferentes1 = [(900, 100, 300), (800, 200, 400), (700, 300, 500), (100, 1, A1)]
    min_precio_accion = 600
    #print("Fuerza Bruta:", fuerza_bruta(oferentes1, A1, min_precio_accion))
    print("Programación Dinámica:", programacion_dinamica(oferentes1, A1, min_precio_accion))
    print("Voraz:", voraz(oferentes1, A1, min_precio_accion))
    print()

    """
    # Otras pruebas (descomentar si es necesario)
    oferentes2 = [(600, 200, 700), (500, 100, 500), (300, 100, 400), (100, 0, 1200)]
    A2 = 1200
    min_precio_accion = 300
    print("Programación Dinámica:", programacion_dinamica(oferentes2, A2, min_precio_accion))
    print("Voraz:", voraz(oferentes2, A2, min_precio_accion))
    """

# Ejecutar las pruebas
pruebas()
