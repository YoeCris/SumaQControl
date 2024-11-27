# pantalla_grabar.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSizePolicy, QSpacerItem, QFormLayout, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pandas as pd

class PantallaGrabar(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # Almacenar datos
        self.cursos = []  # Lista para los cursos agregados
        self.alumnos = []  # Lista para los alumnos agregados
        self.notas_inputs = []  # Lista para almacenar referencias a los campos de notas
        self.contador_alumnos = 1  # Comienza en 1

        # Crear la interfaz
        self.init_ui()

    def init_ui(self):
        pantalla = self
        layout = QVBoxLayout(self)

        # Sección de cursos
        self.curso_layout = QVBoxLayout()
        self.curso_layout.setAlignment(Qt.AlignTop)

        self.curso_label = QLabel("CURSOS", self)
        self.curso_label.setFixedHeight(70)
        self.curso_label.setStyleSheet("font-size: 40px; color: #0a5ca3; font-weight: bold; padding: 5px")
        self.curso_label.setAlignment(Qt.AlignCenter)
        self.curso_layout.addWidget(self.curso_label)

        curso_input_layout = QHBoxLayout()
        self.curso_input = QLineEdit(self)
        self.curso_input.setPlaceholderText("Ingrese el nombre del curso")
        self.curso_input.setMinimumHeight(30)
        self.curso_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.curso_input.setStyleSheet("""
            QLineEdit {
                font-size: 25px;
                border: 3px solid #2088d8;
                border-radius: 5px;
                padding: 5px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #20add8;
            }
        """)
        curso_input_layout.addWidget(self.curso_input)

        # Botón para agregar curso
        self.boton_agregar_curso = QPushButton("+", self)
        self.boton_agregar_curso.setFixedSize(50, 50)
        self.boton_agregar_curso.setStyleSheet("font-size: 40px; background-color: #2088d8; font-weight: bold; color: white; border-radius: 10px; padding: 1px")
        self.boton_agregar_curso.clicked.connect(self.agregar_curso_gui)
        curso_input_layout.addWidget(self.boton_agregar_curso)

        self.curso_layout.addLayout(curso_input_layout)

        self.cursos_agregados_layout = QVBoxLayout()
        self.cursos_agregados_layout.setAlignment(Qt.AlignTop)
        self.curso_layout.addLayout(self.cursos_agregados_layout)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.curso_layout.addItem(spacer)

        # Botón Siguiente
        self.boton_siguiente = QPushButton("Siguiente", self)
        self.boton_siguiente.setStyleSheet("background-color: #2088d8; font-weight: bold; font-size: 25px; color: white; padding: 10px;")
        self.boton_siguiente.clicked.connect(self.habilitar_alumnos)
        self.boton_siguiente.setEnabled(False)

        self.curso_layout.addWidget(self.boton_siguiente)

        cursos_frame = QWidget()
        cursos_frame.setLayout(self.curso_layout)
        cursos_frame.setStyleSheet("border: 3px solid #2088d8; padding: 15px; border-radius: 10px;")
        cursos_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Sección de alumnos
        self.alumnos_layout = QVBoxLayout()
        self.alumnos_frame = QWidget()
        self.alumnos_frame.setLayout(self.alumnos_layout)
        self.alumnos_frame.setStyleSheet("border: 3px solid #20add8; padding: 15px; border-radius: 10px;")
        self.alumnos_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Creamos y configuramos el título antes de deshabilitar el frame
        alumno_label = QLabel("ALUMNOS", self)
        alumno_label.setFixedHeight(70)
        alumno_label.setStyleSheet("font-size: 40px; color: #007faf; font-weight: bold; padding: 5px")
        alumno_label.setAlignment(Qt.AlignCenter)
        self.alumnos_layout.addWidget(alumno_label)

        # Crear y agregar el contador de alumnos debajo del título
        self.contador_label = QLabel(f"ALUMNO Nº: {self.contador_alumnos}", self)
        self.contador_label.setFixedHeight(50)
        self.contador_label.setStyleSheet("font-size: 30px; color: #007faf; font-weight: bold; padding: 5px")
        self.contador_label.setAlignment(Qt.AlignCenter)
        self.alumnos_layout.addWidget(self.contador_label)

        # Ahora deshabilitamos el frame de alumnos para que los demás widgets estén deshabilitados
        self.alumnos_frame.setDisabled(True)

        # Iniciamos el formulario
        self.alumno_form_layout = QFormLayout()
        self.alumno_apellido = QLineEdit(self)
        self.alumno_apellido.setPlaceholderText("Apellidos")
        self.alumno_apellido.returnPressed.connect(self.foco_alumno_nombre)
        self.alumno_apellido.setStyleSheet("""
            QLineEdit {
                font-size: 35px;
                border: 3px solid #20add8;
                border-radius: 10px;
                padding: 1px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #2088d8;
            }
        """)
        self.alumno_nombre = QLineEdit(self)
        self.alumno_nombre.setPlaceholderText("Nombres")
        self.alumno_nombre.returnPressed.connect(self.foco_nota_curso_0)
        self.alumno_nombre.setStyleSheet("""
            QLineEdit {
                font-size: 35px;
                border: 3px solid #20add8;
                border-radius: 10px;
                padding: 1px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #2088d8;
            }
        """)

        self.alumno_form_layout.addRow("Apellidos:", self.alumno_apellido)
        self.alumno_form_layout.addRow("Nombres:", self.alumno_nombre)
        for i in range(self.alumno_form_layout.rowCount()):
            item_label = self.alumno_form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if isinstance(item_label, QLabel):
                item_label.setStyleSheet("""
                    QLabel {
                        font-size: 20px;
                        font-weight: bold; 
                        padding: 1px;
                    }
                """)

        self.alumnos_layout.addLayout(self.alumno_form_layout)

        # Campos de notas para los cursos
        self.notas_layout = QVBoxLayout()
        # Se generarán después de agregar los cursos

        # Configuración de los botones
        botones_layout = QHBoxLayout()

        self.boton_guardar = QPushButton("Guardar Registros", self)
        self.boton_guardar.setStyleSheet("background-color: #20add8; font-weight: bold; font-size: 25px; color: white; padding: 10px;")
        self.boton_guardar.setEnabled(False)
        self.boton_guardar.clicked.connect(self.guardar_alumnos_gui)
        botones_layout.addWidget(self.boton_guardar)

        # Botón para agregar alumno
        self.boton_agregar_alumno = QPushButton("+", self)
        self.boton_agregar_alumno.setFixedSize(60, 60)
        self.boton_agregar_alumno.setStyleSheet("background-color: #20add8; font-weight: bold; font-size: 50px; color: white; padding: 1px;")
        self.boton_agregar_alumno.clicked.connect(self.agregar_alumno_gui)
        # Añadimos el botón "+" al layout de botones, al lado del botón "Guardar Registros"
        botones_layout.addWidget(self.boton_agregar_alumno)
        # En el constructor o en la función pantalla_grabar, después de crear el botón
        self.boton_agregar_alumno.setDefault(True)

        # Añadimos el layout de botones al layout principal de alumnos
        self.alumnos_layout.addLayout(botones_layout)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(cursos_frame)
        horizontal_layout.addWidget(self.alumnos_frame)
        horizontal_layout.setSpacing(10)

        layout.addLayout(horizontal_layout)

        # Mantener el botón "Atrás" en rojo
        boton_atras = QPushButton("Atrás", self)
        boton_atras.setFixedHeight(40)
        boton_atras.setStyleSheet("""
                    QPushButton {
                        background-color: #E53935;
                        color: white;
                        font-size: 22px;
                        font-weight: bold;
                        border-radius: 10px;
                        padding: 1px;
                    }
                    QPushButton:hover {
                        background-color: #fc0606;
                    }
                """)
        boton_atras.clicked.connect(self.main_window.ir_a_atras)

        layout.addWidget(boton_atras)

    #---------------------------------#
    # Funciones del widget de cursos
    #---------------------------------#

    def agregar_curso_gui(self):
        """Función para agregar un curso"""
        nuevo_curso = self.curso_input.text()
        if nuevo_curso:
            self.cursos.append(nuevo_curso)
            self.curso_input.clear()
            self.crear_curso_widget(nuevo_curso)
            self.boton_siguiente.setEnabled(True)
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un curso válido.")

    def crear_curso_widget(self, nombre_curso):
        """Crear un widget para mostrar el curso agregado"""
        curso_label = QLabel(nombre_curso, self)
        curso_label.setStyleSheet("font-size: 25px; font-weight: bold; color: #333; padding: 1px; border: 3px solid #2088d8; border-radius: 5px;")
        curso_label.setFixedHeight(40)
        curso_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        index_boton_siguiente = self.curso_layout.indexOf(self.boton_siguiente)
        self.curso_layout.insertWidget(index_boton_siguiente, curso_label)

    def habilitar_alumnos(self):
        """Habilitar la sección de alumnos después de agregar cursos"""
        self.curso_input.setDisabled(True)
        self.boton_agregar_curso.setDisabled(True)
        self.boton_siguiente.setDisabled(True)
        self.alumnos_frame.setDisabled(False)
        self.notas_layout = self.generar_campos_notas()
        self.alumnos_layout.insertLayout(self.alumnos_layout.count() - 1, self.notas_layout)
        self.boton_guardar.setEnabled(True)

    #---------------------------------#
    # Funciones del widget de alumnos
    #---------------------------------#

    def generar_campos_notas(self):
        """Generar los campos de notas para cada curso"""
        self.notas_inputs = []
        notas_layout = QVBoxLayout()

        for index, curso in enumerate(self.cursos):
            curso_nota_layout = QHBoxLayout()
            nota_label = QLabel(f"Nota de {curso}:", self)
            nota_label.setStyleSheet("font-size: 25px; margin-right: 10px; padding: 1px;")
            nota_input = QLineEdit(self)
            nota_input.setFixedSize(100, 55)
            nota_input.setStyleSheet("font-size: 25px; margin-right: 10px; padding: 1px;")
            # Conectamos la señal returnPressed al método correspondiente
            if index < len(self.cursos) - 1:
                # Si no es el último campo, enfocar al siguiente campo de nota
                nota_input.returnPressed.connect(lambda idx=index+1: self.notas_inputs[idx].setFocus())
            else:
                # Si es el último campo, enfocar al botón de agregar alumno
                nota_input.returnPressed.connect(self.foco_boton_agregar_alumno)
            self.notas_inputs.append(nota_input)
            curso_nota_layout.addWidget(nota_label)
            curso_nota_layout.addWidget(nota_input)
            notas_layout.addLayout(curso_nota_layout)

        return notas_layout

    def foco_alumno_nombre(self):
        """Función para enfocar el campo "Nombres" después de "Apellidos"."""
        self.alumno_nombre.setFocus()

    def foco_nota_curso_0(self):
        """Función para enfocar el primer campo de notas después de "Nombres"."""
        if self.notas_inputs:
            self.notas_inputs[0].setFocus()

    def foco_boton_agregar_alumno(self):
        """Función para enfocar el botón de agregar alumno después de la última nota."""
        self.boton_agregar_alumno.setFocus()

    def agregar_alumno_gui(self):
        """Función para agregar un alumno"""
        apellido = self.alumno_apellido.text().strip()
        nombre = self.alumno_nombre.text().strip()

        # Validar que los campos de apellido y nombre no estén vacíos
        if not apellido or not nombre:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos de Apellidos y Nombres.")
            return

        # Recopilar las notas ingresadas y validar que estén entre 0 y 20
        notas = []
        for nota_input in self.notas_inputs:
            try:
                nota = float(nota_input.text().strip())
                if nota < 0 or nota > 20:
                    QMessageBox.warning(self, "Error", "Las notas deben estar entre 0 y 20.")
                    return
                notas.append(nota)
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, ingrese notas válidas.")
                return

        # Agregar el alumno a la lista
        self.alumnos.append({"apellido": apellido, "nombre": nombre, "notas": notas})
        QMessageBox.information(self, "Éxito", f"Alumno {nombre} {apellido} agregado correctamente.")

        # Limpiar los campos después de agregar el alumno
        self.alumno_apellido.clear()
        self.alumno_nombre.clear()
        for nota_input in self.notas_inputs:
            nota_input.clear()

        # Incrementar el contador de alumnos
        self.contador_alumnos += 1

        # Actualizar el texto del contador_label
        self.contador_label.setText(f"ALUMNO NRO: {self.contador_alumnos}")

        # Habilitar el botón "Guardar Alumno" si no estaba habilitado
        self.boton_guardar.setEnabled(True)

    def guardar_alumnos_gui(self):
        """Función para guardar los alumnos en un archivo cuando el usuario lo decida"""
        # Verificar si hay alumnos para guardar
        if not self.alumnos:
            QMessageBox.warning(self, "Error", "No hay alumnos para guardar. Debe agregar al menos un alumno.")
            return

        # Si se cargó un archivo previamente, usamos el mismo
        if hasattr(self, 'archivo_cargado') and hasattr(self, 'df'):
            archivo = self.archivo_cargado
            # Agregar los nuevos alumnos al DataFrame existente
            nuevos_alumnos_df = pd.DataFrame(self.alumnos)
            # Recalcular promedio y desempeño para los nuevos alumnos
            nuevos_alumnos_df['Promedio'] = nuevos_alumnos_df['notas'].apply(lambda notas: round(sum(notas) / len(notas)))
            nuevos_alumnos_df['Desempeño'] = nuevos_alumnos_df['Promedio'].apply(self.calcular_desempeno)
            # Expandir las notas en columnas
            notas_df = pd.DataFrame(nuevos_alumnos_df['notas'].tolist(), columns=self.cursos)
            nuevos_alumnos_df = pd.concat([nuevos_alumnos_df[['apellido', 'nombre']], notas_df, nuevos_alumnos_df[['Promedio', 'Desempeño']]], axis=1)
            nuevos_alumnos_df.columns = ['Apellidos', 'Nombres'] + self.cursos + ['Promedio', 'Desempeño']
            # Concatenar con el DataFrame existente
            self.df = pd.concat([self.df, nuevos_alumnos_df], ignore_index=True)
            # Guardar en el mismo archivo
            self.df.to_csv(archivo, index=False)
            QMessageBox.information(self, "Éxito", f"Alumnos guardados en {archivo}")
        else:
            # Abrir el cuadro de diálogo para seleccionar la ubicación del archivo
            archivo, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Archivos CSV (*.csv)")

            if archivo:
                #si no tiene extencion .csv, lo agrega
                if not archivo.lower().endswith('.csv'):
                    archivo += '.csv'
                # Lógica para guardar los alumnos en un archivo CSV
                with open(archivo, 'w') as file:
                    # Escribir encabezados
                    file.write("Apellidos,Nombres," + ",".join(self.cursos) + ",Promedio,Desempeño\n")

                    # Crear un DataFrame con los alumnos nuevos
                    data = []
                    for alumno in self.alumnos:
                        alumno_dict = {
                            'Apellidos': alumno['apellido'],
                            'Nombres': alumno['nombre'],
                            **dict(zip(self.cursos, alumno['notas'])),
                        }
                        promedio = round(sum(alumno['notas']) / len(alumno['notas']))
                        alumno_dict['Promedio'] = promedio
                        alumno_dict['Desempeño'] = self.calcular_desempeno(promedio)
                        data.append(alumno_dict)
                    nuevos_alumnos_df = pd.DataFrame(data)
                    # Guardar en el archivo CSV
                    nuevos_alumnos_df.to_csv(archivo, index=False)
                QMessageBox.information(self, "Éxito", f"Alumnos guardados en {archivo}")
        # Limpiar la lista de alumnos después de guardar
        self.alumnos.clear()
        self.boton_guardar.setEnabled(False)
        self.volver_al_menu_principal()


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

    def volver_al_menu_principal(self):
        """Función para volver al menú principal y limpiar la interfaz sin afectar el programa"""
        # Llamamos a resetear_pantalla_grabar para limpiar la pantalla de Grabar
        self.resetear_pantalla_grabar()

        # Volver al menú principal
        self.main_window.ir_a_atras()

    def resetear_pantalla_grabar(self):
        """Función para restablecer la pantalla de Grabar a su estado inicial"""
        # Limpiar los datos almacenados
        self.cursos.clear()
        self.alumnos.clear()
        self.notas_inputs.clear()
        self.contador_alumnos = 1  # Reiniciar el contador de alumnos

        # Restablecer los widgets de la sección de Cursos
        self.curso_input.setDisabled(False)
        self.curso_input.clear()
        self.boton_agregar_curso.setDisabled(False)
        self.boton_siguiente.setDisabled(True)

        # Limpiar la lista de cursos mostrados en la interfaz
        while self.cursos_agregados_layout.count():
            widget = self.cursos_agregados_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Restablecer los widgets de la sección de Alumnos
        self.alumnos_frame.setDisabled(True)

        # Limpiar los campos de entrada de alumnos
        self.alumno_apellido.clear()
        self.alumno_nombre.clear()

        # Limpiar los campos de notas si existen
        if hasattr(self, 'notas_layout'):
            for i in reversed(range(self.notas_layout.count())):
                item = self.notas_layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
            # Eliminar el layout de notas
            self.alumnos_layout.removeItem(self.notas_layout)
            del self.notas_layout

        # Actualizar el contador de alumnos en la interfaz
        self.contador_label.setText(f"ALUMNO NRO: {self.contador_alumnos}")

        # Deshabilitar el botón "Guardar Registros"
        self.boton_guardar.setEnabled(False)

    def configurar_pantalla_grabar_para_agregar(self):
        """Configura la pantalla de grabar para agregar alumnos a un conjunto existente"""
        # Ocultar o deshabilitar la sección de Cursos
        self.curso_input.setDisabled(True)
        self.boton_agregar_curso.setDisabled(True)
        self.boton_siguiente.setDisabled(True)

        # Limpiar cualquier curso mostrado previamente
        while self.cursos_agregados_layout.count():
            widget = self.cursos_agregados_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Mostrar los cursos existentes en la interfaz
        for curso in self.cursos:
            self.crear_curso_widget(curso)

        # Habilitar la sección de Alumnos
        self.alumnos_frame.setDisabled(False)

        # Actualizar el contador de alumnos en la interfaz
        self.contador_label.setText(f"ALUMNO NRO: {self.contador_alumnos}")

        # Generar los campos de notas para los cursos cargados
        if hasattr(self, 'notas_layout'):
            for i in reversed(range(self.notas_layout.count())):
                item = self.notas_layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        self.notas_layout = self.generar_campos_notas()
        # Reemplazar el layout de notas en la interfaz
        self.alumnos_layout.insertLayout(self.alumnos_layout.count() - 1, self.notas_layout)

        # Asegurarnos de que el botón "Guardar Registros" esté habilitado
        self.boton_guardar.setEnabled(True)
