import sys 
from Controlador import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit, QTableWidgetItem, QPushButton, QTableWidget, QFileDialog, QInputDialog 
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt


class ventanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("login.ui",self)
        self.Controller = controlador()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ventananewuser = newuser(self)
        self.ventanaedituser = edituser(self)
        self.setup()

    def setup(self):
        regex = r'^[a-zA-Z0-9]+$'
        validator = QRegExpValidator(QRegExp(regex))
        self.username.setValidator(validator)
        self.password.setValidator(validator)
        self.minimizar.clicked.connect(self.minimizator)
        self.exit.clicked.connect(self.salir)  
        self.ingresar.clicked.connect(self.login)
        self.nuevo.clicked.connect(self.newuser)
        self.editar.clicked.connect(self.edituser)
        self.password.setEchoMode(QLineEdit.Password)

    def minimizator(self):
        self.showMinimized()     
        
    def salir(self):
        QApplication.quit()  

    def login(self):
        username = self.username.text()
        password = self.password.text()
        existe = self.Controller.ingresoCont(username, password)
        if existe:
            self.vetView = programa()
            self.vetView.show()
            self.close()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('No existe un usuario con los \ndatos proporcionados')
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos()
            msgBox.exec()
    
    def limpiar_campos(self):
        self.username.setText("")
        self.password.setText("")
        
    def newuser(self):
        self.limpiar_campos()
        self.hide()
        self.ventananewuser.show()
        
    def edituser(self):
        self.limpiar_campos()
        self.hide()
        self.ventanaedituser.show()
           
    # Metodos de implementación de eventos de ratón, dado que la ventana es personalizada
    def mousePressEvent(self, event): # Inicia el arrastre
        if event.buttons() == Qt.LeftButton:
            self.dragging = True # Se indica que está en modo de arrastre
            self.offset = event.pos() # Guardo la posición

    def mouseReleaseEvent(self, event): # Termina el arrastre.
        if event.button() == Qt.LeftButton:
            self.dragging = False # Arraste terminado 
            
    def mouseMoveEvent(self, event): # Calcula y realiza el movimiento del widget durante el arrastre.
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset)) 
                # Mueve el widget a la nueva posición calculada en función del 
                # desplazamiento del cursor desde el momento en que se inició el arrastre.
        except:
            pass
      
class newuser(QDialog):
    def __init__(self, ventana1):
        super().__init__()
        loadUi("newuser.ui",self)
        self.ventana1 = ventana1
        self.Controller = controlador()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setup()

    def setup(self):
        regex = r'^[a-zA-Z0-9]+$'
        validator = QRegExpValidator(QRegExp(regex))
        self.username.setValidator(validator)
        self.password.setValidator(validator)
        self.minimizar.clicked.connect(self.minimizator)
        self.exit.clicked.connect(self.salir)  
        self.guardar.clicked.connect(self.anadir)
        self.cancelar.clicked.connect(self.volver)
        self.password.setEchoMode(QLineEdit.Password)
        self.password_2.setEchoMode(QLineEdit.Password)
        
    def minimizator(self):
        self.showMinimized()
        
    def salir(self):
        QApplication.quit()  
  
    def anadir(self):
        try:
            self.guardar.clicked.disconnect()
        except TypeError:
            pass
        self.guardar.clicked.connect(self.ok)
    
    def ok(self):
        username = self.username.text()
        password = self.password.text()
        password_2 = self.password_2.text()
        if not username or not password or not password_2:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        if password == password_2:
            bool = self.Controller.nuevoUsuarioCont(username, password)
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Usuario ingresado exitosamente')
                msgBox.setWindowTitle('Usuario ingresado')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos()
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Usuario existente')
                msgBox.setWindowTitle('Ya existe un usuario con el nombre diligenciado. \nIngrese uno diferente.')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos()
                msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Contraseña')
            msgBox.setWindowTitle('La contraseña no coincide. \nIntente nuevamente.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            
    def limpiar_campos(self):
        self.username.setText("")
        self.password.setText("")
        self.password_2.setText("")
        
    def volver(self):
        self.limpiar_campos()
        self.hide()  # Oculto la ventana actual (Ventana2)
        self.ventana1.show()
        
        # Metodos de implementación de eventos de ratón, dado que la ventana es personalizada
    def mousePressEvent(self, event): # Inicia el arrastre
        if event.buttons() == Qt.LeftButton:
            self.dragging = True # Se indica que está en modo de arrastre
            self.offset = event.pos() # Guardo la posición

    def mouseReleaseEvent(self, event): # Termina el arrastre.
        if event.button() == Qt.LeftButton:
            self.dragging = False # Arraste terminado 
            
    def mouseMoveEvent(self, event): # Calcula y realiza el movimiento del widget durante el arrastre.
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset)) 
                # Mueve el widget a la nueva posición calculada en función del 
                # desplazamiento del cursor desde el momento en que se inició el arrastre.
        except:
            pass
    
