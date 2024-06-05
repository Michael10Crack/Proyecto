from Modelo import *
from PyQt5.QtWidgets import QMessageBox

class controlador:
    def __init__(self, controlador = BaseMySQL(), acceso = manejoUsuarios()):
        self.__controlador = controlador
        self.__acceso = acceso
    
    def desconectar(self):
        self.__controlador.desconectar()
    
    def ingresarPacCont(self, nombre:str, apellido:str, edad:str, identificacion:str):
        bool = self.__controlador.ingresarPac(nombre, apellido, edad, identificacion)
        return bool
    
    def listaPacCont(self, nombre):
        return self.__controlador.buscar(nombre)
    
    def eliminarPacCont(self, identificacion:str):
        return self.__controlador.eliminarPac(identificacion)

        ####################################

    def insertarArchivoCont(self, clave, tipo, ruta):
        return self.__controlador.insertarArchivo(clave, tipo, ruta)
    
    def obtenerArchivosCont(self, tipo=None):
        return self.__controlador.obtenerArchivos(tipo)
    
    def cargarMatCont(self, ruta):
        return self.__controlador.cargarMat(ruta)
    
    def cargarCsvCont(self, ruta):
        return self.__controlador.cargarCsv(ruta)

    def insertarDatosMatCont(self, archivo_id, nombre_matriz):
        return self.__controlador.insertarDatosMat(archivo_id, nombre_matriz)

    def insertarDatosCsvCont(self, archivo_id, nombre_columna):
        return self.__controlador.insertarDatosCsv(archivo_id, nombre_columna)
    
    def eliminarArchivo(self, clave):
        return self.modelo.eliminarArchivo(clave)
    
    def mostrarMensajeError(self, mensaje):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(mensaje)
        msgBox.setWindowTitle('Error')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
    
        ####################################
        
    def ingresoCont(self, username:str, password:str):
        return self.__acceso.ingreso(username, password)
    
    def nuevoUsuarioCont(self, username:str, password:str):
        return self.__acceso.nuevousuario(username, password)
    
    def modificarUsuarioCont(self, usernameviejo:str, passwordviejo:str, username:str, password:str):
        return self.__acceso.modificar(usernameviejo, passwordviejo, username, password)
        
    
        
    
        