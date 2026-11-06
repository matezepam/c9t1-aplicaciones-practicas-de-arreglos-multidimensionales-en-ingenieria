# PROBLEMA 2
# El fluido ocupa un volumen de tres capas, tres filas y tres columnas donde cada
# celda conserva presión, temperatura y las tres componentes de su velocidad,
# usando una perturbación inicial para observar su propagación entre vecinos.
# El modelo es una aproximación de una onda acústica y mantiene la temperatura
# constante porque no incluye intercambio térmico ni una simulación completa de flujo.

from APOYO import dimensiones_volumen, mostrar_matriz, graficar_capas


def crear_fluido(presion_base=101325.0, temperatura=20.0):
    volumen = []
    for capa in range(3):
        plano = []
        for fila in range(3):
            linea = []
            for columna in range(3):
                # Creo un registro distinto en cada posición para que cambiar
                # la presión de una celda no modifique las otras por referencia.
                linea.append({'presion': presion_base, 'temperatura': temperatura,
                              'velocidad_x': 0.0, 'velocidad_y': 0.0, 'velocidad_z': 0.0})
            plano.append(linea)
        volumen.append(plano)
    return volumen


# Extraigo sólo presiones cuando necesito conservar el paso anterior para no
# duplicar también temperatura y velocidad, que ya están en el estado actual.
def extraer_presiones(fluido):
    presiones = []
    for plano in fluido:
        capa = []
        for linea in plano:
            fila = []
            for celda in linea:
                fila.append(celda['presion'])
            capa.append(fila)
        presiones.append(capa)
    return presiones


# Fuera del volumen se considera presión ambiente fija para definir qué ocurre
# en los bordes sin acceder a posiciones negativas o inexistentes del arreglo.
def leer_presion(fluido, capa, fila, columna, exterior):
    capas, filas, columnas = len(fluido), len(fluido[0]), len(fluido[0][0])
    if 0 <= capa < capas and 0 <= fila < filas and 0 <= columna < columnas:
        return fluido[capa][fila][columna]['presion']
    return exterior


def propagar_un_paso(fluido, presion_anterior, dt=0.001, distancia=1.0,
                      rapidez_onda=340.0, densidad=1.2, presion_exterior=101325.0):
    capas, filas, columnas = dimensiones_volumen(fluido)
    if dimensiones_volumen(presion_anterior) != (capas, filas, columnas):
        raise ValueError('Las presiones anteriores deben tener las dimensiones del fluido.')
    if dt <= 0 or distancia <= 0 or rapidez_onda <= 0 or densidad <= 0:
        raise ValueError('El tiempo, la distancia, la rapidez y la densidad deben ser positivos.')
    # El límite de un tercio evita usar un paso de tiempo que haga crecer
    # artificialmente la onda al combinar sus cambios en las tres dimensiones.
    coeficiente = (rapidez_onda * dt / distancia) ** 2
    if coeficiente > 1 / 3:
        raise ValueError('El paso de tiempo es demasiado grande para esta cuadrícula 3D.')
    # Estos desplazamientos seleccionan los seis vecinos que comparten una
    # cara con la celda y permiten repetir la misma consulta en cada dirección.
    direcciones = [(0, 0, 1), (0, 0, -1), (0, 1, 0),
                   (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    # El factor es común a todas las celdas de este paso y se calcula una sola vez.
    factor_velocidad = dt / (2 * densidad * distancia)
    nuevo = []
    actuales = []
    for capa in range(capas):
        plano_nuevo, plano_actual = [], []
        for fila in range(filas):
            fila_nueva, fila_actual = [], []
            for columna in range(columnas):
                celda = fluido[capa][fila][columna]
                presion = celda['presion']
                vecinos = []
                for dc, df, dj in direcciones:
                    vecinos.append(leer_presion(fluido, capa + dc, fila + df,
                                                columna + dj, presion_exterior))
                # El paso previo conserva la evolución de la onda y la diferencia
                # con los seis vecinos representa su cambio espacial, en vez de
                # promediar presiones como si fuera un simple suavizado.
                diferencia_vecinos = sum(vecinos) - 6 * presion
                siguiente = (2 * presion - presion_anterior[capa][fila][columna]
                             + coeficiente * diferencia_vecinos)
                # La diferencia de presión entre lados opuestos determina
                # el cambio de velocidad en cada eje durante este paso.
                fila_nueva.append({
                    'presion': siguiente,
                    # Conservo la temperatura porque este modelo sigue la onda
                    # de presión y no calcula intercambio de calor entre celdas.
                    'temperatura': celda['temperatura'],
                    'velocidad_x': celda['velocidad_x'] - factor_velocidad * (vecinos[0] - vecinos[1]),
                    'velocidad_y': celda['velocidad_y'] - factor_velocidad * (vecinos[2] - vecinos[3]),
                    'velocidad_z': celda['velocidad_z'] - factor_velocidad * (vecinos[4] - vecinos[5])})
                fila_actual.append(presion)
            plano_nuevo.append(fila_nueva)
            plano_actual.append(fila_actual)
        nuevo.append(plano_nuevo)
        actuales.append(plano_actual)
    return nuevo, actuales


# Se guarda el estado siguiente por separado para que todas las celdas lean el
# mismo instante y el resultado no dependa del orden de los tres ciclos anidados.
def simular_fluido(fluido, pasos):
    if type(pasos) is not int or pasos < 0:
        raise ValueError('La cantidad de pasos debe ser un entero no negativo.')
    anterior = extraer_presiones(fluido)
    actual = fluido
    # Reemplazo los estados al avanzar para no guardar un historial completo
    # del volumen, conservando sólo la información necesaria para el próximo paso.
    for paso in range(pasos):
        actual, anterior = propagar_un_paso(actual, anterior)
    return actual


def demostracion():
    inicial = crear_fluido()
    inicial[1][1][1]['presion'] += 1000
    final = simular_fluido(inicial, pasos=4)
    presiones_iniciales = extraer_presiones(inicial)
    presiones_finales = extraer_presiones(final)
    print('VOLUMEN DE 3 CAPAS, 3 FILAS Y 3 COLUMNAS')
    for capa in range(3):
        print(f'\nPresión final en Pa de la capa {capa + 1}')
        mostrar_matriz(presiones_finales[capa])
    celda = final[1][1][0]
    print(f'\nTemperatura de ejemplo {celda["temperatura"]:.1f} °C')
    print(f'Velocidad de ejemplo X {celda["velocidad_x"]:.4f} m/s, '
          f'Y {celda["velocidad_y"]:.4f} m/s, Z {celda["velocidad_z"]:.4f} m/s')
    ruta = graficar_capas(presiones_iniciales, presiones_finales,
                          'PRESION.png', 'Propagación de presión en Pa', 100000, 103000)
    print(f'\nGráfica guardada en {ruta}')


if __name__ == '__main__':
    demostracion()