class edituser(QDialog):
    def __init__(self, ventana1):
        super().__init__()
        loadUi("modificar.ui",self)
        self.ventana1 = ventana1
        self.Controller = controlador()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ingreso.show()
        self.cambio.hide()
        self.setup()

    def setup(self):
        regex = r'^[a-zA-Z0-9]+$'
        validator = QRegExpValidator(QRegExp(regex))
        self.username.setValidator(validator)
        self.password.setValidator(validator)
        self.minimizar.clicked.connect(self.minimizator)
        self.exit.clicked.connect(self.salir)  
        self.ingresar.clicked.connect(self.login)
        self.cancelar.clicked.connect(self.volver)
        self.cancelar_2.clicked.connect(self.volver)
        self.ingresar_2.clicked.connect(self.ok)
        self.password.setEchoMode(QLineEdit.Password)
        self.password_1.setEchoMode(QLineEdit.Password)
        self.password_2.setEchoMode(QLineEdit.Password)
        
    def minimizator(self):
        self.showMinimized()
        
    def salir(self):
        QApplication.quit()  

    def desconect(self):
        try:
            self.ingresar.clicked.disconnect()
        except TypeError:
            pass
        self.ingresar.clicked.connect(self.login)
           
    def cambiargrupo2(self):
        self.ingreso.hide()
        self.cambio.show()

    def volver(self):
        self.limpiar_campos_ingreso()
        self.limpiar_campos_nuevo()
        self.cambiargrupo1()
        self.hide()  # Oculto la ventana actual (Ventana2)
        self.ventana1.show()
    
    def login(self):
        username = self.username.text()
        password = self.password.text()
        existe = self.Controller.ingresoCont(username, password)
        if existe:
            self.cambiargrupo2()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('No existe un usuario con los \ndatos proporcionados')
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
    
    def limpiar_campos_ingreso(self):
        self.username.setText("")
        self.password.setText("")
    
    def ok(self):
        usernameviejo = self.username.text()
        passwordnuevo = self.password.text()
        username = self.username_1.text()
        password_1 = self.password_1.text()
        password_2 = self.password_2.text()
        if not username or not password_1 or not password_2:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_nuevo()
            msgBox.exec()
            return
        if password_1 == password_2:
            bool = self.Controller.modificarUsuarioCont(usernameviejo, passwordnuevo, username, password_1)
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Cambios guardados exitosamente')
                msgBox.setWindowTitle('Cambios guardados ingresado exitosamente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.cambiargrupo1()
                self.volver()
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Usuario existente')
                msgBox.setWindowTitle('Ya existe un usuario con el nombre diligenciado. \nIngrese uno diferente.')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_nuevo()
                msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Contraseña')
            msgBox.setWindowTitle('La contraseña no coincide. \nIntente nuevamente.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_nuevo()
            msgBox.exec()
    
    def limpiar_campos_nuevo(self):
        self.username_1.setText("")
        self.password_1.setText("")
        self.password_2.setText("")
    
    def cambiargrupo1(self):
        self.cambio.hide()
        self.ingreso.show()
        

        
        # Metodos de implementación de eventos de ratón, dado que la ventana es personalizada
    def mousePressEvent(self, event): # Inicia el arrastre
        if event.buttons() == Qt.LeftButton:
            self.dragging = True # Se indica que está en modo de arrastre
            self.offset = event.pos() # Guardo la posición

    def mouseReleaseEvent(self, event): # Termina el arrastre.
        if event.button() == Qt.LeftButton:
            self.dragging = False # Arraste terminado 
            
    def mouseMoveEvent(self, event): # Calcula y realiza el movimiento del widget durante el arrastre.
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset)) 
                # Mueve el widget a la nueva posición calculada en función del 
                # desplazamiento del cursor desde el momento en que se inició el arrastre.
        except:
            pass

