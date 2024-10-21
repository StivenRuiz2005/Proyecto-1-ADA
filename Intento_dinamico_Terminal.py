import numpy as np

"""
Nombre : Carlos Stiven Ruiz Rojas
Descripcion: Archivo de prueba para el algoritmo dinamico de la terminal
Fecha: 21 / 10 / 2024
Ultima modificacion: 21 / 10 / 2024
"""

def levenshtein_custom(source, target, a, d, r, i, k):
    n = len(source)
    m = len(target)
    dp = np.zeros((n + 1, m + 1))

    # Inicializar la primera columna (coste de eliminar todos los caracteres de source)
    for x in range(1, n + 1):
        dp[x][0] = x * d

    # Inicializar la primera fila (coste de insertar caracteres en target)
    for y in range(1, m + 1):
        dp[0][y] = y * i

    # Llenar la tabla DP considerando todas las operaciones
    for x in range(1, n + 1):
        for y in range(1, m + 1):
            if source[x - 1] == target[y - 1]:
                dp[x, y] = dp[x - 1, y - 1] + a
            else:
                replace_cost = dp[x - 1, y - 1] + r
                delete_cost = dp[x - 1, y - 1] + d   
                insert_cost = dp[x - 1, y - 1] + i
                
                dp[x, y] = min(replace_cost, delete_cost, insert_cost)
            
            # Evaluar movimiento avanzado solamente si es igual
            if x > 1 and y > 1 and source[x - 1] == target[y - 1]:
                dp[x, y] = min(dp[x, y], dp[x - 1, y - 1] + a)

        # Evaluar operación kill
        dp[x, m] = min(dp[x, m], dp[x - 1, m] + k)

    # Evaluar operación kill desde el final
    for y in range(1, m + 1):
        dp[n, y] = min(dp[n, y], dp[n, y - 1] + k)

    # Imprimir la matriz DP para depuración
    print(f"Matriz DP:\n{dp}")

    return dp[n, m]

# Ejemplo de uso:
source = "algorithm"
target = "altruistic"
cost_advance = 1
cost_delete = 2
cost_replace = 3
cost_insert = 2
cost_kill = 1

distancia = levenshtein_custom(source, target, cost_advance, cost_delete, cost_replace, cost_insert, cost_kill)

print(f"La distancia personalizada entre '{source}' y '{target}' es: {distancia}")
