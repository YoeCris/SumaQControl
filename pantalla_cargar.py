# pantalla_cargar.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd
from pantalla_grabar import PantallaGrabar


class PantallaCargar(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # DataFrame para almacenar los datos
        self.df = pd.DataFrame()

        # Crear la interfaz
        self.init_ui()

    def init_ui(self):
        pantalla = self
        layout = QVBoxLayout(self)

        # Color de fondo de la pantalla
        self.setStyleSheet("""
            QWidget {
                background-color: #00A5B5;
            }
        """)

        # Botón para cargar el archivo CSV
        boton_cargar_archivo = QPushButton("Cargar Archivo", self)
        boton_cargar_archivo.setMinimumHeight(40)
        boton_cargar_archivo.setStyleSheet("""
            QPushButton {
                background-color: #0e4d67; 
                color: white;
                font-size: 20px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #008bbb; 
            }
        """)
        boton_cargar_archivo.clicked.connect(self.cargar_archivo)
        layout.addWidget(boton_cargar_archivo)

        # Crear la tabla dinámica
        self.tabla_alumnos = QTableWidget(self)
        self.tabla_alumnos.setEditTriggers(QAbstractItemView.AllEditTriggers)  # Permitir edición
        self.tabla_alumnos.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF; /* Blanco */
                border: 2px solid #0c667e; /* Borde teal claro */
                gridline-color: #1D2948; /* Líneas grid teal */
                font-size: 15px;
                color: #0e4d67; /* Teal oscuro */
            }
            QHeaderView::section {
                background-color: #0a93a0; /* Teal 700 */
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #0e4d67; /* Teal 900 */
            }
        """)
        layout.addWidget(self.tabla_alumnos)

        # Conectar la señal de cambio de celda a la función después de crear self.tabla_alumnos
        self.tabla_alumnos.itemChanged.connect(self.actualizar_promedio_desempeno)

        # Botones de acciones (Agregar, Ordenar, Eliminar)
        acciones_layout = QHBoxLayout()

        # Estilo común para los botones de acción
        estilo_botones_accion = """
            QPushButton {
                background-color: #0c667e; 
                color: white;
                font-size: 20px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0a93a0; 
            }
        """

        # Botón para agregar alumno
        boton_agregar = QPushButton("Agregar Alumno", self)
        boton_agregar.setMinimumHeight(40)
        boton_agregar.setStyleSheet(estilo_botones_accion)
        boton_agregar.clicked.connect(self.ir_a_agregar_alumno)
        acciones_layout.addWidget(boton_agregar)

        # Botón para ordenar alumnos
        boton_ordenar = QPushButton("Ordenar", self)
        boton_ordenar.setMinimumHeight(40)
        boton_ordenar.setStyleSheet(estilo_botones_accion)
        boton_ordenar.clicked.connect(self.ordenar_alumnos_por_promedio)
        acciones_layout.addWidget(boton_ordenar)

        # Botón para eliminar alumno
        boton_eliminar = QPushButton("Eliminar Alumno", self)
        boton_eliminar.setMinimumHeight(40)
        boton_eliminar.setStyleSheet(estilo_botones_accion)
        boton_eliminar.clicked.connect(self.eliminar_alumno_gui)
        acciones_layout.addWidget(boton_eliminar)

        # Añadir el layout de los botones de acciones al layout principal
        layout.addLayout(acciones_layout)

        # Crear un layout horizontal para los botones "Guardar Cambios" y "Atrás"
        botones_layout = QHBoxLayout()

        # Botón para guardar cambios
        boton_guardar = QPushButton("Guardar Cambios", self)
        boton_guardar.setMinimumHeight(40)
        boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #0c667e; 
                color: white;
                font-size: 20px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0a93a0; 
            }
        """)
        boton_guardar.clicked.connect(self.guardar_cambios_csv)
        botones_layout.addWidget(boton_guardar)

        # Botón para volver atrás
        boton_atras = QPushButton("Atrás", self)
        boton_atras.setStyleSheet("""
            QPushButton {
                background-color: #E53935; 
                color: #FFFFFF; 
                font-weight: bold;
                border-radius: 10px;
                padding: 5;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #fc0606; 
            }
        """)
        boton_atras.clicked.connect(self.main_window.ir_a_atras)
        botones_layout.addWidget(boton_atras)

        # Añadir el layout horizontal para los botones finales al layout principal
        layout.addLayout(botones_layout)

    #---------------------------------#
    # Funciones de la pantalla cargar
    #---------------------------------#

    def cargar_archivo(self):
        """Función para cargar archivo CSV y mostrarlo en una tabla editable"""
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar archivo CSV", "", "Archivos CSV (*.csv)")

        if archivo:
            # Guardamos el nombre del archivo cargado para poder guardar los cambios más tarde
            self.archivo_cargado = archivo

            # Leer el archivo CSV y guardarlo en un DataFrame
            self.df = pd.read_csv(archivo)

            # Mostrar los datos en la tabla
            self.mostrar_alumnos_en_tabla(self.df)
        else:
            QMessageBox.warning(self, "Error", "No se pudo cargar el archivo.")

    def mostrar_alumnos_en_tabla(self, df):
        """Función para mostrar los datos del archivo CSV en la tabla dinámica"""
        self.tabla_alumnos.setRowCount(0)  # Limpiar filas anteriores
        self.tabla_alumnos.setColumnCount(len(df.columns))  # Ajustar el número de columnas
        self.tabla_alumnos.setHorizontalHeaderLabels(df.columns)  # Establecer los encabezados

        # Hacer que las columnas de promedio y desempeño no sean editables
        self.columnas_no_editables = ['Promedio', 'Desempeño']  # Columnas que no se pueden editar

        # Añadir los datos a la tabla
        for row in range(len(df)):
            self.tabla_alumnos.insertRow(row)
            for col, column_name in enumerate(df.columns):
                value = df.iloc[row, col]
                if column_name == 'Promedio':
                    item = QTableWidgetItem(str(df.iloc[row, col]))
                else:
                    item = QTableWidgetItem(str(value))
                if column_name in self.columnas_no_editables:
                    # Deshabilitar la edición en las columnas de promedio y desempeño
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tabla_alumnos.setItem(row, col, item)
        
        # Ajustar el ancho de las columnas al contenido
        self.tabla_alumnos.resizeColumnsToContents()

    def actualizar_promedio_desempeno(self, item):
        """Función para actualizar el promedio y desempeño cuando se editan las notas"""
        # Obtenemos la fila y columna del item modificado
        row = item.row()
        column = item.column()
        column_name = self.tabla_alumnos.horizontalHeaderItem(column).text()

        # Verificamos si la columna editada es una de las notas
        if column_name not in ['Apellidos', 'Nombres', 'Promedio', 'Desempeño']:
            try:
                # Intentamos convertir la nota a float
                nueva_nota = float(item.text())
                # Actualizamos el DataFrame
                self.df.at[row, column_name] = nueva_nota
                # Recalculamos el promedio
                notas_columnas = [col for col in self.df.columns if col not in ['Apellidos', 'Nombres', 'Promedio', 'Desempeño']]
                notas = self.df.loc[row, notas_columnas].astype(float)
                promedio = notas.mean()
                promedio = round(promedio)
                self.df.at[row, 'Promedio'] = promedio
                # Recalculamos el desempeño
                desempeno = self.calcular_desempeno(promedio)
                self.df.at[row, 'Desempeño'] = desempeno
                # Actualizamos las celdas en la tabla
                self.tabla_alumnos.blockSignals(True)  # Bloqueamos señales para evitar recursión
                self.tabla_alumnos.setItem(row, self.df.columns.get_loc('Promedio'), QTableWidgetItem(f"{promedio}"))
                self.tabla_alumnos.setItem(row, self.df.columns.get_loc('Desempeño'), QTableWidgetItem(desempeno))
                self.tabla_alumnos.blockSignals(False)  # Desbloqueamos señales
            except ValueError:
                QMessageBox.warning(self, "Error", "Ingrese un valor numérico válido para la nota.")
                # Restauramos el valor anterior en caso de error
                valor_anterior = self.df.at[row, column_name]
                self.tabla_alumnos.blockSignals(True)
                self.tabla_alumnos.setItem(row, column, QTableWidgetItem(str(valor_anterior)))
                self.tabla_alumnos.blockSignals(False)

    def calcular_desempeno(self, promedio):
        """Función auxiliar para clasificar el desempeño basado en el promedio"""
        if promedio <= 7:
            desempeno = "Pésimo"
        elif promedio <= 11:
            desempeno = "Deficiente"
        elif promedio <= 14:
            desempeno = "Regular"
        elif promedio <= 17:
            desempeno = "Bueno"
        else:
            desempeno = "Excelente"
        return desempeno

    def ordenar_alumnos_por_promedio(self):
        """Función para ordenar los alumnos por promedio de mayor a menor"""
        if hasattr(self, 'df') and not self.df.empty:
            # Ordenar el DataFrame por la columna 'Promedio' en orden descendente
            self.df = self.df.sort_values(by='Promedio', ascending=False).reset_index(drop=True)
            # Actualizar la tabla con el DataFrame ordenado
            self.mostrar_alumnos_en_tabla(self.df)
            QMessageBox.information(self, "Éxito", "Alumnos ordenados por promedio de mayor a menor.")
        else:
            QMessageBox.warning(self, "Error", "No hay datos para ordenar. Por favor, cargue un archivo primero.")

    def eliminar_alumno_gui(self):
        """Función para eliminar el alumno seleccionado"""
        fila_seleccionada = self.tabla_alumnos.currentRow()

        if fila_seleccionada >= 0:
            # Confirmar eliminación
            respuesta = QMessageBox.question(self, "Confirmar eliminación", "¿Está seguro de que desea eliminar este alumno?", QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                # Eliminar del DataFrame
                self.df = self.df.drop(self.df.index[fila_seleccionada]).reset_index(drop=True)
                # Actualizar la tabla
                self.mostrar_alumnos_en_tabla(self.df)
                QMessageBox.information(self, "Éxito", "Alumno eliminado correctamente.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un alumno para eliminar.")

    def guardar_cambios_csv(self):
        """Función para guardar los cambios en el mismo archivo CSV"""
        if not hasattr(self, 'archivo_cargado'):
            QMessageBox.warning(self, "Error", "Debe cargar un archivo antes de guardar.")
            return

        try:
            # Guardamos el DataFrame actualizado en el archivo CSV
            self.df.to_csv(self.archivo_cargado, index=False)
            QMessageBox.information(self, "Éxito", "Cambios guardados correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el archivo: {str(e)}")

    def ir_a_agregar_alumno(self):
        """Función para cambiar a la pantalla de grabar y agregar más alumnos al archivo cargado"""
        # Verificar que se haya cargado un archivo y que exista el DataFrame
        if not hasattr(self, 'df') or self.df.empty:
            QMessageBox.warning(self, "Error", "Debe cargar un archivo antes de agregar un alumno.")
            return

        # Obtener la lista de cursos desde las columnas del DataFrame
        # Suponemos que las columnas de cursos están entre 'Nombres' y 'Promedio'
        columnas_cursos = self.df.columns.tolist()
        try:
            indice_inicio = columnas_cursos.index('Nombres') + 1
            indice_fin = columnas_cursos.index('Promedio')
            cursos = columnas_cursos[indice_inicio:indice_fin]
        except ValueError:
            QMessageBox.warning(self, "Error", "El archivo cargado no tiene el formato esperado.")
            return

        # Actualizar el contador de alumnos según los datos existentes
        contador_alumnos = len(self.df) + 1  # Iniciar desde el siguiente alumno

        # Configurar la pantalla de grabar para agregar más alumnos
        self.main_window.pantalla_grabar_widget = PantallaGrabar(self.main_window)
        self.main_window.pantalla_grabar_widget.cursos = cursos
        self.main_window.pantalla_grabar_widget.alumnos = []
        self.main_window.pantalla_grabar_widget.contador_alumnos = contador_alumnos

        # **Asignar archivo_cargado y df a PantallaGrabar**
        self.main_window.pantalla_grabar_widget.archivo_cargado = self.archivo_cargado
        self.main_window.pantalla_grabar_widget.df = self.df

        self.main_window.pantalla_grabar_widget.configurar_pantalla_grabar_para_agregar()

        # Añadir la pantalla de grabar al stacked_widget si no está ya
        if self.main_window.stacked_widget.indexOf(self.main_window.pantalla_grabar_widget) == -1:
            self.main_window.stacked_widget.addWidget(self.main_window.pantalla_grabar_widget)

        # Cambiar a la pantalla de grabar
        index = self.main_window.stacked_widget.indexOf(self.main_window.pantalla_grabar_widget)
        self.main_window.stacked_widget.setCurrentIndex(index)

