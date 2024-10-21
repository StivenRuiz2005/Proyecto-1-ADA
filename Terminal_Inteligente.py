"""
Autor: Carlos Stiven Ruiz Rojas
Descripcion: Implementación de algoritmos de fuerza bruta, programación dinámica y voraz para el problema de la terminal inteligente.
Fecha: 16/10/2024
"""

import sys

# Ya esta bien
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

# Ya esta bien
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
    pass

a = 1  # advance cost
d = 2  # delete cost
r = 3  # replace cost
i = 2  # insert cost
k = 1  # kill cost

test_cases = [
    ("canción", "canción"),   # Ejemplo 1
    ("correr", "cobrar"),     # Ejemplo 2
    ("perro", "pájaro"),      # Ejemplo 3
    ("bailar", "malabar"),    # Ejemplo 4
    ("ratón", "ratones"),     # Ejemplo 5
    ("algorithm", "altruistic"),  # Ejemplo 6
]
for x,y in test_cases:
    print("Fuerza bruta: ")
    print(brute_force_transform(x, y, a, d, r, i, k))
    #print("DP: ")
    #print(dp_transform(x, y, a, d, r, i, k))
    print("Greedy: ")
    print(greedy_transform(x, y, a, d, r, i, k))
