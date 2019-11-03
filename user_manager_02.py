from mainUI import *
import sqlite3
from os import getcwd
import sys
from PyQt5 import uic
from PyQt5.QtSql import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QByteArray, QIODevice, QBuffer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel, QPushButton, QFileDialog,
                             QLabel, QLineEdit, QAction, QMessageBox)
from PyQt5.uic.properties import QtGui



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def newBBDD(self):
        miConexion = sqlite3.connect("Usuarios")

        miCursor = miConexion.cursor()

        try:

            miCursor.execute('''
                    CREATE TABLE Usuarios (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOMBRE_USUARIO VARCHAR(50),
                    FOTO BLOB,
                    RFID VARCHAR(20),
                    NUMERO_TRABAJADOR VARCHAR(50),
                    PUESTO VARCHAR(50),
                    EMERGECIA VARCHAR(10),
                    COMENTARIOS VARCHAR(100))
                ''')

            QMessageBox.information(self, "Atencion", "La BBDD a sido creada con exito", QMessageBox.Ok)

        except:

            QMessageBox.information(self, "Atencion", "Ya existe la base de datos", QMessageBox.Ok)

    def crear(self):
        # Obtener el nombre de usuario y la foto
        nombre = " ".join(self.editNombre.text().split()).title()
        foto = self.labelImagen.pixmap()
        numero_trabajador = " ".join(self.editNumero.text())
        tarjeta = " ".join(self.editTrarjeta.text())
        puesto = " ".join(self.editPuesto.text())
        emergencia = " ".join(self.editEmergencia.text())
        # comentarios = " ".join(self.textEdit.text())

        if foto:
            # Convertir la foto al tipo de dato adecuado
            bArray = QByteArray()
            bufer = QBuffer(bArray)
            bufer.open(QIODevice.WriteOnly)
            bufer.close()
            foto.save(bufer, "PNG")
        else:
            bArray = ""

        if nombre and bArray:
            # Establecer conexión con la base de datos
            conexion = sqlite3.connect("DB_USUARIOS.db")
            cursor = conexion.cursor()

            # Crear tabla, si no existe
            cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (NOMBRE TEXT, FOTO BLOB, NUMERO_TRA TEXT, TARJETA TEX, PUESTO TEXT, EMERGENCIA TEXT)")
            conexion.commit()

            # Verificar que el usuario no exista
            if cursor.execute("SELECT * FROM Usuarios WHERE NOMBRE = ?", (nombre,)).fetchone():
                QMessageBox.information(self, "Atencion", "El usuario {} ya existe".format(nombre), QMessageBox.Ok)
            else:
                # Guardar en la base de datos, el nombre de usuario y la foto
                cursor.execute("INSERT INTO Usuarios VALUES (?,?,?,?,?,?)", (nombre, bArray, numero_trabajador, tarjeta, puesto, emergencia))
                conexion.commit()

                self.labelImagen.clear()
                self.editNombre.clear()
                self.editNumero.clear()
                self.editTrarjeta.clear()
                self.editPuesto.clear()
                self.editEmergencia.clear()
                self.textEdit.clear()

                QMessageBox.information(self, "Usuario", "El Usuario se registro con exito", QMessageBox.Ok)

            # Cerrar la conexión con la base de datos
            conexion.close()

            self.editNombre.setFocus()
        else:
            self.editNombre.setFocus()


    def seleccionarImagen(self):
        imagen, extension = QFileDialog.getOpenFileName(self, "Seleccionar imagen", getcwd(),
                                                        "Archivos de imagen (*.png *.jpg)",
                                                        options=QFileDialog.Options())

        if imagen:
            # Adaptar imagen
            pixmapImagen = QPixmap(imagen).scaled(280, 300, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation)

            # Mostrar imagen
            self.labelImagen.setPixmap(pixmapImagen)

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("Administrador de Almacen")
        self.setWindowIcon(QIcon(""))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowMinimizeButtonHint)

        buttonSeleccionar = QPushButton("Seleccionar", self)
        buttonSeleccionar.setToolTip("Seleccionar imagen")
        buttonSeleccionar.setCursor(Qt.PointingHandCursor)
        buttonSeleccionar.setGeometry(30, 500, 280, 25)
        buttonSeleccionar.clicked.connect(self.seleccionarImagen)
        # Llamar función al hacer clic sobre el label

        self.labelImagen.clicked.connect(self.seleccionarImagen)

        # btn = QPushButton("Conectar", self)
        # btn.setToolTip("CrearBBDD")
        # btn.setGeometry(30, 530, 100, 25)
        # btn.clicked.connect(self.newBBDD)

        btn = QPushButton("Crear", self)
        btn.setToolTip("registro")
        btn.setGeometry(30, 530, 100, 25)
        btn.clicked.connect(self.crear)

        btnBus = QPushButton("Buscar", self)
        btnBus.setToolTip("buscar")
        btnBus.setGeometry(131, 530, 100, 25)
        #btnBus.clicked.connect(self.crear)

        btnBus = QPushButton("Eliminar", self)
        btnBus.setToolTip("eliminar")
        btnBus.setGeometry(231, 530, 100, 25)
        # btnBus.clicked.connect(self.crear)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()

    app.exec_()
