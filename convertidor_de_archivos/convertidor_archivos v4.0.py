from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QComboBox, 
                            QFileDialog, QProgressBar, QMessageBox, QFrame, QSplashScreen, QLineEdit,
                            QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient
import sys
import pandas as pd
from docx2pdf import convert
from PIL import Image
import os
import subprocess
import shutil

#clase SplashScreen
class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        width = 680
        height = 400
        
        # boton de inicio
        self.start_button = QPushButton("Iniciar Programa", self)

        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        
        # Agregar sombra al botón de inicio
        sombra_boton = QGraphicsDropShadowEffect()
        sombra_boton.setBlurRadius(8)
        sombra_boton.setColor(QColor(0, 0, 0, 80))
        sombra_boton.setOffset(0, 3)
        self.start_button.setGraphicsEffect(sombra_boton)
        
        self.start_button.hide()
        self.start_button.clicked.connect(self.start_main_program)
        
        # pixmap con fondo negro
        self.pixmap = QPixmap(width, height)
        self.pixmap.fill(QColor(0, 0, 0))
        
        # Configura el diseño del splash
        self.setPixmap(self.pixmap)
        
        # Contador para la animación
        self.counter = 0
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        # Inicia el timer para la animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)
        
        # Dibuja el splash inicial
        self.draw_splash()

    def draw_splash(self):
        # Crea un nuevo pixmap y pintor
        pixmap = QPixmap(self.size())
        pixmap.fill(QColor(0, 0, 0))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Configura la fuente
        font = QFont()
        font.setFamily('Segoe UI')
        font.setBold(True)
        
        # Dibuja el titulo
        font.setPointSize(30)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(0, 50, self.width(), 50, Qt.AlignCenter, 'Convertidor de Archivos')
        
        # Dibuja el subtitulo
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(0, 100, self.width(), 30, Qt.AlignCenter, 'v3.8')
        
        # Información del desarrollador
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QColor(180, 180, 180))
        
        # Datos del desarrollador
        dev_info = [
            "Desarrollado por: Daniel Ruiz Poli",
            "Email: danielruiz36@gmail.com",
            "GitHub: github.com/PolixDev",
            "Academia: ConquerBlocks"
        ]
        
        y_position = 150
        for info in dev_info:
            painter.drawText(0, y_position, self.width(), 30, Qt.AlignCenter, info)
            y_position += 25
        
        # Dibuja la barra de carga
        painter.setPen(QColor(255, 255, 255))
        painter.drawRoundedRect(140, 280, 400, 20, 10, 10)
        
        # Barra de progreso interior    
        painter.setBrush(QColor(21, 156, 231))
        painter.setPen(Qt.NoPen)
        progress_width = int((self.counter/100) * 392)
        painter.drawRoundedRect(144, 284, progress_width, 12, 6, 6)
        
        # Texto de carga
        painter.setPen(QColor(255, 255, 255))
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(0, 320, self.width(), 30, Qt.AlignCenter, f'Cargando... {self.counter}%')
        
        # Actualiza la posición del botón
        button_width = 200
        button_height = 40
        button_x = (self.width() - button_width) // 2
        button_y = 360
        self.start_button.setGeometry(button_x, button_y, button_width, button_height)
        
        painter.end()
        self.setPixmap(pixmap)
#fin de la clase SplashScreen

#metodo para la animacion de la barra de carga
    def loading(self):
        self.counter += 1
        self.draw_splash()
        
        if self.counter >= 100:
            self.timer.stop()
            self.start_button.show()  # Muestra el botón cuando la carga está completa

    def set_main_window(self, window):
        self.main_window = window

    def start_main_program(self):
        if hasattr(self, 'main_window'):
            self.main_window.show()
            self.close()

#clase para la conversion de archivos
class ConvertidorThread(QThread):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(int)


