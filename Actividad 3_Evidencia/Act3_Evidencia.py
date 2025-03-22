"""
Herramientas Computacionales: El Arte de la Programación

Evidencia de Proyecto

Equipo: Jonathan Uziel Medina Rodríguez (A01255048), Pablo Ernesto Cruz Moreno (A01255437) y
        Miguel de Jesús Degollado Macías (A01255388@).

Docente: Baldomero Olvera Villanueva

Fecha: 23/03/2025

Descripción: Programa que aplica filtros de convolución a una radiografía para detectar cuerpos extraños, enfermedades respiratorias, etc.
"""
# Librerías
import numpy as np
import cv2
import os
import time
import matplotlib.pyplot as plt

# Función para agregar un filtro de convolución a una imagen. Complejidad O(n^2) al tener 2 iteraciones anidadas.
def convolucion(imagen, filtro):
    filaImg, colImg, = imagen.shape                                                 # Tamaño de la imagen (m filas, n columnas).
    filaF, colF = filtro.shape                                                      # Tamaño del filtro/kernel (k filas, l columnas).

    padding_y = int((filaF - 1)/2)                                                  # Padding en el eje Y (altura).
    padding_x = int((colF - 1)/2)                                                   # Padding en el eje X (ancho).

    matriz = np.zeros(imagen.shape)                                                 # Matriz resultante de ceros.

    imagenPadding = np.zeros((filaImg + (padding_y*2), colImg + (padding_x*2)))     # Matriz de ceros de la imagen con padding añadido.
    
    imagenPadding[padding_y:imagenPadding.shape[0] - padding_y,                     # Parte de la matriz es tomada por toda la imagen.
                  padding_x:imagenPadding.shape[1] - padding_x] = imagen

    """
    Se recorre cada columna de cada fila para llevara cabo la operación de convolución:
    sumatoria del producto de cada celda del filtro y de la imagen.
    """
    for i in range(filaImg):
        for j in range(colImg):
            matriz[i][j] = np.sum(imagenPadding[i:i + filaF, j:j + colF] * filtro)

    return matriz # Retornar matriz


# Programa principal
if __name__ == "__main__":

    # Ingresar nombre o directorio del archivo. 
    archivo = input("\nIngrese el nombre de la imagen: ")

    if os.path.isfile(archivo) == False:
        # Imagen no encontrada.
        print("\nNo se pudo encontrar la imagen.")

    else:

        colorMapArr = ["bone", "afmhot", "pink", "gray"]      # Mapas de color que admite el programa 
        colorMap = ""                                           # Mapa de color elegido por el usuario

        # Verificar que el usuario ingrese un mapa de color válido.
        while colorMap not in colorMapArr:
            colorMap = input("\nIngrese el nombre del mapa de color que quiera utilizar:\n"
                            "\t1. bone\n"
                            "\t2. afmhot\n"
                            "\t3. pink\n"
                            "\t4. gray\n"
                            "____________________________________________________________\n"
                            "Opción: ")
            
            if colorMap not in colorMapArr:
                print("\n\nEl mapa de color no es válido. Ingrese uno de los solicitados.\n\n")
                time.sleep(2)
            else:
                break

        # Se lee la imagen.
        imagen = cv2.imread(archivo)

        # La imagen se convierte a blanco y negro (escala de grises). 
        imagenEG = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)

        # Matriz del filtro de extensión de punto.
        extpt = np.array([[-0.627, -0.352, -0.627],
                          [-0.352, 1.923, -0.352],
                          [-0.627, -0.352, -0.627]])

        # Matriz de bordes modifcado.
        bordes = np.array([[-1, 0, -1],
                           [-1, -3, -1],
                           [-1, 0, -1]])
        
        # Matriz de filtro de Scharr modificado.
        scharr = np.array([[-3, 10, 3],
                           [1, -5, 1],
                           [-3, 0, 3]])
        
        # Sobel vertical.
        sobel = np.array([[-1, -2, -1],
                          [ -2, 1,  2],
                          [ 1,  2,  1]])
        
        # Nitidez 3x3
        nitidez = np.array([[1, 1, 1],
                            [1, 7, 1],
                            [1, 1, 1]])
        
        # Matrices de convolución con los filtros aplicados.
        mascara1 = convolucion(imagenEG, scharr)
        print("\nMáscara #1 aplicada.")
        mascara2 = convolucion(mascara1, bordes)
        print("\nMáscara #2 aplicada.")
        mascara3 = convolucion(mascara2, sobel)
        print("\nMáscara #3 aplicada.")
        mascara4 = convolucion(mascara3, nitidez)
        print("\nMáscara #4 aplicada.")

        time.sleep(1)

        # Definir la posición, mapa de color y título de la imagen con escala de grises.
        plt.subplot(1,2,1)
        plt.imshow(imagenEG, cmap="gray")
        plt.title("Imagen con Escala de Grises")

        # Definir la posición, mapa de color y título de la imagen con el filtro aplicado.
        plt.subplot(1,2,2)
        plt.imshow(mascara4, cmap=colorMap)
        plt.title("Imagen con el Filtro Aplicado")

        # Mostrar las imágenes.
        plt.show()

