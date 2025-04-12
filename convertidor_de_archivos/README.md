# Convertidor de Archivos

Una aplicación de conversión de archivos con interfaz gráfica desarrollada en PyQt5, que permite transformar diversos formatos de documentos e imágenes de manera rápida y sencilla.

## Características Principales

### Texto y Documentos
- Convertir Excel a CSV
- Convertir Word a PDF
- Convertir TXT a PDF
- Convertir PDF a TXT

### Imágenes y Gráficos
- Convertir JPG a PDF
- Convertir PNG a PDF
- Convertir JPG a PNG
- Convertir PNG a JPG
- Convertir PNG a AVIF
- Convertir PNG a SVG
- Convertir WEBP a PNG
- Convertir AVIF a PNG
- Convertir SVG a PNG
- Convertir SVG a PDF
- Convertir BMP a PNG

## Requisitos

- Python 3.6+
- PyQt5
- pandas
- docx2pdf
- Pillow (PIL)
- numpy
- potrace (para conversión a SVG)
- PyMuPDF (para procesamiento de PDF)

## Instalación

```bash
# Instalación de dependencias principales
pip install PyQt5 pandas docx2pdf pillow numpy PyMuPDF

# Para conversión PNG a SVG
pip install pypotrace


## Configuración

Para mostrar correctamente las imágenes de fondo en el programa:

1. Crea una carpeta llamada `assets` en el directorio del proyecto.
2. Coloca todos los archivos de imagen dentro de la carpeta `assets`.
3. Asegúrate de que el archivo principal del programa esté ubicado fuera de la carpeta `assets`, en el directorio raíz del proyecto.

## Uso básico

1. Ejecuta el programa con `python main.py`
2. Selecciona el tipo de conversión que deseas realizar
3. Carga el archivo o archivos de origen
4. Selecciona la ubicación de destino
5. Haz clic en "Convertir" y espera a que finalice el proceso

## Interfaz de Usuario

La aplicación cuenta con una interfaz moderna y sencilla que incluye:
- Pantalla de inicio con animación
- Selector de tipo de conversión organizado por categorías
- Selección de archivos de entrada/salida
- Barra de progreso para seguimiento de la conversión
- Mensajes de estado con retroalimentación visual
- Tema claro/oscuro personalizable

## Soporte y contribuciones

Para reportar errores o solicitar nuevas características, por favor crea un issue en el repositorio del proyecto. Las contribuciones son bienvenidas a través de pull requests.

## Desarrolladores

Desarrollado por: Daniel Ruiz Poli  
Academia: ConquerBlocks  
Web: [conquerblocks.com](https://conquerblocks.com)



## Versión
4.0  
Fecha: Abril 2025