#metodo para iniciar la conversion de archivos  
    def __init__(self, tipo_conversion, ruta_entrada, ruta_salida):
        super().__init__()
        self.tipo_conversion = tipo_conversion
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = ruta_salida

#metodo para iniciar la conversion de archivos
    def run(self):
        try:
            self.progress.emit(10)
            if self.tipo_conversion == "Excel a CSV":
                df = pd.read_excel(self.ruta_entrada)
                self.progress.emit(50)
                df.to_csv(self.ruta_salida, index=False)
                self.progress.emit(100)
            
            elif self.tipo_conversion == "Word a PDF":
                convert(self.ruta_entrada, self.ruta_salida)
                self.progress.emit(100)
            
            elif self.tipo_conversion in ["JPG a PDF", "PNG a PDF", "SVG a PDF"]:
                try:
                    imagen = Image.open(self.ruta_entrada)
                    self.progress.emit(40)
                    imagen_rgb = imagen.convert('RGB')
                    self.progress.emit(70)
                    imagen_rgb.save(self.ruta_salida, 'PDF')
                    self.progress.emit(100)
                except Exception as e:
                    self.finished.emit(False, f"Error al convertir a PDF: {str(e)}")
                    return
            
            elif self.tipo_conversion in ["JPG a PNG", "WEBP a PNG", "SVG a PNG", "AVIF a PNG"]:
                try:
                    imagen = Image.open(self.ruta_entrada)
                    self.progress.emit(50)
                    imagen.save(self.ruta_salida, 'PNG')
                    self.progress.emit(100)
                except Exception as e:
                    self.finished.emit(False, f"Error al convertir a PNG: {str(e)}")
                    return

            elif self.tipo_conversion == "PNG a JPG":
                try:
                    imagen = Image.open(self.ruta_entrada)
                    if imagen.mode in ('RGBA', 'LA') or (imagen.mode == 'P' and 'transparency' in imagen.info):
                        fondo = Image.new('RGB', imagen.size, (255, 255, 255))
                        if imagen.mode == 'RGBA':
                            fondo.paste(imagen, mask=imagen.split()[3])
                        else:
                            fondo.paste(imagen)
                        imagen = fondo
                    self.progress.emit(50)
                    imagen.save(self.ruta_salida, 'JPEG', quality=95)
                    self.progress.emit(100)
                except Exception as e:
                    self.finished.emit(False, f"Error al convertir a JPG: {str(e)}")
                    return
                
            elif self.tipo_conversion == "PNG a AVIF":
                try:
                    # Verificar si ImageMagick está instalado
                    if not shutil.which('convert'):
                        self.finished.emit(False, "ImageMagick no está instalado. Por favor, instálelo con: sudo apt-get install imagemagick")
                        return
                    
                    self.progress.emit(30)
                    
                    # Usar ImageMagick para convertir PNG a AVIF
                    comando = ['convert', self.ruta_entrada, self.ruta_salida]
                    proceso = subprocess.run(comando, capture_output=True, text=True)
                    
                    self.progress.emit(80)
                    
                    # Verificar si hubo errores
                    if proceso.returncode != 0:
                        self.finished.emit(False, f"Error al convertir con ImageMagick: {proceso.stderr}")
                        return
                    
                    self.progress.emit(100)
                except Exception as e:
                    self.finished.emit(False, f"Error al convertir a AVIF: {str(e)}\nAsegúrate de tener instalado ImageMagick: sudo apt-get install imagemagick")
                    return

            elif self.tipo_conversion == "PNG a SVG":
                # Para PNG a SVG requiere bibliotecas adicionales como potrace
                try:
                    import potrace
                    import numpy as np
                    
                    # Convertir imagen a modo binario para el trazado
                    self.progress.emit(20)
                    try:
                        imagen = Image.open(self.ruta_entrada).convert('L')
                    except Exception as e:
                        self.finished.emit(False, f"Error al abrir la imagen PNG: {str(e)}")
                        return
                        
                    self.progress.emit(30)
                    
                    # Convertir a array de NumPy y binarizar
                    data = np.array(imagen)
                    data = (data > 128).astype(np.uint32)
                    self.progress.emit(50)
                    
                    # Crear un objeto de bitmap para potrace
                    bmp = potrace.Bitmap(data)
                    # Trazar el contorno
                    path = bmp.trace()
                    self.progress.emit(70)
                    
                    # Generar SVG
                    with open(self.ruta_salida, 'w') as f:
                        f.write(f'<svg width="{imagen.width}" height="{imagen.height}" xmlns="http://www.w3.org/2000/svg">')
                        f.write('<path fill="black" d="')
                        
                        # Escribir los datos del trazado
                        for curve in path:
                            f.write(f'M {curve.start_point.x} {curve.start_point.y} ')
                            for segment in curve:
                                if segment.is_corner:
                                    f.write(f'L {segment.c.x} {segment.c.y} L {segment.end_point.x} {segment.end_point.y} ')
                                else:
                                    f.write(f'C {segment.c1.x} {segment.c1.y} {segment.c2.x} {segment.c2.y} {segment.end_point.x} {segment.end_point.y} ')
                        f.write('Z"/></svg>')
                    self.progress.emit(100)
                except ImportError:
                    self.finished.emit(False, "Se requiere el módulo 'potrace'. Instálelo con: pip install pypotrace")
                    return
                except Exception as e:
                    self.finished.emit(False, f"Error al procesar la imagen: {str(e)}")
                    return

            self.finished.emit(True, "Conversión completada con éxito")
        except Exception as e:
            self.finished.emit(False, str(e))

