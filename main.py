# main.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt  # Agrega esta línea
import sys
import pandas as pd

# Importar las pantallas desde sus módulos
from pantalla_principal import PantallaPrincipal
from pantalla_grabar import PantallaGrabar
from pantalla_cargar import PantallaCargar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SumaQControl")
        self.setGeometry(400, 150, 1200, 700)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Almacenar datos
        self.df = pd.DataFrame()

        # Crear las pantallas
        self.pantalla_principal = PantallaPrincipal(self)
        self.stacked_widget.addWidget(self.pantalla_principal)

        # Inicialmente, las pantallas de grabar y cargar no existen
        self.pantalla_grabar_widget = None
        self.pantalla_cargar_widget = None

        # Cambiar a la pantalla principal inicialmente
        self.stacked_widget.setCurrentIndex(0)

    def ir_a_grabar(self):
        """Función para cambiar a la pantalla de grabar"""
        # Si la pantalla de grabar no existe o ha sido eliminada, crearla de nuevo
        if not self.pantalla_grabar_widget:
            self.pantalla_grabar_widget = PantallaGrabar(self)
            self.stacked_widget.addWidget(self.pantalla_grabar_widget)
        # Establecer la pantalla de grabar como la actual
        index = self.stacked_widget.indexOf(self.pantalla_grabar_widget)
        self.stacked_widget.setCurrentIndex(index)

    def ir_a_cargar(self):
        """Función para cambiar a la pantalla de cargar"""
        # Si la pantalla de cargar no existe o ha sido eliminada, crearla de nuevo
        if not self.pantalla_cargar_widget:
            self.pantalla_cargar_widget = PantallaCargar(self)
            self.stacked_widget.addWidget(self.pantalla_cargar_widget)
        # Establecer la pantalla de cargar como la actual
        index = self.stacked_widget.indexOf(self.pantalla_cargar_widget)
        self.stacked_widget.setCurrentIndex(index)

    def ir_a_atras(self):
        """Función para retroceder una pantalla y restablecer el estado si es necesario"""
        current_widget = self.stacked_widget.currentWidget()

        # Si estamos en la pantalla de Grabar
        if self.pantalla_grabar_widget and current_widget == self.pantalla_grabar_widget:
            # Remover la pantalla de Grabar del stacked_widget
            self.stacked_widget.removeWidget(self.pantalla_grabar_widget)
            self.pantalla_grabar_widget.deleteLater()
            self.pantalla_grabar_widget = None
            # Volver a la pantalla principal
            self.stacked_widget.setCurrentIndex(0)
        # Si estamos en la pantalla de Cargar
        elif self.pantalla_cargar_widget and current_widget == self.pantalla_cargar_widget:
            # Remover la pantalla de Cargar del stacked_widget
            self.stacked_widget.removeWidget(self.pantalla_cargar_widget)
            self.pantalla_cargar_widget.deleteLater()
            self.pantalla_cargar_widget = None
            # Limpiar el DataFrame y otros estados si es necesario
            self.df = pd.DataFrame()
            # Volver a la pantalla principal
            self.stacked_widget.setCurrentIndex(0)
        elif self.stacked_widget.currentIndex() > 0:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() - 1)  # Cambia a la pantalla anterior

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())
