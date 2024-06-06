import sys 
import pydicom
import os
import cv2
from Controlador import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit, QFileDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QSlider, QFrame, QHBoxLayout
from PyQt5.QtGui import QRegExpValidator, QPixmap
from PyQt5.QtCore import Qt, QRegExp, QTimer
from PyQt5.uic import loadUi

class ventanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("login.ui",self)
        self.Controller = controlador()
        self.ventananewuser = newuser(self)
        self.ventanaedituser = edituser(self)
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
        self.ingresar.clicked.connect(self.anadirLogin)
        self.nuevo.clicked.connect(self.newuser)
        self.editar.clicked.connect(self.edituser)
        self.password.setEchoMode(QLineEdit.Password)

    def minimizator(self):
        self.showMinimized()     
        
    def salir(self):
        self.Controller.desconectar()
        QApplication.quit()  

    def anadirLogin(self):
        try:
            self.ingresar.clicked.disconnect()
        except TypeError:
            pass
        self.ingresar.clicked.connect(self.login)
        
    def login(self):
        username = self.username.text()
        password = self.password.text()
        existe = self.Controller.ingresoCont(username, password)
        if existe:
            self.Controller.conectar()
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
        self.ingresar.clicked.connect(self.desconectIngNueUser)
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

    def desconectIngNueUser(self):
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
        self.verEstudio = VisualizadorDICOM()
        self.nombre_medicopn = ""
        self.nombre_medicope = ""
        self.urlpn = ""
        self.urlpe = ""
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setup()

    def setup(self):
        self.min.clicked.connect(self.minimizator)
        self.out.clicked.connect(self.salir)
        self.pacientes.clicked.connect(self.holapac)
        self.medicos.clicked.connect(self.holamed)
        self.lista_med()
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
        self.hojaspac()
        self.newpac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(1))
        self.editpac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(2))
        self.erasepac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(3))
        self.estudiospac.clicked.connect(lambda: self.edicionespac.setCurrentIndex(4))
        self.edicionespac.currentChanged.connect(self.update_widgets_pacientes)
        
    def hojaspac(self):
        regex = r'^[a-zA-Z0-9]+$'
        validator = QRegExpValidator(QRegExp(regex))
        self.namepac.setValidator(validator)
        self.lastnamepac.setValidator(validator)
        self.agepac.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.idpac.setValidator(validator)
        self.idpac_buscar.setValidator(validator)
        self.nameedtpac.setValidator(validator)
        self.lastnameedtpac.setValidator(validator)
        self.ageedtpac.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.idedtpac.setValidator(validator)

    def update_widgets_pacientes(self, index):
        if index == 1:
            self.browse.setText("SELECCIONE EL ARCHIVO")
            self.cargaedtpac.setText("SELECCIONE EL ARCHIVO")
            self.addpac.clicked.connect(self.anadirPacNuevo)
            self.cancelpac.clicked.connect(self.volverpac)
            self.browse.clicked.connect(self.anadirCargarNuevo)
        elif index == 2:
            self.buscarpac.clicked.connect(self.anadirPacBus)
            self.browse.setText("SELECCIONE EL ARCHIVO")
            self.cargaedtpac.setText("SELECCIONE EL ARCHIVO")
            self.addedtpac.clicked.connect(self.anadirPacEdit)
            self.canceledtpac.clicked.connect(self.volverpac)
            self.cargaedtpac.clicked.connect(self.anadirCargarEdit)
            self.groupBox_10.hide()
            pass
        elif index == 3:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.idpac_eliminar.setValidator(validator)
            self.paceliminar.clicked.connect(self.eliminarpac)
        elif index == 4:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.idpac_estudio.setValidator(validator)
            self.anadirestudio()

    def anadirPacNuevo(self):
        try:
            self.addpac.clicked.disconnect()
        except TypeError:
            pass
        self.addpac.clicked.connect(self.okPacNuevo)

    def anadirPacBus(self):
        try:
            self.buscarpac.clicked.disconnect()
        except TypeError:
            pass
        self.buscarpac.clicked.connect(self.busquedaPac)
       
    def anadirPacEdit(self):
        try:
            self.addedtpac.clicked.disconnect()
        except TypeError:
            pass
        self.addedtpac.clicked.connect(self.okPacEdit)
        
    def anadirPacEli(self):
        try:
            self.paceliminar.clicked.disconnect()
        except TypeError:
            pass
        self.paceliminar.clicked.connect(self.eliminarpac)   
    
    def anadirCargarNuevo(self):
        try:
            self.browse.clicked.disconnect()
        except TypeError:
            pass
        self.browse.clicked.connect(self.procesar_dicom)   
    
    def anadirCargarEdit(self):
        try:
            self.cargaedtpac.clicked.disconnect()
        except TypeError:
            pass
        self.cargaedtpac.clicked.connect(self.procesar_dicom) 
    
    def anadirestudio(self):
        try:
            self.pacestudio.clicked.disconnect()
        except TypeError:
            pass
        self.pacestudio.clicked.connect(self.estudio)
    
    def procesar_dicom(self):
        ruta_carpeta = QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta con archivos DICOM', '')
        if ruta_carpeta:
            archivos_dicom = [os.path.join(ruta_carpeta, file) for file in os.listdir(ruta_carpeta) if file.endswith('.dcm')]
            if archivos_dicom:
                    try:
                        for file in archivos_dicom:
                            dicom_data = pydicom.dcmread(file)                        
                        # Procesar el archivo DICOM
                            manejador_dicom = self.Controller.manejodicompath(dicom_data)
                            imagen_procesada = self.Controller.apply_modality_lut(manejador_dicom.pixel_array)
                        # Cadena original 
                            ruta_carpeta
                            # Dividir la cadena en partes utilizando "/" como separador
                            partes = ruta_carpeta.split("/")
                            # Buscar la parte que contiene "Archivos_Dicom"
                            indice_archivos_dicom = partes.index("Archivos_Dicom")
                            # Guardar la parte de la cadena desde "Archivos_Dicom" en adelante
                            ruta_carpeta = "/".join(partes[indice_archivos_dicom:])
                        self.urlpe = ruta_carpeta
                        self.urlpn = ruta_carpeta
                        self.exito(ruta_carpeta)
                        self.browse.setText("ARCHIVO CARGADO")
                        self.cargaedtpac.setText("ARCHIVO CARGADO")
                    except pydicom.errors.InvalidDicomError:
                        # El archivo no es un archivo DICOM válido
                        self.mostrar_advertencia(file)
                        self.lista_med()
                        pass
            else:
                self.mostrar_advertencia2()
                self.lista_med()
                
    def okPacNuevo(self):
        namepac = self.namepac.text().upper()
        lastnamepac = self.lastnamepac.text().upper()
        agepac = self.agepac.text()
        texto = self.idpac.text()
        idpac = ''.join(c.upper() if c.isalpha() else c for c in texto)
        medpac = self.nombre_medicopn
        url = self.urlpn
        if not namepac or not lastnamepac or not agepac or not idpac or medpac == '' or url == '':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_PacNuevo()
            self.lista_med()
            self.browse.setText("SELECCIONE EL ARCHIVO")
            self.urlpn = ''
            self.nombre_medicopn = ''
            msgBox.exec()
        else:
            bool = self.Controller.ingresarPacCont(namepac, lastnamepac, agepac, idpac, medpac, url)
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Paciente ingresado exitosamente')
                msgBox.setWindowTitle('Paciente ingresado')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_PacNuevo()
                self.lista_med()
                self.groupBox_10.hide()
                self.browse.setText("SELECCIONE EL ARCHIVO")
                self.urlpn = ''
                self.nombre_medicopn = ''
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Ya existe un usuario con el ID diligenciado.\nIngrese uno diferente.')
                msgBox.setWindowTitle('Usuario existente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_PacNuevo()
                self.lista_med()
                self.agepac.setText("SELECCIONE EL ARCHIVO")
                self.url = ''
                self.nombre_medicopn = ''
                msgBox.exec()
        
    def okPacEdit(self):
        nameedtpac = self.nameedtpac.text().upper()
        lastnameedtpac = self.lastnameedtpac.text().upper()
        ageedtpac = self.ageedtpac.text()
        texto = self.idedtpac.text()
        idedtpac = ''.join(c.upper() if c.isalpha() else c for c in texto)
        medpac = self.nombre_medicope
        url = self.urlpe
        idpac_buscar = self.idpac_buscar.text()
        if not nameedtpac or not lastnameedtpac or not ageedtpac or not idedtpac or medpac == '' or url == '':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_PacEdit()
            self.lista_med()
            self.cargaedtpac.setText("SELECCIONE EL ARCHIVO")
            self.urlpe = ''
            self.nombre_medicope = ''
            msgBox.exec()
        else:
            bool = self.Controller.editarPacCont(idpac_buscar, idedtpac, nameedtpac, lastnameedtpac, ageedtpac, medpac, url )
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Paciente ingresado exitosamente')
                msgBox.setWindowTitle('Paciente ingresado')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_PacEdit()
                self.lista_med()
                self.groupBox_10.hide()
                self.cargaedtpac.setText("SELECCIONE EL ARCHIVO")
                self.urlpe = ''
                self.nombre_medicope = ''
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('No existe un paciente con el ID diligenciado.')
                msgBox.setWindowTitle('Usuario existente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_PacEdit()
                self.lista_med()
                self.cargaedtpac.setText("SELECCIONE EL ARCHIVO")
                self.urlpe = ''
                self.nombre_medicope = ''
                msgBox.exec()

    def limpiar_campos_PacNuevo(self):
        self.namepac.setText("")
        self.lastnamepac.setText("")
        self.agepac.setText("")
        self.idpac.setText("")
        self.nombre_medicopn = ""
        self.urlpn = ""
        self.nombre_medicope = ""
        self.urlpe = ""
    
    def limpiar_campos_PacEdit(self):
        self.nameedtpac.setText("")
        self.lastnameedtpac.setText("")
        self.ageedtpac.setText("")
        self.idedtpac.setText("")
        self.nombre_medicopn = ""
        self.urlpn = ""
        self.nombre_medicope = ""
        self.urlpe = ""

    def volverpac(self):
        self.nameedtpac.setText("")
        self.lastnameedtpac.setText("")
        self.ageedtpac.setText("")
        self.idedtpac.setText("")
        self.namepac.setText("")
        self.lastnamepac.setText("")
        self.agepac.setText("")
        self.idpac.setText("")
        self.idpac_buscar.setText("")
        self.nombre_medicopn = ""
        self.urlpn = ""
        self.nombre_medicope = ""
        self.urlpe = ""
        self.edicionespac.setCurrentIndex(0)
        
    def lista_med(self):
        self.actualizar_lista_medicos()
        
    def actualizar_lista_medicos(self):
        lista_medicos = self.Controller.lista_medicosCont()
        lista_medicos.insert(0, "")
        self.desplegmed.clear()
        self.desplegedtmed.clear()
        self.desplegmed.addItems(lista_medicos)
        self.desplegedtmed.addItems(lista_medicos)
        self.desplegmed.currentTextChanged.connect(self.actualizar_nombremed_seleccionadopacn)
        self.desplegedtmed.currentTextChanged.connect(self.actualizar_nombremed_seleccionadopace)

    def actualizar_nombremed_seleccionadopacn(self, nombre_seleccionado):
        self.nombre_medicopn = nombre_seleccionado
    
    def actualizar_nombremed_seleccionadopace(self, nombre_seleccionado):
        self.nombre_medicope = nombre_seleccionado

    def busquedaPac(self):
        texto = self.idpac_buscar.text()
        idpac_buscar = ''.join(c.upper() if c.isalpha() else c for c in texto)
        if not idpac_buscar:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete el campo.')
            msgBox.setWindowTitle('Campo incompleto')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.idpac_buscar.setText("")
            msgBox.exec()
        else:
            if self.Controller.validarPacCont(idpac_buscar):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('No existe un paciente con el ID diligenciado.')
                msgBox.setWindowTitle('Paciente no existe')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.idpac_buscar.setText("")
                msgBox.exec()
            else:
                self.groupBox_10.show()

    def eliminarpac(self):
        texto = self.idpac_eliminar.text()
        idpac_eliminar = ''.join(c.upper() if c.isalpha() else c for c in texto)
        if not idpac_eliminar:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete el campo.')
            msgBox.setWindowTitle('Campo incompleto')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.idpac_eliminar.setText("")
            msgBox.exec()  
        else:
            bool = self.Controller.eliminarPacCont(idpac_eliminar)
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Paciente no existente en la base de datos')
                msgBox.setWindowTitle('Paciente no existente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.idpac_eliminar.setText("")
                msgBox.exec()
            elif bool == False:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Paciente eliminado exitosamente')
                msgBox.setWindowTitle('Paciente eliminado')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.idpac_eliminar.setText("")
                msgBox.exec()
                
    def estudio(self):
        texto = self.idpac_estudio.text()
        idpac_estudio = ''.join(c.upper() if c.isalpha() else c for c in texto)
        if self.Controller.validarPacCont(idpac_estudio):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('No existe un usuario con el ID diligenciado.')
            msgBox.setWindowTitle('Usuario no existe')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.idpac_estudio.setText("")
            msgBox.exec()
        else:
            namepac, lastnamepac, agepac, idpac, medpac, url = self.Controller.pacienteCon(idpac_estudio)
            self.verEstudio = VisualizadorDICOM()  # Reinstanciar la ventana para cada paciente
            self.verEstudio.setup()
            self.verEstudio.initUI(url)
            self.verEstudio.setup2(namepac, lastnamepac, agepac, idpac, medpac)
            self.idpac_estudio.setText("")
            self.verEstudio.show()
        
    def exito(self, ruta_carpeta):
        # Mostrar una ventana emergente con un mensaje de procesamiento exitoso
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(f'Carpeta DICOM seleccionada: {ruta_carpeta}')
        msgBox.setWindowTitle('Información')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def mostrar_advertencia(self, file):
        # Mostrar una ventana emergente con un mensaje de advertencia
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(f"Error al procesar la imagenen {file}.")
        msgBox.setWindowTitle('Advertencia')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def mostrar_advertencia2(self):
        # Mostrar una ventana emergente con un mensaje de advertencia
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("La carpeta seleccionada no contiene archivos DICOM")
        msgBox.setWindowTitle('Advertencia')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def holamed(self):
        self.base.setCurrentIndex(2)
        self.edicionesmed.show()
        self.edicionesmed.setCurrentIndex(0)
        self.hojasmed()
        self.newmed.clicked.connect(lambda: self.edicionesmed.setCurrentIndex(1))
        self.editmed.clicked.connect(lambda: self.edicionesmed.setCurrentIndex(2))
        self.erasemed.clicked.connect(lambda: self.edicionesmed.setCurrentIndex(3))
        self.edicionesmed.currentChanged.connect(self.update_widgets)
        
    def hojasmed(self):
        regex = r'^[a-zA-Z0-9]+$'
        validator = QRegExpValidator(QRegExp(regex))
        self.namemed.setValidator(validator)
        self.lastnamemed.setValidator(validator)
        self.agemed.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.regmed.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.espmed.setValidator(validator)
        self.regedtmed.setValidator(validator)
        self.nameedtmed.setValidator(validator)
        self.lastnameedtmed.setValidator(validator)
        self.ageedtmed.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.regedtmed.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.espedtmed.setValidator(validator)

    def update_widgets(self, index):
        if index == 1:
            self.addmed.clicked.connect(self.anadirMedNuevo)
            self.cancelmed.clicked.connect(self.volver)
        elif index == 2:
            self.buscarmed.clicked.connect(self.anadirMedBus)
            self.addedtmed.clicked.connect(self.anadirMedEdit)
            self.canceledtmed.clicked.connect(self.volver)
            self.groupBox_8.hide()
        elif index == 3:
            regex = r'^[a-zA-Z0-9]+$'
            validator = QRegExpValidator(QRegExp(regex))
            self.reg_eliminar.setValidator(validator)
            self.medeliminar.clicked.connect(self.eliminarmed)
            
    def anadirMedNuevo(self):
        try:
            self.addmed.clicked.disconnect()
        except TypeError:
            pass
        self.addmed.clicked.connect(self.okMedNuevo)

    def anadirMedBus(self):
        try:
            self.buscarmed.clicked.disconnect()
        except TypeError:
            pass
        self.buscarmed.clicked.connect(self.busquedaMed)
       
    def anadirMedEdit(self):
        try:
            self.addedtmed.clicked.disconnect()
        except TypeError:
            pass
        self.addedtmed.clicked.connect(self.okMedEdit)
        
    def anadirMedEli(self):
        try:
            self.medeliminar.clicked.disconnect()
        except TypeError:
            pass
        self.medeliminar.clicked.connect(self.eliminarmed)   
   
    def okMedNuevo(self):
        namemed = self.namemed.text().upper()
        lastnamemed = self.lastnamemed.text().upper()
        agemed = self.agemed.text()
        regmed = self.regmed.text()
        espmed = self.espmed.text().upper()
        if not namemed or not lastnamemed or not agemed or not agemed or not regmed or not espmed:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_MedNuevo()
            self.lista_med()
            msgBox.exec()
        else:
            bool = self.Controller.ingresarMedCont(namemed, lastnamemed, agemed, regmed, espmed)
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Médico ingresado exitosamente')
                msgBox.setWindowTitle('Médico ingresado')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_MedNuevo()
                self.groupBox_8.hide()
                self.lista_med()
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Ya existe un usuario con el ID diligenciado.\nIngrese uno diferente.')
                msgBox.setWindowTitle('Usuario existente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_MedNuevo()
                self.agemed.setText("SELECCIONE EL ARCHIVO")
                msgBox.exec()
        
    def okMedEdit(self):
        nameedtmed = self.nameedtmed.text().upper()
        lastnameedtmed = self.lastnameedtmed.text().upper()
        ageedtmed = self.ageedtmed.text()
        regedtmed = self.regedtmed.text()
        espedtmed = self.espedtmed.text()
        reg_buscar = self.reg_buscar.text()
        if not nameedtmed or not lastnameedtmed or not ageedtmed or not ageedtmed or not espedtmed:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete todos los campos.')
            msgBox.setWindowTitle('Campos incompletos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.limpiar_campos_MedEdit()
            msgBox.exec()
        else:
            bool = self.Controller.editarMedCont(reg_buscar, regedtmed, nameedtmed, lastnameedtmed, ageedtmed, ageedtmed, espedtmed)
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Médico ingresado exitosamente')
                msgBox.setWindowTitle('Médico ingresado')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_MedEdit()
                self.groupBox_8.hide()
                self.lista_med()
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('No existe un mpedico con el registro diligenciado.')
                msgBox.setWindowTitle('Médico existente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.limpiar_campos_MedEdit()
                msgBox.exec()

    def limpiar_campos_MedNuevo(self):
        self.namemed.setText("")
        self.lastnamemed.setText("")
        self.agemed.setText("")
        self.regmed.setText("")
        self.espmed.setText("")
        self.regedtmed.setText("")
    
    def limpiar_campos_MedEdit(self):
        self.nameedtmed.setText("")
        self.lastnameedtmed.setText("")
        self.ageedtmed.setText("")
        self.regedtmed.setText("")
        self.espedtmed.setText("")

    def volver(self):
        self.namemed.setText("")
        self.lastnamemed.setText("")
        self.agemed.setText("")
        self.regmed.setText("")
        self.espmed.setText("")
        self.regedtmed.setText("")
        self.nameedtmed.setText("")
        self.lastnameedtmed.setText("")
        self.ageedtmed.setText("")
        self.regedtmed.setText("")
        self.espedtmed.setText("")
        self.reg_buscar_2.setText("")
        self.edicionesmed.setCurrentIndex(0)
        
    def busquedaMed(self):
        reg_buscar = self.reg_buscar_2.text()
        if not reg_buscar:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete el campo.')
            msgBox.setWindowTitle('Campo incompleto')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.regedtmed.setText("")
            msgBox.exec()
        else:
            if self.Controller.validarMedCont(reg_buscar):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('No existe un médico con el registro diligenciado.')
                msgBox.setWindowTitle('Médico no existe')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.regedtmed.setText("")
                msgBox.exec()
            else:
                self.groupBox_8.show()

    def eliminarmed(self):
        reg_eliminar = self.reg_eliminar.text()
        if not reg_eliminar:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Por favor, complete el campo.')
            msgBox.setWindowTitle('Campo incompleto')
            msgBox.setStandardButtons(QMessageBox.Ok)
            self.reg_eliminar.setText("")
            msgBox.exec()  
        else:
            bool = self.Controller.eliminarmedCont(reg_eliminar)
            if bool:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Médico no existente en la base de datos')
                msgBox.setWindowTitle('Médico no existente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.reg_eliminar.setText("")
                msgBox.exec()
            elif bool == False:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('Médico eliminado exitosamente')
                msgBox.setWindowTitle('Médico eliminado')
                msgBox.setStandardButtons(QMessageBox.Ok)
                self.reg_eliminar.setText("")
                self.lista_med()
                msgBox.exec()       
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

class VisualizadorDICOM(QDialog):
    def init(self):
        super().init()
        self.ruta_carpeta = None
        self.archivos_dicom = []
        self.indice_actual = 0
        self.label = None
        self.timer = None
        self.setup()

    def setup(self):
    
        self.Controller = controlador()
        loadUi("imagenes_dicom.ui", self)
        self.label = self.findChild(QLabel, "label")
        self.frame_principal = self.findChild(QFrame, "frame_principal")
        self.btn_minimizar = self.findChild(QPushButton, "minimizar")
        self.btn_cerrar = self.findChild(QPushButton, "exit")
        self.btn_adelante = self.findChild(QPushButton, "adelante")
        self.btn_atras = self.findChild(QPushButton, "atras")
        self.slider = self.findChild(QSlider, "slider")

        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.addWidget(self.frame_principal)
        self.setLayout(self.layout_principal)

        # Conectar los eventos
        self.btn_minimizar.clicked.connect(self.minimizator)
        self.btn_cerrar.clicked.connect(self.salir)
        self.btn_adelante.clicked.connect(self.avanzar_imagen)
        self.btn_atras.clicked.connect(self.retroceder_imagen)
        self.slider.sliderMoved.connect(self.slider_moved)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setup2(self, namepac, lastnamepac, agepac, idpac, medpac):
        self.nombreline.setText(namepac)
        self.apellidoline.setText(lastnamepac)
        self.edadline.setText(agepac)
        self.idline.setText(idpac)
        self.medicoline.setText(medpac)

    def minimizator(self):
        self.showMinimized()
    
    def salir(self):
        self.hide()

    def initUI(self, ruta):
        self.ruta_carpeta = ruta
        self.archivos_dicom = [os.path.join(ruta, file) for file in os.listdir(ruta) if file.endswith('.dcm')]
        self.indice_actual = 0
        self.slider.setMaximum(len(self.archivos_dicom) - 1)  # Establecer el maximo del slider

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.avanzar_imagen)
        # self.timer.start(2000)  # Cambiar la imagen cada 2 segundos

        self.mostrar_siguiente_imagen()

    def mostrar_siguiente_imagen(self):
        if self.archivos_dicom:
            if 0 <= self.indice_actual < len(self.archivos_dicom):
                archivo_dicom = self.archivos_dicom[self.indice_actual]
                imagen_dicom = pydicom.dcmread(archivo_dicom)
                pixel_data = imagen_dicom.pixel_array

                imagen_normalizada = cv2.normalize(pixel_data, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
                alpha = 1.5
                beta = 50
                imagen_ajustada = cv2.convertScaleAbs(imagen_normalizada, alpha=alpha, beta=beta)

                imagen_qt = QImage(imagen_ajustada.data, imagen_ajustada.shape[1], imagen_ajustada.shape[0], QImage.Format_Grayscale8)

                pixmap = QPixmap.fromImage(imagen_qt)
                self.label.setPixmap(pixmap)
                self.label.setScaledContents(True)  # Ajustar la imagen al tamaño del QLabel
                self.slider.setValue(self.indice_actual)

    def avanzar_imagen(self):
        self.indice_actual += 1
        if self.indice_actual >= len(self.archivos_dicom):
            self.indice_actual = 0
        self.mostrar_siguiente_imagen()

    def retroceder_imagen(self):
        self.indice_actual -= 1
        if self.indice_actual < 0:
            self.indice_actual = len(self.archivos_dicom) - 1
        self.mostrar_siguiente_imagen()

    def slider_moved(self, value):
        self.indice_actual = value
        self.mostrar_siguiente_imagen()
    
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