#clase para la ventana principal
class ConvertidorArchivos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor de Archivos v3.8 por PolixDev")
        self.setMinimumSize(1600, 900)
        self.resize(1600, 900)
        
        # Widget central personalizado con imagen de fondo
        class CentralWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                # Obtener la ruta absoluta del directorio actual para cargar la imagen de fondo en la carpeta assets
                current_dir = os.path.dirname(os.path.abspath(__file__))
                self.assets_dir = os.path.join(current_dir, "assets")
                self.background_path = os.path.join(self.assets_dir, "imgsplash1.png")
                
                # Crear directorio assets si no existe
                if not os.path.exists(self.assets_dir):
                    os.makedirs(self.assets_dir)
                    print(f"Directorio assets creado en: {self.assets_dir}")
                
                # Verificar si existe la imagen
                if not os.path.exists(self.background_path):
                    print(f"""
                    ATENCIÓN: Imagen de fondo no encontrada
                    Por favor, coloque el archivo 'imgsplash1.png' en:
                    {self.assets_dir}
                    """)

#metodo para dibujar el fondo de la ventana
            def paintEvent(self, event):
                painter = QPainter(self)
                
                if os.path.exists(self.background_path):
                    # Cargar y dibujar la imagen si existe
                    pixmap = QPixmap(self.background_path)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(
                            self.size(), 
                            Qt.KeepAspectRatioByExpanding, 
                            Qt.SmoothTransformation
                        )
                        # Centrar la imagen
                        x = (self.width() - scaled_pixmap.width()) // 2
                        y = (self.height() - scaled_pixmap.height()) // 2
                        painter.drawPixmap(x, y, scaled_pixmap)
                    else:
                        self._draw_fallback_background(painter)
                else:
                    self._draw_fallback_background(painter)

            def _draw_fallback_background(self, painter):
                # Fondo degradado como respaldo
                gradient = QLinearGradient(0, 0, 0, self.height())
                gradient.setColorAt(0, QColor("#2c3e50"))
                gradient.setColorAt(1, QColor("#3498db"))
                painter.fillRect(self.rect(), gradient)

        # Widget central principal
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(50, 190, 50, 40)

        # Contenedor principal con fondo más transparente
        self.contenedor = QFrame()
        self.contenedor.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.92);
                border-radius: 18px;
                padding: 30px;
                border: 1px solid rgba(255, 255, 255, 0.7);
            }
        """)
        
        # Aplicar sombra al contenedor
        sombra_contenedor = QGraphicsDropShadowEffect()
        sombra_contenedor.setBlurRadius(20)
        sombra_contenedor.setColor(QColor(0, 0, 0, 60))
        sombra_contenedor.setOffset(0, 8)
        self.contenedor.setGraphicsEffect(sombra_contenedor)
        
        #estilos de la ventana principal
        self.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: bold;
            }   
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            } 
            QPushButton:hover {
                background-color: #2980B9;
            } 
            QPushButton:pressed {
                background-color: #1C5980;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
            }
            QComboBox {
                padding: 10px;
                border: 2px solid #BDC3C7;
                border-radius: 8px;
                background-color: white;
                min-width: 220px;
                font-weight: bold;
                selection-background-color: #3498DB;
            }
            QComboBox:hover {
                border-color: #3498DB;
            }
            QComboBox:drop-down {
                border: none;
                width: 30px;
            }
            QComboBox:down-arrow {
                background-color: #3498DB;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #3498DB;
                selection-color: white;
            }
            QProgressBar {
                border: 2px solid #BDC3C7;
                border-radius: 8px;
                text-align: center;
                height: 25px;
                background-color: white;
                font-weight: bold;
                color: #2C3E50;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27AE60, stop:1 #2ECC71);
                border-radius: 6px;
            }
            QLineEdit {
                background-color: white;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #BDC3C7;
                color: #2C3E50;
                font-weight: bold;
            }
            QLineEdit:focus {
                border-color: #3498DB;
            }
        """)
        
        self.setup_ui()

