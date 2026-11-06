# PROBLEMA 3
# El volumen contiene tres imágenes de ejemplo con intensidades de gris entre
# cero y 255, donde las capas representan profundidades diferentes y los valores
# aislados simulan ruido para comparar el resultado de un promedio por capa.
# Los datos son sintéticos y el suavizado no constituye una evaluación médica.

from APOYO import dimensiones_volumen, mostrar_matriz, graficar_capas


# En los bordes se utilizan sólo vecinos existentes para no introducir ceros que
# oscurezcan artificialmente la imagen y dividir siempre por los datos incluidos.
def promedio_vecinos(imagen, fila, columna):
    total = 0.0
    cantidad = 0
    # Los desplazamientos de menos uno a uno cubren la ventana de tres por tres
    # sin copiar sus valores a otra lista cada vez que se procesa un píxel.
    for df in range(-1, 2):
        for dc in range(-1, 2):
            f, c = fila + df, columna + dc
            if 0 <= f < len(imagen) and 0 <= c < len(imagen[0]):
                total += imagen[f][c]
                cantidad += 1
    # Divido por los vecinos que realmente se incluyeron para tratar también
    # las esquinas y los bordes con el mismo cálculo del promedio.
    return total / cantidad


# La salida se construye con capas y filas nuevas para que cada promedio utilice
# la imagen original y no un vecino que ya fue modificado dentro del recorrido.
def suavizar_volumen(volumen):
    capas, filas, columnas = dimensiones_volumen(volumen)
    resultado = []
    # Proceso cada profundidad por separado para suavizar sus variaciones
    # usando únicamente vecinos de la misma imagen y conservar las capas.
    for capa in range(capas):
        nueva_capa = []
        for fila in range(filas):
            nueva_fila = []
            for columna in range(columnas):
                nueva_fila.append(promedio_vecinos(volumen[capa], fila, columna))
            nueva_capa.append(nueva_fila)
        resultado.append(nueva_capa)
    return resultado


def demostracion():
    volumen = [
        [[20, 20, 20, 20, 20],
         [20, 100, 100, 100, 20],
         [20, 100, 255, 100, 20],
         [20, 100, 100, 100, 20],
         [20, 20, 20, 20, 20]],
        [[20, 20, 20, 20, 20],
         [20, 120, 120, 120, 20],
         [20, 120, 0, 120, 20],
         [20, 120, 120, 120, 20],
         [20, 20, 20, 20, 20]],
        [[20, 20, 20, 20, 20],
         [20, 140, 140, 140, 20],
         [20, 140, 255, 140, 20],
         [20, 140, 140, 140, 20],
         [20, 20, 20, 20, 20]]]
    resultado = suavizar_volumen(volumen)
    for capa in range(len(volumen)):
        print(f'\nCAPA {capa + 1} ORIGINAL')
        mostrar_matriz(volumen[capa])
        print(f'CAPA {capa + 1} SUAVIZADA')
        mostrar_matriz(resultado[capa])
    ruta = graficar_capas(volumen, resultado, 'SUAVIZADO.png', 'Suavizado por capas')
    print(f'\nGráfica guardada en {ruta}')


if __name__ == '__main__':
    demostracion()
