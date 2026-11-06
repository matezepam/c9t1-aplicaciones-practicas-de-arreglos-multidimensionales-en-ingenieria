# PROBLEMA 5
# Cada fila de la matriz contiene las coordenadas x e y de un punto y la matriz
# de transformación define una rotación respecto al origen, usando un ángulo
# positivo para el sentido contrario a las agujas del reloj y mostrando ambos
# conjuntos sobre los mismos ejes para conservar una referencia común.

from math import cos, sin, radians
from APOYO import dimensiones_matriz, mostrar_matriz, graficar_puntos


def crear_matriz_rotacion(angulo_grados):
    # Convierto los grados a radianes porque seno y coseno reciben esa unidad,
    # manteniendo la entrada en grados para facilitar la elección de la rotación.
    angulo = radians(angulo_grados)
    return [[cos(angulo), -sin(angulo)],
            [sin(angulo), cos(angulo)]]


# La matriz se aplica a las dos coordenadas de cada punto para formar una nueva
# fila sin modificar la original, separando el cálculo de la presentación para
# reutilizarlo con otra rotación o una matriz de escalado de dos por dos.
def transformar_puntos(puntos, transformacion):
    if dimensiones_matriz(transformacion) != (2, 2):
        raise ValueError('La transformación debe ser una matriz de dos por dos.')
    if not puntos:
        return []
    if dimensiones_matriz(puntos)[1] != 2:
        raise ValueError('Cada punto debe tener coordenadas x e y.')
    resultado = []
    for punto in puntos:
        nuevo_punto = []
        # Cada fila de la transformación produce una coordenada de salida
        # al sumar sus productos con x e y, por eso recorro ambas columnas.
        for fila in range(2):
            coordenada = 0.0
            for columna in range(2):
                coordenada += transformacion[fila][columna] * punto[columna]
            nuevo_punto.append(coordenada)
        resultado.append(nuevo_punto)
    return resultado


def demostracion():
    puntos = [[1, 1], [3, 1], [3, 2], [1, 2], [2, 3]]
    transformacion = crear_matriz_rotacion(90)
    resultado = transformar_puntos(puntos, transformacion)
    print('MATRIZ DE ROTACIÓN DE 90 GRADOS')
    mostrar_matriz(transformacion)
    print('\nPUNTOS ANTES Y DESPUÉS')
    for indice in range(len(puntos)):
        print(f'P{indice + 1} ({puntos[indice][0]:.2f}, {puntos[indice][1]:.2f}) '
              f'-> ({resultado[indice][0]:.2f}, {resultado[indice][1]:.2f})')
    ruta = graficar_puntos(puntos, resultado, 'ROTACION.png', 'Rotación de 90 grados')
    print(f'\nGráfica guardada en {ruta}')


if __name__ == '__main__':
    demostracion()
