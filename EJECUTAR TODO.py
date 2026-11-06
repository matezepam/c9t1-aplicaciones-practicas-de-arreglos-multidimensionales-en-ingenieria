# Este archivo permite probar los cinco ejercicios con una sola ejecución,
# usando el mismo intérprete del entorno donde se instaló Matplotlib para
# evitar que cada programa busque la biblioteca en una instalación diferente.

from pathlib import Path
import subprocess
import sys


def ejecutar_ejercicios():
    carpeta = Path(__file__).resolve().parent
    archivos = [
        'PROBLEMA 1 FUERZAS.py',
        'PROBLEMA 2 FLUIDO.py',
        'PROBLEMA 3 IMAGENES MEDICAS.py',
        'PROBLEMA 4 SENSORES.py',
        'PROBLEMA 5 COORDENADAS.py',
    ]
    # Los ejecuto por separado y en orden para conservar la salida de cada
    # problema y detener la prueba si alguno presenta un error.
    for archivo in archivos:
        print(f'\nEJECUTANDO {archivo}', flush=True)
        subprocess.run([sys.executable, str(carpeta / archivo)], check=True)
    print('\nLos cinco ejercicios finalizaron correctamente')
    print(f'Las gráficas están en {carpeta / "RESULTADOS"}')


if __name__ == '__main__':
    ejecutar_ejercicios()
