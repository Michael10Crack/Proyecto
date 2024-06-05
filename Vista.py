import sys 
import pydicom
import os
from Controlador import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QPixmap
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi



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
        self.Controller.desconectar()
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
        self.Controller.desconectar()
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
        self.Controller.desconectar()
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
        self.nombre_medico = ""
        self.url = ""
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setup()

    def setup(self):
        self.min.clicked.connect(self.minimizator)
        self.out.clicked.connect(self.salir)
        self.pacientes.clicked.connect(self.holapac)
        self.medicos.clicked.connect(self.holamed)
        self.hola()

    def minimizator(self):
        self.showMinimized()
        
    def salir(self):
        self.Controller.desconectar()
        QApplication.quit()
        
    def hola(self):
        self.edicionespac.hide()
        self.base.setCurrentIndex(0)     
    
    def holapac(self):
        self.base.setCurrentIndex(1) 
        self.edicionespac.show()
        self.edicionespac.setCurrentIndex(0)
        self.newpac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(1))
        self.editpac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(2))
        self.erasepac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(3))
        self.estudiospac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(4))
        self.base.currentChanged.connect(self.update_widgets)
        
    def update_widgets(self, index):
        if index == 1:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.namepac.setValidator(validator)
            self.lastnamepac.setValidator(validator)
            self.age.setValidator(QIntValidator())
            self.idpac.setValidator(validator)
            self.addpac.clicked.connect(self.anadirPacNuevo)
            self.cancelpac.clicked.connect(self.volver)
            self.desplegmed.addItems(self.lista_med)
            self.browse.clicked.connect(self.procesar_dicom)
        if index == 2:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.idpac_buscar.setValidator(validator)
            self.buscarpac.clicked.connect(self.busquedapac)
            self.nameedtpac.setValidator(validator)
            self.lastnameedtpac.setValidator(validator)
            self.ageedtpac.setValidator(QIntValidator())
            self.idedtpac.setValidator(validator)
            self.desplegedtmed.setValidator(validator)
            self.addedtpac.clicked.connect(self.anadirPacEdit)
            self.canceledtpac.clicked.connect(self.volver)
            self.desplegedtmed.addItems(self.lista_med)
            self.cargaedtpac.clicked.connect(self.procesar_dicom)
            self.groupBox_10.hide()
            pass
        if index == 3:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.idpac_eliminar.setValidator(validator)
            self.paceliminar.clicked.connect(self.eliminarpac)
        if index == 4:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.idpac_estudio.setValidator(validator)
            self.pacestudio.clicked.connect(self.estudio)

            pass
            # self.browse.clicked.connect(self.procesar_dicom)

    def anadirPacNuevo(self):
        try:
            self.addpac.clicked.disconnect()
        except TypeError:
            pass
        self.addpac.clicked.connect(self.okPacNuevo)

    def anadirPacEdit(self):
        try:
            self.addedtpac.clicked.disconnect()
        except TypeError:
            pass
        self.addedtpac.clicked.connect(self.okPacEdit)