"""
Referencias:

- Función de convolución. (s. f.). ArcGIS Desktop. Recuperado el 20 de marzo de 2025 de https://desktop.arcgis.com/es/arcmap/latest/manage-data/raster-and-images/convolution-function.htm
- GeeksforGeeks. (2020, 22 abril). Matplotlib.pyplot.imshow() in Python. GeeksforGeeks. Recuperado el 20 de marzo de 2025 de https://www.geeksforgeeks.org/matplotlib-pyplot-imshow-in-python/
- GeeksforGeeks. (2022, 10 febrero). How to Fix: ValueError: setting an array element with a sequence. GeeksforGeeks. Recuperado el 20 de marzo de 2025 de https://www.geeksforgeeks.org/how-to-fix-valueerror-setting-an-array-element-with-a-sequence/
- GeeksforGeeks. (2023, 14 marzo). Introduction to Convolutions using Python. GeeksforGeeks. Recuperado el 20 de marzo de 2025 de https://www.geeksforgeeks.org/introduction-to-convolutions-using-python/
- GeeksforGeeks. (2024, 24 abril). Python - How to Check if a file or directory exists. GeeksforGeeks. Recuperado el 20 de marzo de 2025 de https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists/
- GeeksforGeeks. (2024, 2 agosto). Python OpenCV | cv2.imread() method. GeeksforGeeks. Recuperado el 20 de marzo de 2025 de https://www.geeksforgeeks.org/python-opencv-cv2-imread-method/
- GeeksforGeeks. (2024, 25 noviembre). How to display multiple images in one figure correctly in Matplotlib? GeeksforGeeks. Recuperado el 20 de marzo de 2025 de https://www.geeksforgeeks.org/how-to-display-multiple-images-in-one-figure-correctly-in-matplotlib/
- GeeksforGeeks. (2025, 24 enero). Numpy.zeros() in Python. GeeksforGeeks. Recuperado el 20 de marzo de 2025 de https://www.geeksforgeeks.org/numpy-zeros-python/
- 8.2 Matriz de convolución. (s. f.). GIMP. https://docs.gimp.org/2.6/es/plug-in-convmatrix.html
- Olvera, B. (s. f.). Convolución [Diapositivas; Digital]. Tecnológico de Monterrey. https://experiencia21.tec.mx/courses/554652/discussion_topics/3503409
- Olvera, B. (s. f.). Procesamiento de Imágenes y Visión Computacional [Diapositivas; Digital]. Tecnológico de Monterrey. https://experiencia21.tec.mx/courses/554652/discussion_topics/3503409

Basado en los siguientes códigos:

- "convolution.py" por Abhisek Jana. Recuperado de https://github.com/benjaminva/semena-tec-tools-vision/tree/master/Scripts/Ejemplos
- "simple_conv.py" por Abhisek Jana y Benajmin Valdes. Recuperado de https://github.com/benjaminva/semena-tec-tools-vision/tree/master/Scripts/Ejemplos
- "simple_sobel.py" por Abhisek Jana y Benajmin Valdes. Recuperado de https://github.com/benjaminva/semena-tec-tools-vision/tree/master/Scripts/Ejemplos
"""