class programa(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("programa.ui", self)
        self.Controller = controlador()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.patientTable = self.findChild(QTableWidget, "patientTable")
        self.setup()

    def setup(self):
        self.minimizar_2.clicked.connect(self.minimizator)
        self.exit_2.clicked.connect(self.salir)
        self.pacientes.clicked.connect(self.holapac)
        self.medicos.clicked.connect(self.holamed)
        self.hola()

    def minimizator(self):
        self.showMinimized()
        
    def salir(self):
        QApplication.quit()
        
    def hola(self):
        self.base.setCurrentIndex(0)     
    
    def holapac(self):
        self.newpac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(0))
        self.editpac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(1))
        self.erasepac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(2))
        self.estudiospac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(3))
        self.pacientes_2.currentChanged.connect(self.update_widgets)
        
    def update_widgets(self, index):
        if index == 0:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.namepac.setValidator(validator)
            self.lastnamepac.setValidator(validator)
            self.age.setValidator(QIntValidator())
            self.idpac.setValidator(validator)
            self.addpac.clicked.connect(self.anadir)
            self.cancelpac.clicked.connect(self.volver)
        if index == 1:
            pass
        if index == 2:
            pass
        if index == 3:
            pass

    def anadir(self):
        try:
            self.addpac.clicked.disconnect()
        except TypeError:
            pass
        self.addpac.clicked.connect(self.ok)

# Aquí se debe ver el botón ese pero no lo he puesto
    def ok(self):
        namepac = self.namepac.text()
        lastnamepac = self.lastnamepac.text()
        agepac = self.agepac.text()
        idpac = self.idpac.text()
        if not namepac or not lastnamepac or not agepac or not idpac:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        bool = self.Controller.nuevopac(idpac)
        if bool:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Usuario ingresado exitosamente')
            msgBox.setWindowTitle('Usuario ingresado')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos()
            msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Usuario existente')
            msgBox.setWindowTitle('Ya existe un usuario con el nombre diligenciado. \nIngrese uno diferente.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos()
            msgBox.exec()
        
    def limpiar_campos(self):
        self.namepac.setText("")
        self.lastnamepac.setText("")
        self.agepac.setText("")
        self.idpac.setText("")

    def volver(self):
        self.limpiar_campos()
        self.edicionespac.setCurrentIndex(0)
        


        
    def holamed(self):
        self.base.setCurrentIndex(2)
        self.newmed.clicked.connect(self.nuevopac)
        self.editmed.clicked.connect(self.editarmed)
        self.erasemed.clicked.connect(self.borrarmed)
        
        
    
        
        
        
        
        
        
        
        
        
    def anadir(self):
        self.stackedWidget.setCurrentIndex(1)
        self.age.setValidator(QIntValidator())
        try:
            self.agregar.clicked.disconnect()
        except TypeError:
            pass
        self.agregar.clicked.connect(self.guardar)
        
    def guardar(self):
        nombre = self.name.text().upper()
        apellido = self.lastname.text().upper()
        edad = self.age.text()
        texto = self.id.text()
        identificacion = ''.join(c.upper() if c.isalpha() else c for c in texto)
        # Recorro la cada caracter del texto con isalpha(), si es letra lo vuelve
        # mayúscula, sino lo deja tal cual. Uno todos los caracteres y los guardo en 
        # una variable.
        
        if not nombre or not apellido or not edad or not identificacion:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return
        
        bool = self.Controller.ingresarPacCont(nombre, apellido, edad , identificacion)
        if bool:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('¡Listo!')
            msgBox.setWindowTitle('Paciente ingresado')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos()
            msgBox.exec()
            self.hola()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('No es posible almacenar dos veces el mismo paciente')
            msgBox.setWindowTitle('Paciente ya existe')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            self.hola()
        
    def borrar(self):
        self.stackedWidget.setCurrentIndex(2)
        self.paciente_buscar.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        try:
            self.busca.clicked.disconnect()
        except TypeError:
            pass
        self.busca.clicked.connect(self.buscar_paciente)

    def limpiar_campos(self):
        self.name.setText("")
        self.lastname.setText("")
        self.age.setText("")
        self.id.setText("")
    
    # Metodos de implementación de eventos de ratón, dado que la ventana es personalizada

    def mousePressEvent(self, event): # Inicia el arrastre
        if event.buttons() == Qt.LeftButton:
            self.dragging = True # Se indica que está en modo de arrastre
            self.offset = event.pos() # Guardo la posición

    def mouseReleaseEvent(self, event): # Termina el arrastre.
        if event.button() == Qt.LeftButton:
            self.dragging = False # Arraste terminado 
            
    def mouseMoveEvent(self, event): # Calcula y realiza el movimiento del widget durante el arrastre.
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset)) 
                # Mueve el widget a la nueva posición calculada en función del 
                # desplazamiento del cursor desde el momento en que se inició el arrastre.
        except:
            pass

    def buscar_paciente(self):
        self.patientTable.setRowCount(0)
        name = self.paciente_buscar.text().strip().upper()
        search_results = self.Controller.listaPacCont(name) if name else self.Controller.listaPacCont("")
        
        if not search_results:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('¡No hubo coincidencias!')
            msgBox.setWindowTitle('Error')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            self.mostrar_resultados(search_results)

    def mostrar_resultados(self, resultados):
        # self.patientTable.setRowCount(0)
        for paciente in resultados:
            rowPosition = self.patientTable.rowCount()
            self.patientTable.insertRow(rowPosition)
            self.patientTable.setItem(rowPosition, 0, QTableWidgetItem(paciente[0]))  # Nombre
            self.patientTable.setItem(rowPosition, 1, QTableWidgetItem(paciente[1]))  # Apellido
            self.patientTable.setItem(rowPosition, 2, QTableWidgetItem(str(paciente[2])))  # Edad
            self.patientTable.setItem(rowPosition, 3, QTableWidgetItem(paciente[3]))  # Identificación

            btnEliminar = QPushButton("Eliminar")
            btnEliminar.clicked.connect(lambda _, r=rowPosition, id=paciente[3]: self.eliminar_paciente(r, id))
            self.patientTable.setCellWidget(rowPosition, 4, btnEliminar)

    def eliminar_paciente(self, row, identificacion):
        self.Controller.eliminarPacCont(identificacion)
        self.patientTable.removeRow(row)
        
              