# Aquí se debe ver el botón ese pero no lo he puesto
    # self.browse.clicked.connect(self.procesar_dicom) # ESTE ES EL BOTON DE BUSCAR

    def procesar_dicom(self):
        ruta_carpeta = QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta con archivos DICOM', '')
        if ruta_carpeta:
            archivos_dicom = [os.path.join(ruta_carpeta, file) for file in os.listdir(ruta_carpeta) if file.endswith('.dcm')]
            if archivos_dicom:
                    try:
                        for file in archivos_dicom:
                            dicom_data = pydicom.dcmread(file)                        
                        # Procesar el archivo DICOM
                            manejador_dicom = manejodicom(dicom_data)
                            imagen_procesada = manejador_dicom.apply_modality_lut()
                        self.url = ruta_carpeta
                        self.exito(ruta_carpeta) 
                    except pydicom.errors.InvalidDicomError:
                        # El archivo no es un archivo DICOM válido
                        self.mostrar_advertencia()
                        pass

    def abrir_dicom(self, namepac, lastnamepac, agepac, idpac, medpac, url):
        ruta_carpeta = url
        if ruta_carpeta:
            archivos_dicom = [os.path.join(ruta_carpeta, file) for file in os.listdir(ruta_carpeta) if file.endswith('.dcm')]
            if archivos_dicom:
                    try:
                        for file in archivos_dicom:
                            dicom_data = pydicom.dcmread(file)                        
                        # Procesar el archivo DICOM
                            manejador_dicom = manejodicom(dicom_data)
                            imagen_procesada = manejador_dicom.apply_modality_lut()
                        self.mostrar_imagenes_dicom(imagen_procesada, namepac, lastnamepac, agepac, idpac, medpac)
                    except pydicom.errors.InvalidDicomError:
                        # El archivo no es un archivo DICOM válido
                        pass

    def mostrar_imagenes_dicom(self, imagen_procesada, namepac, lastnamepac, agepac, idpac, medpac):
        ventana = VentanaEmergente(namepac, lastnamepac, agepac, idpac, medpac) #la defino como la clase
        ventana.mostrar_imagen_procesada(imagen_procesada) # 'plotear'
        ventana.exec_() #mostrar la ventana

    def exito(self, ruta_carpeta):
        # Mostrar una ventana emergente con un mensaje de procesamiento exitoso
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(f'Carpeta DICOM seleccionada: {ruta_carpeta}')
        msgBox.setWindowTitle('Información')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def mostrar_advertencia(self):
        # Mostrar una ventana emergente con un mensaje de advertencia
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("La carpeta seleccionada contiene al menos 1 archivo diferente a .dcm.")
        msgBox.setWindowTitle('Advertencia')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        
    def okPacNuevo(self):
        namepac = self.namepac.text().upper()
        lastnamepac = self.lastnamepac.text().upper()
        agepac = self.agepac.text()
        texto = self.idpac.text()
        idpac = ''.join(c.upper() if c.isalpha() else c for c in texto)
        medpac = self.nombre_medico
        url = self.url
        if not namepac or not lastnamepac or not agepac or not idpac or not medpac or not url:
            self.nombre_medico = ""
            self.url = ""
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        bool = self.Controller.ingresarPacCont(namepac, lastnamepac, agepac, idpac, medpac, url)
        if bool:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Usuario ingresado exitosamente')
            msgBox.setWindowTitle('Usuario ingresado')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_PacNuevo()
            self.groupBox_10.hide()
            msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Ya existe un usuario con el ID diligenciado.\nIngrese uno diferente.')
            msgBox.setWindowTitle('Usuario existente')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_PacNuevo()
            msgBox.exec()
        
    def okPacEdit(self):
        nameedtpac = self.nameedtpac.text().upper()
        lastnameedtpac = self.lastnameedtpac.text().upper()
        ageedtpac = self.ageedtpac.text()
        texto = self.idedtpac.text()
        idedtpac = ''.join(c.upper() if c.isalpha() else c for c in texto)
        medpac = self.nombre_medico
        url = self.url
        idpac_buscar = self.idpac_buscar.text()
        if not nameedtpac or not lastnameedtpac or not ageedtpac or not idedtpac or not medpac or not url:
            self.nombre_medico = ""
            self.url = ""
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        bool = self.Controller.editarPacCont(idpac_buscar, idedtpac, nameedtpac, lastnameedtpac, ageedtpac, medpac, url )
        if bool:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Usuario ingresado exitosamente')
            msgBox.setWindowTitle('Usuario ingresado')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_PacEdit()
            self.groupBox_10.hide()
            msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Ya existe un usuario con el ID diligenciado.\nIngrese uno diferente.')
            msgBox.setWindowTitle('Usuario existente')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_PacEdit()
            msgBox.exec()

    def limpiar_campos_PacNuevo(self):
        self.namepac.setText("")
        self.lastnamepac.setText("")
        self.agepac.setText("")
        self.idpac.setText("")
        self.nombre_medico = ""
        self.url = ""
    
    def limpiar_campos_PacEdit(self):
        self.nameedtpac.setText("")
        self.lastnameedtpac.setText("")
        self.ageedtpac.setText("")
        self.idedtpac.setText("")
        self.nombre_medico = ""
        self.url = ""

    def volver(self):
        self.nameedtpac.setText("")
        self.lastnameedtpac.setText("")
        self.ageedtpac.setText("")
        self.idedtpac.setText("")
        self.namepac.setText("")
        self.lastnamepac.setText("")
        self.agepac.setText("")
        self.idpac.setText("")
        self.idpac_buscar.setText("")
        self.nombre_medico = ""
        self.url = ""
        self.edicionespac.setCurrentIndex(0)
        
    def lista_med(self):
        self.desplegedtmed.addItems(self.Controller.lista_medCont)
        self.comboBox.currentTextChanged.connect(self.actualizar_nombre_seleccionado)
        
    def actualizar_nombre_seleccionado(self, nombre_seleccionado):
        self.nombre_medico = nombre_seleccionado

    def busquedapac(self):
        texto = self.idpac_buscar.text()
        idpac_buscar = ''.join(c.upper() if c.isalpha() else c for c in texto)
        if self.Controller.validarPacCont(idpac_buscar):
            self.groupBox_10.show()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Ya existe un usuario con el ID diligenciado.')
            msgBox.setWindowTitle('Usuario no existe')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.idpac_buscar.setText("")
            msgBox.exec()

    def eliminarpac(self):
        texto = self.idpac_eliminar.text()
        idpac_eliminar = ''.join(c.upper() if c.isalpha() else c for c in texto)
        if not idpac_eliminar:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete el campo.')
            msgBox.setWindowTitle('Campo incompleto')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        bool = self.Controller.eliminarPacCont(idpac_eliminar)
        if bool:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Paciente eliminado exitosamente')
            msgBox.setWindowTitle('Paciente eliminado')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.idpac_eliminar.setText("")
            msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Paciente no existente en la base de datos')
            msgBox.setWindowTitle('Paciente no existente')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.idpac_eliminar.setText("")
            msgBox.exec()

    def estudio(self):
        texto = self.idpac_estudio.text()
        idpac_estudio = ''.join(c.upper() if c.isalpha() else c for c in texto)
        if self.Controller.validarPacCont(idpac_estudio):
            namepac, lastnamepac, agepac, idpac, medpac, url, = self.Controller.pacienteCon(idpac_estudio)
            self.abrir_dicom(namepac, lastnamepac, agepac, idpac, medpac, url)
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Ya existe un usuario con el ID diligenciado.')
            msgBox.setWindowTitle('Usuario no existe')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.idpac_buscar.setText("")
            msgBox.exec()

    def holamed(self):
        self.base.setCurrentIndex(2)
        self.newmed.clicked.connect(self.nuevopac)
        self.editmed.clicked.connect(self.editarmed)
        self.erasemed.clicked.connect(self.borrarmed)
    
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


