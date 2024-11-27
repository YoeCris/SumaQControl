from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, compatible con PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y almacena el path en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PantallaPrincipal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        pantalla = self

        # Crear un QLabel para la imagen de fondo
        self.fondo = QLabel(pantalla)
        self.fondo.setPixmap(QPixmap(resource_path("appf.png")))
        self.fondo.setScaledContents(True)  # Permitir redimensionamiento
        self.fondo.setGeometry(0, 0, pantalla.width(), pantalla.height())

        # Layout principal
        layout_principal = QVBoxLayout(self)

        # Crear encabezado (logos e información de la universidad)
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)

        # Imagen izquierda (Logo Universidad)
        logo_universidad = QLabel(self)
        pixmap_universidad = QPixmap(resource_path("Logo_UNAP.png"))
        logo_universidad.setPixmap(pixmap_universidad.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_universidad.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(logo_universidad)

        # Texto centrado (Información de la universidad)
        texto_centrado = QVBoxLayout()
        informacion_universidad = QLabel(self)
        informacion_universidad.setText("""
            <p style="font-size: 20px; font-weight: bold; color: #FFFFFF; text-align: center; margin: 0;">
                UNIVERSIDAD NACIONAL DEL ALTIPLANO - PUNO
            </p>
            <p style="font-size: 18px; font-weight: bold; color: #FFFFFF; text-align: center; margin: 0;">
                Facultad de Ingeniería Estadística e Informática
            </p>
            <p style="font-size: 16px; font-weight: bold; color: #FFFFFF; text-align: center; margin: 0;">
                Escuela Profesional de Ingeniería Estadística e Informática
            </p>
        """)
        informacion_universidad.setAlignment(Qt.AlignCenter)
        texto_centrado.addWidget(informacion_universidad)

        # Título principal directamente debajo de la información de la universidad
        titulo = QLabel("Bienvenido a SumaQControl", self)
        titulo.setFont(QFont('Roboto', 24, QFont.Bold))
        titulo.setStyleSheet("color: white; margin: 0;")  # Sin márgenes
        titulo.setAlignment(Qt.AlignCenter)
        texto_centrado.addWidget(titulo)

        header_layout.addLayout(texto_centrado)

        # Imagen derecha (Logo Escuela)
        logo_escuela = QLabel(self)
        pixmap_escuela = QPixmap(resource_path("Logo_FINESI.png"))
        logo_escuela.setPixmap(pixmap_escuela.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_escuela.setAlignment(Qt.AlignRight)
        header_layout.addWidget(logo_escuela)

        # Asegurar que el header_widget tenga un tamaño fijo
        header_widget.setFixedHeight(150)
        layout_principal.addWidget(header_widget)

        # Espaciador para empujar los botones hacia abajo
        layout_principal.addStretch()

        # Botones en la parte inferior
        boton_layout = QHBoxLayout()
        boton_layout.setSpacing(20)
        boton_layout.setContentsMargins(30, 20, 30, 20)

        # Botones con efectos
        boton_grabar = self.crear_boton_con_efectos("Ingreso de datos generales", self.main_window.ir_a_grabar, "#106994", "#286cff", "#2949ff")
        boton_cargar = self.crear_boton_con_efectos("Cargar Registros", self.main_window.ir_a_cargar, "#106994", "#286cff", "#2949ff")
        boton_salir = self.crear_boton_con_efectos("Salir", self.main_window.close, "#106994", "#ff5959", "#fc0606")
        

        # Añadir botones al layout de los botones
        boton_layout.addWidget(boton_grabar)
        boton_layout.addWidget(boton_cargar)
        boton_layout.addWidget(boton_salir)

        # Añadir el layout de botones al layout principal
        layout_principal.addLayout(boton_layout)

        # Ajustar el fondo al tamaño de la ventana
        def redimensionar_fondo(event):
            self.fondo.setGeometry(0, 0, self.width(), self.height())
            super(PantallaPrincipal, self).resizeEvent(event)

        self.resizeEvent = redimensionar_fondo

    def crear_boton_con_efectos(self, texto, accion, color_base, color_hover, color_pressed):
        """Crea un botón con efectos evidentes al pasar el cursor"""
        boton = QPushButton(texto, self)
        boton.setMinimumHeight(50)
        boton.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_base};
                color: #FFFFFF;
                font-size: 20px;
                font-family: Roboto;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
            QPushButton:pressed {{
                background-color: {color_pressed};
            }}
        """)
        boton.clicked.connect(accion)
        return boton
