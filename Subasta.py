"""
Autor: Carlos Stiven Ruiz Rojas
Descripcion: Implementación de algoritmos de fuerza bruta, programación dinámica y voraz para el problema de la subasta.
Fecha: 16/10/2024
Ultima modificacion: 21/10/2024
"""

import numpy as np

# Implementación de la solución por fuerza bruta
def fuerza_bruta(oferentes, A):
    n = len(oferentes)
    max_valor = 0
    mejor_asignacion = None

    # Generar todas las combinaciones manualmente (asumiendo que son 3 oferentes)
    for i in range(oferentes[0][1], oferentes[0][2] + 1):
        for j in range(oferentes[1][1], oferentes[1][2] + 1):
            for k in range(oferentes[2][1], oferentes[2][2] + 1):
                asignacion = (i, j, k)
                
                if sum(asignacion) == A:  # Verificamos si la suma de asignaciones es A
                    valor = sum(p * x for (p, m, M), x in zip(oferentes, asignacion))
                    if valor > max_valor:
                        max_valor = valor
                        mejor_asignacion = asignacion

    return mejor_asignacion, max_valor


def programacion_dinamica(oferentes, A):
    
    n = len(oferentes)
    dp = np.zeros((n + 1, A + 1), dtype=int)
    seleccion = np.zeros((n + 1, A + 1), dtype=int)
    
    for i in range(1, n + 1):
        precio, min_acc, max_acc = oferentes[i - 1]
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

    return asignacion.tolist(), int(dp[n, A])


def voraz(oferentes, A):
    
    n = len(oferentes)
    asignacion = [0] * n
    valor_total = 0
    acciones_restantes = A

    while acciones_restantes > 0:
        max_precio = -1
        max_index = -1
        
        for i in range(n):
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
        else:
            asignacion[max_index] = 0 

    return asignacion, valor_total


def pruebas():
    # Prueba 1
    print("Prueba 1:")
    oferentes1 = [(500, 100, 600), (450, 400, 800), (100, 0, 1000)]
    A1 = 1000
    #print("Fuerza Bruta:", fuerza_bruta(oferentes1, A1))
    print("Programación Dinámica:", programacion_dinamica(oferentes1, A1))
    print("Voraz:", voraz(oferentes1, A1))
    #print()

    """
    # Prueba 2
    print("Prueba 2:")
    oferentes2 = [(600, 200, 700), (500, 100, 500), (300, 100, 400), (100, 0, 1200)]
    A2 = 1200
    #print("Fuerza Bruta:", fuerza_bruta(oferentes2, A2))
    print("Programación Dinámica:", programacion_dinamica(oferentes2, A2))
    print("Voraz:", voraz(oferentes2, A2))
    print()

    # Prueba 3
    print("Prueba 3:")
    oferentes3 = [(600, 100, 500), (450, 100, 400), (400, 100, 300), (100, 0, 1000)]
    A3 = 1000
    #print("Fuerza Bruta:", fuerza_bruta(oferentes3, A3))
    print("Programación Dinámica:", programacion_dinamica(oferentes3, A3))
    print("Voraz:", voraz(oferentes3, A3))
    print()

    # Prueba 4
    print("Prueba 4:")
    oferentes4 = [(700, 200, 600), (650, 100, 400), (500, 100, 800), (100, 0, 1500)]
    A4 = 1500
    #print("Fuerza Bruta:", fuerza_bruta(oferentes4, A4))
    print("Programación Dinámica:", programacion_dinamica(oferentes4, A4))
    print("Voraz:", voraz(oferentes4, A4))
    print()

    # Prueba 5
    print("Prueba 5 (Caso donde el Greedy no da solución óptima):")
    oferentes5 = [(500, 200, 500), (450, 100, 400), (1000, 300, 600), (100, 0, 1000)]
    A5 = 1000
    #print("Fuerza Bruta:", fuerza_bruta(oferentes5, A5))
    print("Programación Dinámica:", programacion_dinamica(oferentes5, A5))
    print("Voraz:", voraz(oferentes5, A5))
    print()
    
    # Prueba 6
    print("Prueba 6:")
    oferentes6 = [(600, 400, 700), (500, 300, 400), (400, 100, 300), (100, 0, 1000)]
    A6 = 1000
    print("Fuerza Bruta:", fuerza_bruta(oferentes6, A6))
    """
# Ejecutar las pruebas
pruebas()