class VentanaEmergente(QDialog):
    def __init__(self, namepac:str, lastnamepac:str, agepac:str, idpac:str, medpac:str):
        super().__init__()
        loadUi("imagenes_dicom.ui",self)
        self.minimizar.clicked.connect(self.minimizator)
        self.exit.clicked.connect(self.salir)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.horizontalSlider.valueChanged.connect(self.actualizar_imagen) #configurar el slider
        self.nombreline.setText(namepac)
        self.apellidoline.setText(lastnamepac)
        self.edadline.setText(agepac)
        self.idline.setText(idpac)
        self.medicoline.setText(medpac)

    def minimizator(self):
        self.showMinimized()
        
    def salir(self):
        self.Controller.desconectar()
        QApplication.quit()  

    def mostrar_imagen_procesada(self, imagen_procesada):
        self.imagen_procesada = imagen_procesada
        self.actualizar_imagen()

    def actualizar_imagen(self):
        indice = self.deslizador1.value()
        # Obtener la imagen correspondiente al índice
        imagen = self.imagen_procesada[indice]
        #convertir a QPixmap para ver en el Qlabel
        pixmap = QPixmap.fromImage(imagen)
        self.label.setPixmap(pixmap)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = ventanaLogin()
    login.show()
    sys.exit(app.exec_())