#metodo para aplicar sombra a un widget
    def aplicar_sombra(self, widget, radio=5, offset_x=2, offset_y=2, color=QColor(0, 0, 0, 50)):
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(radio)
        sombra.setColor(color)
        sombra.setOffset(offset_x, offset_y)
        widget.setGraphicsEffect(sombra)

#metodo para configurar la ventana principal        
    def setup_ui(self):
        # Título
        titulo = QLabel("")
        titulo.setFont(QFont("Arial", 30, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: white; background-color: transparent;")
        self.main_layout.addWidget(titulo)

        # Contenedor principal con fondo semi-transparente
        contenedor_layout = QVBoxLayout(self.contenedor)
        contenedor_layout.setSpacing(20)

        # Selector de conversión
        tipo_layout = QHBoxLayout()
        tipo_label = QLabel("Tipo de conversión:")
        tipo_label.setStyleSheet("""
            QLabel {
                background-color: rgba(44, 62, 80, 0.1);
                padding: 10px;
                border-radius: 8px;
                color: #2C3E50;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        self.tipo_combo = QComboBox()
        self.tipo_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(52, 152, 219, 0.1);
                padding: 10px;
                border-radius: 8px;
                color: #2C3E50;
                font-weight: bold;
                border: 2px solid rgba(52, 152, 219, 0.3);
                font-size: 15px;
            }
            QComboBox:hover {
                background-color: rgba(52, 152, 219, 0.2);
                border-color: rgba(52, 152, 219, 0.5);
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                background-color: #3498DB;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: rgba(52, 152, 219, 0.8);
                selection-color: white;
            }
        """)
        
        # Agregar categorías y opciones
        self.tipo_combo.addItem("Seleccione tipo de conversión")
        self.tipo_combo.insertSeparator(1)
        
        # Categoría Texto y Documentos
        self.tipo_combo.addItem("-- Texto y Documentos --")
        self.tipo_combo.addItems([
            "Excel a CSV",
            "Word a PDF"
        ])
        self.tipo_combo.insertSeparator(5)
        
        # Categoría Imágenes y Gráficos
        self.tipo_combo.addItem("-- Imágenes y Gráficos --")
        self.tipo_combo.addItems([
            "JPG a PDF",
            "PNG a PDF",
            "JPG a PNG",
            "PNG a JPG",
            "PNG a AVIF",
            "PNG a SVG",
            "WEBP a PNG",
            "AVIF a PNG",
            "SVG a PNG",
            "SVG a PDF"
        ])
        
        tipo_layout.addWidget(tipo_label)
        tipo_layout.addWidget(self.tipo_combo)
        contenedor_layout.addLayout(tipo_layout)

        # Archivo de entrada
        entrada_layout = QHBoxLayout()
        self.entrada_label = QLabel("Archivo no seleccionado")
        self.entrada_label.setStyleSheet("""
            QLabel {
                background-color: rgba(44, 62, 80, 0.1);
                padding: 10px;
                border-radius: 8px;
                color: #2C3E50;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        entrada_btn = QPushButton("Seleccionar archivo")
        entrada_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                icon-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #1C5980;
            }
        """)
        entrada_btn.clicked.connect(self.seleccionar_entrada)
        entrada_layout.addWidget(self.entrada_label)
        entrada_layout.addWidget(entrada_btn)
        contenedor_layout.addLayout(entrada_layout)
        
        # Aplicar sombra al botón de entrada
        self.aplicar_sombra(entrada_btn)

        # Archivo de salida
        salida_layout = QHBoxLayout()
        self.salida_label = QLabel("Ubicación no seleccionada")
        self.salida_label.setStyleSheet("""
            QLabel {
                background-color: rgba(44, 62, 80, 0.1);
                padding: 10px;
                border-radius: 8px;
                color: #2C3E50;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        # Campo para editar el nombre del archivo de salida
        self.nombre_salida = QLineEdit()
        self.nombre_salida.setPlaceholderText("Nombre del archivo de salida")
        self.nombre_salida.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #BDC3C7;
                color: #2C3E50;
                font-weight: bold;
                font-size: 15px;
            }
            QLineEdit:focus {
                border-color: #3498DB;
            }
        """)
        self.nombre_salida.setVisible(False)
        
        salida_btn = QPushButton("Seleccionar destino")
        salida_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #1C5980;
            }
        """)
        salida_btn.clicked.connect(self.seleccionar_salida)
        
        salida_layout.addWidget(self.salida_label)
        salida_layout.addWidget(self.nombre_salida)
        salida_layout.addWidget(salida_btn)
        contenedor_layout.addLayout(salida_layout)
        
        # Aplicar sombra al botón de salida
        self.aplicar_sombra(salida_btn)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #BDC3C7;
                border-radius: 8px;
                text-align: center;
                height: 28px;
                background-color: white;
                font-weight: bold;
                font-size: 14px;
                color: #2C3E50;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27AE60, stop:1 #2ECC71);
                border-radius: 6px;
            }
        """)
        contenedor_layout.addWidget(self.progress_bar)

        # Botón convertir
        self.convertir_btn = QPushButton("Convertir")
        self.convertir_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27AE60, stop:1 #2ECC71);
                font-weight: bold;
                padding: 15px;
                font-size: 16px;
                border-radius: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #219a52, stop:1 #25a25a);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e8449, stop:1 #208e4e);
            }
        """)
        self.convertir_btn.clicked.connect(self.iniciar_conversion)
        contenedor_layout.addWidget(self.convertir_btn)
        
        # Aplicar sombra al botón de convertir
        self.aplicar_sombra(self.convertir_btn, radio=8, offset_y=3, color=QColor(0, 0, 0, 80))

        # Agregar el contenedor al layout principal
        self.main_layout.addWidget(self.contenedor)
        
        # Estado
        self.estado_label = QLabel("")
        self.estado_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.estado_label)

        self.ruta_entrada = ""
        self.ruta_salida = ""

#metodo para seleccionar el archivo de entrada
    def seleccionar_entrada(self):
        tipos_archivo = self.obtener_tipos_archivo()
        if not tipos_archivo:
            QMessageBox.warning(self, "Advertencia", "Seleccione primero el tipo de conversión")
            return

        filename, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo", "", tipos_archivo)
        if filename:
            self.ruta_entrada = filename
            self.entrada_label.setText(os.path.basename(filename))
            # Sugerir nombre de salida
            base = os.path.splitext(filename)[0]
            extension = self.obtener_extension_salida()
            self.ruta_salida = f"{base}{extension}"
            self.salida_label.setText(os.path.basename(self.ruta_salida))
            # Mostrar campo para editar nombre
            self.nombre_salida.setVisible(True)
            self.nombre_salida.setText(os.path.splitext(os.path.basename(self.ruta_salida))[0])

#metodo para seleccionar el archivo de salida
    def seleccionar_salida(self):
        extension = self.obtener_extension_salida()
        if not extension:
            QMessageBox.warning(self, "Advertencia", "Seleccione primero el tipo de conversión")
            return

        # Obtener el nombre personalizado si existe
        nombre_archivo = self.nombre_salida.text().strip() or "output"
        nombre_archivo = f"{nombre_archivo}{extension}"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar como", nombre_archivo, f"Archivo (*{extension})")
        if filename:
            self.ruta_salida = filename
            self.salida_label.setText(os.path.basename(filename))
            # Actualizar el campo de nombre con el nuevo nombre
            self.nombre_salida.setText(os.path.splitext(os.path.basename(filename))[0])

#metodo para obtener los tipos de archivos
    def obtener_tipos_archivo(self):
        tipo = self.tipo_combo.currentText()
        if tipo == "Excel a CSV":
            return "Excel Files (*.xlsx *.xls)"
        elif tipo == "Word a PDF":
            return "Word Files (*.docx *.doc)"
        elif tipo == "JPG a PDF":
            return "Image Files (*.jpg *.jpeg)"
        elif tipo == "PNG a PDF":
            return "PNG Files (*.png)"
        elif tipo == "JPG a PNG":
            return "Image Files (*.jpg *.jpeg)"
        elif tipo == "WEBP a PNG":
            return "WEBP Files (*.webp)"
        elif tipo == "AVIF a PNG":
            return "AVIF Files (*.avif)"
        elif tipo == "PNG a JPG":
            return "PNG Files (*.png)"
        elif tipo == "PNG a AVIF":
            return "PNG Files (*.png)"
        elif tipo == "PNG a SVG":
            return "PNG Files (*.png)"
        elif tipo == "SVG a PNG":
            return "SVG Files (*.svg)"
        elif tipo == "SVG a PDF":
            return "SVG Files (*.svg)"
        return ""

#metodo para obtener la extension de salida
    def obtener_extension_salida(self):
        tipo = self.tipo_combo.currentText()
        if tipo == "Excel a CSV":
            return ".csv"
        elif tipo in ["Word a PDF", "JPG a PDF", "PNG a PDF", "SVG a PDF"]:
            return ".pdf"
        elif tipo in ["JPG a PNG", "WEBP a PNG", "SVG a PNG", "AVIF a PNG"]:
            return ".png"
        elif tipo == "PNG a JPG":
            return ".jpg"
        elif tipo == "PNG a AVIF":
            return ".avif"
        elif tipo == "PNG a SVG":
            return ".svg"
        return ""

#metodo para iniciar la conversion de archivos
    def iniciar_conversion(self):
        if not self.validar_campos():
            return

        # Verificar si el archivo de salida ya existe
        if os.path.exists(self.ruta_salida):
            respuesta = QMessageBox.question(
                self, 
                "Archivo existente", 
                "El archivo de salida ya existe. ¿Desea sobrescribirlo?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.No:
                return

        self.convertir_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.estado_label.setText("Convirtiendo...")
        
        self.thread = ConvertidorThread(
            self.tipo_combo.currentText(),
            self.ruta_entrada,
            self.ruta_salida
        )
        self.thread.progress.connect(self.actualizar_progreso)
        self.thread.finished.connect(self.conversion_terminada)
        self.thread.start()

#metodo para actualizar el progreso
    def actualizar_progreso(self, valor):
        self.progress_bar.setValue(valor)

#metodo para terminar la conversion de archivos
    def conversion_terminada(self, exito, mensaje):
        try:
            self.convertir_btn.setEnabled(True)
            if exito:
                self.estado_label.setText("¡Conversión completada!")
                self.estado_label.setStyleSheet("""
                    font-size: 28px;
                    font-weight: bold;
                    color: #27AE60;
                    background-color: rgba(255, 255, 255, 0.8);
                    border: 2px solid #27AE60;
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 10px;
                """)
                # Sombra para el mensaje de éxito
                sombra_estado = QGraphicsDropShadowEffect()
                sombra_estado.setBlurRadius(10)
                sombra_estado.setColor(QColor(39, 174, 96, 100))
                sombra_estado.setOffset(0, 4)
                self.estado_label.setGraphicsEffect(sombra_estado)
                
                QMessageBox.information(self, "Éxito", mensaje)
            else:
                self.estado_label.setText(f"Error en la conversión: {mensaje}")
                self.estado_label.setStyleSheet("""
                    font-size: 24px;
                    font-weight: bold;
                    color: #E74C3C;
                    background-color: rgba(255, 255, 255, 0.8);
                    border: 2px solid #E74C3C;
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 10px;
                """)
                # Sombra para el mensaje de error
                sombra_estado = QGraphicsDropShadowEffect()
                sombra_estado.setBlurRadius(10)
                sombra_estado.setColor(QColor(231, 76, 60, 100))
                sombra_estado.setOffset(0, 4)
                self.estado_label.setGraphicsEffect(sombra_estado)
                
                QMessageBox.critical(self, "Error", f"Error durante la conversión: {mensaje}")
        except Exception as e:
            print(f"Error en conversion_terminada: {str(e)}")

#metodo para validar los campos
    def validar_campos(self):
        # Obtener el tipo de conversión seleccionado
        self.tipo_conversion = self.tipo_combo.currentText()
        
        # Validaciones básicas
        if self.tipo_conversion == "Seleccione tipo de conversión" or self.tipo_conversion.startswith("--"):
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un tipo de conversión válido")
            return False
            
        if not self.ruta_entrada:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un archivo de entrada")
            return False
            
        if not os.path.exists(self.ruta_entrada):
            QMessageBox.warning(self, "Advertencia", f"El archivo de entrada no existe: {self.ruta_entrada}")
            return False
            
        if not self.ruta_salida:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione la ubicación de salida")
            return False
            
        if not self.nombre_salida.text().strip():
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un nombre válido para el archivo de salida")
            return False
            
        # Validar directorio de salida existe
        directorio_salida = os.path.dirname(self.ruta_salida)
        if directorio_salida and not os.path.exists(directorio_salida):
            try:
                os.makedirs(directorio_salida)
            except Exception as e:
                QMessageBox.warning(self, "Advertencia", f"No se puede crear el directorio de salida: {str(e)}")
                return False
                
        # Verificaciones específicas por tipo de conversión
        if self.tipo_conversion == "PNG a SVG":
            try:
                import potrace
            except ImportError:
                QMessageBox.warning(self, "Advertencia", "Se requiere la biblioteca potrace para esta conversión.\nInstálela con: pip install pypotrace")
                return False
        
        return True

#metodo para iniciar la aplicacion
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        splash = SplashScreen()
        window = ConvertidorArchivos()
        splash.set_main_window(window)
        splash.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error en la aplicación principal: {str(e)}") 