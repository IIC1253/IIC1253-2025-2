from z3 import *

# Variables proposicionales x_i_j_k:
# en la casilla de la fila i y la columna j esta el numero k
# i,j,k estan en el rango 0 a 3. (para que calce con la indexacion de python)

x = [
    [
        [Bool(f"x_{i}_{j}_{k}") for k in range(4)]
        for j in range(4)
    ]
    for i in range(4)
]

# Creamos el solver

solver = Solver()

# Agregamos las formulas al solver

# A cada casilla se le asigna al menos un numero

for i in range(4):
  for j in range(4):
    solver.add((x[i][j][0] | x[i][j][1] | x[i][j][2] | x[i][j][3]))

# No se le puede asignar a una casilla mas de un numero
for i in range(4):
  for j in range(4):
    for k1 in range(4):
      for k2 in range(k1+1,4):
        solver.add(
            ~(x[i][j][k1] & x[i][j][k2])
            )

# En cada fila, los numeros son distintos
for i in range(4):
  for j1 in range(4):
    for j2 in range(j1+1,4):
      for k in range(4):
        solver.add(
            ~(x[i][j1][k] & x[i][j2][k])
            )

# En cada columna, los numeros son distintos
for j in range(4):
  for i1 in range(4):
    for i2 in range(i1+1,4):
      for k in range(4):
        solver.add(
            ~(x[i1][j][k] & x[i2][j][k])
            )

# Agregamos las casillas ocupadas: [1,1,2], [2,3,1], [3,2,4], [3,4,3], [4,1,3]
# Hay que restarle 1 a los numeros para que calce con la indexacion
solver.add(
    x[0][0][1],
    x[1][2][0],
    x[2][1][3],
    x[2][3][2],
    x[3][0][2]
)

# Ejecutamos el solver y verificamos satisfacibilidad
if solver.check() == sat:
    solucion = solver.model()
    print("Variables verdaderas:\n")
    for v in solucion:
      if solucion[v] == True:
        print(v)

    print("\nSolucion obtenida ajustada a la indexacion original (1 a 4):\n")

    for i in range(4):
      fila = []
      for j in range(4):
        for k in range(4):
          if solucion[x[i][j][k]] == True:
            fila.append(k+1)
      print(fila)

else:
    print("No hay solucion para el tablero")