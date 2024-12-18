from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QComboBox, 
                            QFileDialog, QProgressBar, QMessageBox, QFrame, QSplashScreen)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient
import sys
import pandas as pd
from docx2pdf import convert
from PIL import Image
import os
import time

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
        painter.drawText(0, 100, self.width(), 30, Qt.AlignCenter, 'v2.8')
        
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
            
            elif self.tipo_conversion == "Word a PDF":
                convert(self.ruta_entrada, self.ruta_salida)
            
            elif self.tipo_conversion in ["JPG a PDF", "PNG a PDF"]:
                imagen = Image.open(self.ruta_entrada)
                self.progress.emit(40)
                imagen_rgb = imagen.convert('RGB')
                self.progress.emit(70)
                imagen_rgb.save(self.ruta_salida, 'PDF')
            
            elif self.tipo_conversion == "JPG a PNG":
                imagen = Image.open(self.ruta_entrada)
                self.progress.emit(50)
                imagen.save(self.ruta_salida, 'PNG')

            elif self.tipo_conversion == "WEBP a PNG":
                imagen = Image.open(self.ruta_entrada)
                self.progress.emit(50)
                imagen.save(self.ruta_salida, 'PNG')

            self.progress.emit(100)
            self.finished.emit(True, "Conversión completada con éxito")
        except Exception as e:
            self.finished.emit(False, str(e))

#clase para la ventana principal
class ConvertidorArchivos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor de Archivos v2.0 por PolixDev")
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
                background-color: rgba(255, 255, 255, 0.90);
                border-radius: 15px;
                padding: 30px;
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
        """)
        #estilos de la ventana principal
        self.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                font-size: 14px;
                font-weight: bold;
            }   
            QPushButton {
                background-color: rgba(52, 152, 219, 0.85);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            } 
            QPushButton:hover {
                background-color: rgba(41, 128, 185, 0.9);
            } 
            QPushButton:pressed {
                background-color: rgba(37, 115, 167, 0.95);
            }
            QComboBox {
                padding: 8px;
                border: 2px solid rgba(189, 195, 199, 0.6);
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.7);
                min-width: 200px;
                font-weight: bold;
            }
            QComboBox:drop-down {
                border: none;
            }
            QComboBox:down-arrow {
                background-color: rgba(52, 152, 219, 0.85);
            }
            QComboBox QAbstractItemView {
                background-color: rgba(255, 255, 255, 0.9);
                selection-background-color: rgba(52, 152, 219, 0.85);
            }
            QProgressBar {
                border: 2px solid rgba(189, 195, 199, 0.6);
                border-radius: 5px;
                text-align: center;
                height: 25px;
                background-color: rgba(255, 255, 255, 0.7);
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: rgba(46, 204, 113, 0.85);
                border-radius: 5px;
            }
        """)
        
        self.setup_ui()

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
                background-color: rgba(0, 0, 0, 0.1);
                padding: 8px;
                border-radius: 5px;
                color: #1a1a1a;
                font-weight: bold;
            }
        """)
        self.tipo_combo = QComboBox()
        self.tipo_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(0, 0, 0, 0.1);
                padding: 8px;
                border-radius: 5px;
                color: #1a1a1a;
                font-weight: bold;
                border: none;
            }
            QComboBox:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                background-color: rgba(0, 0, 0, 0.3);
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        self.tipo_combo.addItems([
            "Seleccione tipo de conversión",
            "Excel a CSV",
            "Word a PDF",
            "JPG a PDF",
            "PNG a PDF",
            "JPG a PNG",
            "WEBP a PNG"
        ])
        tipo_layout.addWidget(tipo_label)
        tipo_layout.addWidget(self.tipo_combo)
        contenedor_layout.addLayout(tipo_layout)

        # Archivo de entrada
        entrada_layout = QHBoxLayout()
        self.entrada_label = QLabel("Archivo no seleccionado")
        self.entrada_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.1);
                padding: 8px;
                border-radius: 5px;
                color: #1a1a1a;
                font-weight: bold;
            }
        """)
        entrada_btn = QPushButton("Seleccionar archivo")
        entrada_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.1);
                padding: 8px;
                border-radius: 5px;
                color: #1a1a1a;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        entrada_btn.clicked.connect(self.seleccionar_entrada)
        entrada_layout.addWidget(self.entrada_label)
        entrada_layout.addWidget(entrada_btn)
        contenedor_layout.addLayout(entrada_layout)

        # Archivo de salida
        salida_layout = QHBoxLayout()
        self.salida_label = QLabel("Ubicación no seleccionada")
        self.salida_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.1);
                padding: 8px;
                border-radius: 5px;
                color: #1a1a1a;
                font-weight: bold;
            }
        """)
        salida_btn = QPushButton("Seleccionar destino")
        salida_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.1);
                padding: 8px;
                border-radius: 5px;
                color: #1a1a1a;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        salida_btn.clicked.connect(self.seleccionar_salida)
        salida_layout.addWidget(self.salida_label)
        salida_layout.addWidget(salida_btn)
        contenedor_layout.addLayout(salida_layout)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        contenedor_layout.addWidget(self.progress_bar)

        # Botón convertir
        self.convertir_btn = QPushButton("Convertir")
        self.convertir_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        self.convertir_btn.clicked.connect(self.iniciar_conversion)
        contenedor_layout.addWidget(self.convertir_btn)

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

#metodo para seleccionar el archivo de salida
    def seleccionar_salida(self):
        extension = self.obtener_extension_salida()
        if not extension:
            QMessageBox.warning(self, "Advertencia", "Seleccione primero el tipo de conversión")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Guardar como", "", f"Archivo (*{extension})")
        if filename:
            self.ruta_salida = filename
            self.salida_label.setText(os.path.basename(filename))

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
        return ""

#metodo para obtener la extension de salida
    def obtener_extension_salida(self):
        tipo = self.tipo_combo.currentText()
        if tipo == "Excel a CSV":
            return ".csv"
        elif tipo in ["Word a PDF", "JPG a PDF", "PNG a PDF"]:
            return ".pdf"
        elif tipo in ["JPG a PNG", "WEBP a PNG"]:
            return ".png"
        return ""

#metodo para iniciar la conversion de archivos
    def iniciar_conversion(self):
        if not self.validar_campos():
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
                self.estado_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #27ae60;")
                QMessageBox.information(self, "Éxito", mensaje)
            else:
                self.estado_label.setText("Error en la conversión")
                self.estado_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #e74c3c;")
                QMessageBox.critical(self, "Error", f"Error durante la conversión: {mensaje}")
        except Exception as e:
            print(f"Error en conversion_terminada: {str(e)}")

#metodo para validar los campos
    def validar_campos(self):
        if self.tipo_combo.currentText() == "Seleccione tipo de conversión":
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un tipo de conversión")
            return False
        if not self.ruta_entrada:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un archivo de entrada")
            return False
        if not self.ruta_salida:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione la ubicación de salida")
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
#fin 