#############################################################################################
    
    def cargar_mat(self):
        ruta, _ = QFileDialog.getOpenFileName(self, 'Cargar archivo MAT', '', 'Archivos MAT (*.mat)')
        if ruta:
            clave, ok = QInputDialog.getText(self, 'Ingresar clave', 'Ingrese la clave con la que quiere asociar el objeto:')
            if ok and clave:
                try:
                    archivo_id = self.Controller.insertarArchivoCont(clave, 'MAT', ruta)
                    data = self.Controller.cargarMatCont(ruta)
                    for key in data.keys():
                        if key.startswith('__'):
                            continue
                        self.Controller.insertarDatosMatCont(archivo_id, key)
                    QMessageBox.information(self, 'Éxito', f'Archivo MAT {clave} cargado exitosamente.')
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Error al cargar archivo MAT: {e}')

    def cargar_csv(self):
        ruta, _ = QFileDialog.getOpenFileName(self, 'Cargar archivo CSV', '', 'Archivos CSV (*.csv)')
        if ruta:
            clave, ok = QInputDialog.getText(self, 'Ingresar clave', 'Ingrese la clave con la que quiere asociar el objeto:')
            if ok and clave:
                try:
                    archivo_id = self.Controller.insertarArchivoCont(clave, 'CSV', ruta)
                    datos = self.Controller.cargarCsvCont(ruta)
                    for columna in datos.columns:
                        self.Controller.insertarDatosCsvCont(archivo_id, columna)
                    QMessageBox.information(self, 'Éxito', f'Archivo CSV {clave} cargado exitosamente.')
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Error al cargar archivo CSV: {e}')




#############################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = ventanaLogin()
    login.show()
    sys.exit(app.exec_())

