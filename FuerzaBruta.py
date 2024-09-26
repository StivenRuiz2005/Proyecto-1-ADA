def transform_cost(x, y, costs):
    n = len(x)
    m = len(y)
    
    # Crear matriz de costos
    M = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    
    # Inicialización
    for i in range(1, n + 1):
        M[i][0] = i * costs['delete']
    for j in range(1, m + 1):
        M[0][j] = j * costs['insert']

    # Rellenar la matriz M
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                M[i][j] = M[i - 1][j - 1]
            else:
                M[i][j] = min(
                    M[i - 1][j - 1] + costs['replace'],  # Reemplazar
                    M[i - 1][j] + costs['delete'],       # Borrar
                    M[i][j - 1] + costs['insert']        # Insertar
                )
    
    return M[n][m]

# Ejemplo de uso
costs = {'advance': 1, 'delete': 2, 'replace': 3, 'insert': 2, 'kill': 1}
x = "ingenioso"
y = "ingeniero"
print(transform_cost(x, y, costs))
