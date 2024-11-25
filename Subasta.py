import numpy as np

# Implementación de la solución por fuerza bruta
def fuerza_bruta(oferentes, A, min_precio):
    # Filtrar oferentes válidos (aquellos cuyo precio sea >= min_precio)
    oferentes_validos = [of for of in oferentes if of[0] >= min_precio]
    n = len(oferentes_validos)

    mejor_asignacion = None
    max_valor = 0

    # Generar todas las combinaciones posibles
    def backtrack(index, asignacion_actual, acciones_asignadas):
        nonlocal mejor_asignacion, max_valor

        # Si hemos asignado todas las acciones requeridas, calcular el valor
        if acciones_asignadas == A:
            # Calcular el valor para los oferentes válidos
            valor = sum(oferentes_validos[i][0] * asignacion_actual[i] for i in range(n))

            # Si el valor obtenido es mejor que el máximo encontrado, actualizar
            if valor > max_valor:
                # Generar la asignación completa para todos los oferentes
                resultado_final = [0] * len(oferentes)
                j = 0
                for i in range(len(oferentes)):
                    if oferentes[i][0] >= min_precio:
                        resultado_final[i] = asignacion_actual[j]
                        j += 1

                mejor_asignacion = resultado_final
                max_valor = valor
            return

        # Si ya hemos recorrido todos los oferentes válidos sin asignar todas las acciones
        if index == n:
            return

        # Obtener el rango de acciones para el oferente actual
        precio, min_acciones, max_acciones = oferentes_validos[index]

        # Probar todas las cantidades posibles de acciones para este oferente
        for x in range(min_acciones, min(max_acciones, A - acciones_asignadas) + 1):
            nueva_asignacion = asignacion_actual + [x]
            backtrack(index + 1, nueva_asignacion, acciones_asignadas + x)

    # Comenzar el backtracking
    backtrack(0, [], 0)

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

def pruebas():
    # Prueba 1 con costo mínimo de 200
    print("Prueba 1:")
    A1 = 1000
    oferentes1 = [(900, 100, 300), (800, 200, 400), (700, 300, 500), (100, 1, A1)]
    min_precio_accion = 600
    #print("Fuerza Bruta:", fuerza_bruta(oferentes1, A1, min_precio_accion))
    print("Programación Dinámica:", programacion_dinamica(oferentes1, A1, min_precio_accion))
    print("Voraz:", algoritmo_voraz(oferentes1, A1, min_precio_accion))
    print()

    print("Prueba 2:")
    A2 = 2000
    oferentes2 = [(500, 200, 600), (450, 300, 700), (400, 400, 800), (600, 1, A2)]
    min_precio_accion = 300
    # Solución esperada: ([600, 700, 400, 300], 940000)
    #print("Fuerza Bruta:", fuerza_bruta(oferentes2, A2, min_precio_accion))
    print("Programación Dinámica:", programacion_dinamica(oferentes2, A2, min_precio_accion))
    print("Voraz:", algoritmo_voraz(oferentes2, A2, min_precio_accion))
    print()
    
    print("Prueba 3:")
    A3 = 1500
    oferentes3 = [(1000, 100, 400), (900, 200, 500), (800, 300, 600), (700,200,400), (500, 1, A3)]
    min_precio_accion = 500
    # Solución esperada: ([400, 500, 600, 0], 1500000)
    #print("Fuerza Bruta:", fuerza_bruta(oferentes3, A3, min_precio_accion))
    print("Programación Dinámica:", programacion_dinamica(oferentes3, A3, min_precio_accion))
    print("Voraz:", algoritmo_voraz(oferentes3, A3, min_precio_accion))
    print()
    
    print("Prueba 4:")
    A4 = 1000
    oferentes4 = [(500, 100, 300), (450, 400, 800), (400, 500, 700), (300, 1, A4)]
    min_precio_accion = 300
    # Fuerza Bruta/Programación Dinámica: ([300, 400, 300, 0], 800000)
    # Algoritmo Voraz posiblemente: ([300, 400, 100, 200], 760000)
    
    #print("Fuerza Bruta:", fuerza_bruta(oferentes4, A4, min_precio_accion))
    print("Programación Dinámica:", programacion_dinamica(oferentes4, A4, min_precio_accion))
    print("Voraz:", algoritmo_voraz(oferentes4, A4, min_precio_accion))
    print()
    

# Ejecutar las pruebas
pruebas()
