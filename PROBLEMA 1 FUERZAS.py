# PROBLEMA 1
# La matriz representa fuerzas verticales en nueve nodos de una placa rígida,
# con filas y columnas separadas por una distancia conocida y tres apoyos que
# permiten calcular las reacciones mediante equilibrio de fuerzas y momentos.
# Como el enunciado no fija apoyos, tomé A en [0][0], B en [0][2] y C en [2][0],
# considerando las cargas positivas hacia abajo y las reacciones positivas hacia arriba.

from APOYO import dimensiones_matriz, mostrar_matriz


# Acumulo las fuerzas y sus momentos en un recorrido para calcular las tres
# reacciones con las ecuaciones de equilibrio y conservar la matriz de cargas.
def calcular_reacciones(fuerzas, separacion=1.0):
    if dimensiones_matriz(fuerzas) != (3, 3):
        raise ValueError('La estructura de este ejercicio debe tener tres filas y tres columnas.')
    if separacion <= 0:
        raise ValueError('La separación entre nodos debe ser positiva.')
    total = 0.0
    momento_x = 0.0
    momento_y = 0.0
    for fila in range(3):
        for columna in range(3):
            fuerza = fuerzas[fila][columna]
            total += fuerza
            momento_x += fuerza * fila * separacion
            momento_y += fuerza * columna * separacion
    # Divido el momento entre la distancia al apoyo para obtener su reacción,
    # dejando la de A como la fuerza restante que equilibra las cargas verticales.
    distancia_apoyos = 2 * separacion
    reaccion_b = momento_y / distancia_apoyos
    reaccion_c = momento_x / distancia_apoyos
    reaccion_a = total - reaccion_b - reaccion_c
    # Si alguna reacción resulta negativa, ese apoyo necesitaría un anclaje
    # que ejerza fuerza hacia abajo para mantener el equilibrio de esta placa.
    # Cada fila se crea por separado para que modificar una reacción no cambie
    # otra posición por compartir accidentalmente la misma lista.
    reacciones = []
    for fila in range(3):
        reacciones.append([0.0, 0.0, 0.0])
    reacciones[0][0] = reaccion_a
    reacciones[0][2] = reaccion_b
    reacciones[2][0] = reaccion_c
    return reacciones


# Los residuos deben ser cero o cercanos a cero y permiten comprobar las leyes
# de la estática sobre el resultado, usando x para columnas e y para filas.
def comprobar_equilibrio(fuerzas, reacciones, separacion=1.0):
    residuo_fuerzas = 0.0
    residuo_momento_x = 0.0
    residuo_momento_y = 0.0
    for fila in range(3):
        for columna in range(3):
            diferencia = reacciones[fila][columna] - fuerzas[fila][columna]
            residuo_fuerzas += diferencia
            residuo_momento_x += diferencia * fila * separacion
            residuo_momento_y -= diferencia * columna * separacion
    return residuo_fuerzas, residuo_momento_x, residuo_momento_y


def demostracion():
    fuerzas = [[100, 120, 80],
               [90, 100, 70],
               [60, 50, 40]]
    reacciones = calcular_reacciones(fuerzas)
    print('FUERZAS APLICADAS EN N')
    mostrar_matriz(fuerzas)
    print('\nREACCIONES EN LOS APOYOS EN N')
    mostrar_matriz(reacciones)
    fuerza, momento_x, momento_y = comprobar_equilibrio(fuerzas, reacciones)
    print(f'Equilibrio de fuerzas {fuerza:.6f} N')
    print(f'Equilibrio de momentos X {momento_x:.6f} N·m')
    print(f'Equilibrio de momentos Y {momento_y:.6f} N·m')
    print('Apoyos A [0][0], B [0][2] y C [2][0], con separación de 1 m entre nodos.')


if __name__ == '__main__':
    demostracion()
