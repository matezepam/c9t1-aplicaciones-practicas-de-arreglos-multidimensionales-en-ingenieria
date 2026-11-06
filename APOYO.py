# Aquí reúno la presentación de los resultados para que cada ejercicio conserve
# sus cálculos con listas y bucles, dejando a Matplotlib únicamente el dibujo
# de las gráficas como imágenes PNG.

from pathlib import Path


def dimensiones_matriz(matriz):
    if not matriz or not matriz[0]:
        raise ValueError('La matriz debe tener filas y columnas.')
    # Una cantidad uniforme de columnas permite recorrer la matriz por índices
    # sin encontrar una fila más corta durante los cálculos de los ejercicios.
    columnas = len(matriz[0])
    for fila in matriz:
        if len(fila) != columnas:
            raise ValueError('Todas las filas deben tener la misma longitud.')
    return len(matriz), columnas


def dimensiones_volumen(volumen):
    if not volumen:
        raise ValueError('El volumen debe tener al menos una capa.')
    filas, columnas = dimensiones_matriz(volumen[0])
    for capa in volumen:
        if dimensiones_matriz(capa) != (filas, columnas):
            raise ValueError('Todas las capas deben tener las mismas dimensiones.')
    return len(volumen), filas, columnas


def mostrar_matriz(matriz):
    for fila in matriz:
        for valor in fila:
            print(f'{valor:10.2f}', end=' ')
        print()


# Guardo cada figura en la carpeta del proyecto y la cierro después para liberar
# sus recursos, así las ejecuciones sucesivas no acumulan ventanas en memoria.
def guardar_figura(figura, nombre):
    import matplotlib.pyplot as plt

    carpeta = Path(__file__).resolve().parent / 'RESULTADOS'
    carpeta.mkdir(exist_ok=True)
    ruta = carpeta / nombre
    figura.savefig(ruta, dpi=160, bbox_inches='tight')
    plt.close(figura)
    return ruta


# Comparo cada capa usando una escala común para que el contraste permita ver
# los cambios reales, sin añadir números encima de los píxeles de la imagen.
def graficar_capas(antes, despues, nombre, titulo, minimo=0, maximo=255):
    import matplotlib.pyplot as plt

    capas, filas, columnas = dimensiones_volumen(antes)
    if dimensiones_volumen(despues) != (capas, filas, columnas) or maximo <= minimo:
        raise ValueError('Las dimensiones y la escala deben ser compatibles.')
    figura, ejes = plt.subplots(capas, 2, figsize=(8, 3 * capas),
                                squeeze=False, layout='constrained')
    mapa = 'coolwarm' if nombre == 'PRESION.png' else 'gray'
    for capa in range(capas):
        for lado, volumen in enumerate((antes, despues)):
            eje = ejes[capa][lado]
            imagen = eje.imshow(volumen[capa], cmap=mapa, vmin=minimo,
                                vmax=maximo, interpolation='nearest')
            estado = 'Inicial' if lado == 0 else 'Resultado'
            eje.set_title(f'{estado} · Capa {capa + 1}')
            eje.set_xticks(range(columnas))
            eje.set_yticks(range(filas))
            eje.set_xlabel('Columna')
            eje.set_ylabel('Fila')
    figura.suptitle(titulo)
    unidad = 'Presión (Pa)' if mapa == 'coolwarm' else 'Intensidad de gris'
    figura.colorbar(imagen, ax=ejes.ravel().tolist(), label=unidad, shrink=0.8)
    return guardar_figura(figura, nombre)


# Las barras parten de cero y las líneas muestran una desviación estándar hacia
# ambos lados de la media para distinguir el nivel de temperatura y su variación.
def graficar_barras(promedios, desviaciones, etiquetas, nombre, titulo):
    import matplotlib.pyplot as plt

    if not promedios or not len(promedios) == len(desviaciones) == len(etiquetas):
        raise ValueError('Cada promedio necesita una desviación y una etiqueta.')
    figura, eje = plt.subplots(figsize=(8, 5), layout='constrained')
    barras = eje.bar(etiquetas, promedios, yerr=desviaciones, capsize=5,
                    color='steelblue', width=0.6, label='Media ± desviación estándar')
    eje.bar_label(barras, fmt='%.2f', padding=12)
    eje.set_title(titulo)
    eje.set_ylabel('Temperatura (°C)')
    eje.set_xlabel('Sensor' if nombre == 'SENSORES.png' else 'Momento')
    eje.set_axisbelow(True)
    eje.grid(axis='y', alpha=0.25)
    eje.margins(y=0.18)
    eje.legend(loc='upper left')
    return guardar_figura(figura, nombre)


# Mantengo la misma escala en los dos ejes para que la rotación no parezca un
# estiramiento, identificando cada punto con su correspondiente transformado.
def graficar_puntos(antes, despues, nombre, titulo):
    import matplotlib.pyplot as plt

    figura, eje = plt.subplots(figsize=(7, 7), layout='constrained')
    for puntos, color, etiqueta, sufijo in (
            (antes, 'steelblue', 'Originales', ''),
            (despues, 'darkorange', 'Transformados', "'")):
        eje.scatter([p[0] for p in puntos], [p[1] for p in puntos],
                    color=color, label=etiqueta, s=55)
        for indice, punto in enumerate(puntos):
            eje.annotate(f'P{indice + 1}{sufijo}', punto,
                         xytext=(6, 7), textcoords='offset points', color=color)
    eje.axhline(0, color='black', linewidth=0.8)
    eje.axvline(0, color='black', linewidth=0.8)
    eje.set_aspect('equal', adjustable='box')
    eje.set_xlabel('X')
    eje.set_ylabel('Y')
    eje.set_title(titulo)
    eje.grid(alpha=0.25)
    eje.margins(0.2)
    eje.legend()
    return guardar_figura(figura, nombre)
