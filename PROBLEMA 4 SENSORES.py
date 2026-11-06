# PROBLEMA 4
# La tabla utiliza cinco filas para momentos y cinco columnas para sensores,
# siguiendo la indicación final del enunciado para poder comparar tanto las
# mediciones de un sensor en el tiempo como las de todos los sensores en un momento.

from math import sqrt
from APOYO import dimensiones_matriz, mostrar_matriz, graficar_barras


# Divido entre la cantidad de mediciones porque describo el conjunto observado
# y devuelvo media y desviación juntas para reutilizar el cálculo en filas y columnas.
def promedio_y_desviacion(valores):
    if not valores:
        raise ValueError('Se necesita al menos una medición.')
    promedio = sum(valores) / len(valores)
    suma_cuadrados = 0.0
    for valor in valores:
        suma_cuadrados += (valor - promedio) ** 2
    # Elevar las diferencias al cuadrado evita que se cancelen entre sí y
    # la raíz devuelve una medida de dispersión expresada también en grados.
    desviacion = sqrt(suma_cuadrados / len(valores))
    return promedio, desviacion


# Las filas se consultan directamente y cada columna se reúne en una lista corta
# para aplicar la misma función sin duplicar las fórmulas, conservando la matriz
# original porque el análisis devuelve resultados y no reemplaza sus mediciones.
def analizar_sensores(tabla):
    filas, columnas = dimensiones_matriz(tabla)
    promedios_momentos, desviaciones_momentos = [], []
    promedios_sensores, desviaciones_sensores = [], []
    for fila in range(filas):
        promedio, desviacion = promedio_y_desviacion(tabla[fila])
        promedios_momentos.append(promedio)
        desviaciones_momentos.append(desviacion)
    # Mantengo fija la columna para reunir las mediciones del mismo sensor
    # a lo largo del tiempo y reutilizo esta lista en cada nueva columna.
    for columna in range(columnas):
        mediciones = []
        for fila in range(filas):
            mediciones.append(tabla[fila][columna])
        promedio, desviacion = promedio_y_desviacion(mediciones)
        promedios_sensores.append(promedio)
        desviaciones_sensores.append(desviacion)
    return (promedios_momentos, desviaciones_momentos,
            promedios_sensores, desviaciones_sensores)


def demostracion():
    tabla = [[22.0, 23.0, 21.5, 24.0, 22.5],
             [22.5, 23.4, 21.8, 24.5, 23.0],
             [23.0, 23.2, 22.1, 25.0, 23.5],
             [22.8, 24.0, 22.0, 24.7, 24.0],
             [23.2, 23.8, 22.4, 25.2, 23.8]]
    pm, dm, ps, ds = analizar_sensores(tabla)
    print('TEMPERATURAS EN °C | FILAS = MOMENTOS | COLUMNAS = SENSORES')
    mostrar_matriz(tabla)
    print('\nRESULTADOS POR SENSOR')
    for sensor in range(5):
        print(f'Sensor {sensor + 1} | Promedio {ps[sensor]:.3f} °C | '
              f'Desviación {ds[sensor]:.3f} °C')
    print('\nRESULTADOS POR MOMENTO')
    for momento in range(5):
        print(f'Momento {momento + 1} | Promedio {pm[momento]:.3f} °C | '
              f'Desviación {dm[momento]:.3f} °C')
    etiquetas_sensores = ['S1', 'S2', 'S3', 'S4', 'S5']
    etiquetas_momentos = ['M1', 'M2', 'M3', 'M4', 'M5']
    sensores = graficar_barras(ps, ds, etiquetas_sensores,
                               'SENSORES.png', 'Temperatura por sensor')
    momentos = graficar_barras(pm, dm, etiquetas_momentos,
                               'MOMENTOS.png', 'Temperatura por momento')
    print(f'\nGráficas guardadas en {sensores} y {momentos}')


if __name__ == '__main__':
    demostracion()
