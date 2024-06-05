from Modelo import *
from PyQt5.QtWidgets import QMessageBox

class controlador:
    def __init__(self, controlador = BaseMySQL(), acceso = manejoUsuarios()):
        self.__controlador = controlador
        self.__acceso = acceso
    
    def desconectar(self):
        self.__controlador.desconectar()
    
    def ingresarPacCont(self, namepac:str, lastnamepac:str, agepac:str, idpac:str, medpac:str, url:str):
        return self.__controlador.ingresarPac(namepac, lastnamepac, agepac, idpac, medpac, url)
        
    def eliminarPacCont(self, identificacion:str):
        return self.__controlador.eliminarPac(identificacion)
    
    def editarPacCont(self, idpac:str, nueva_id:str, namepac:str, lastnamepac:str, agepac:str, medpac:str, url:str):
        return self.__controlador.editarPac(idpac, nueva_id, namepac, lastnamepac, agepac, medpac, url)
    
    



        
    def ingresoCont(self, username:str, password:str):
        return self.__acceso.ingreso(username, password)
    
    def nuevoUsuarioCont(self, username:str, password:str):
        return self.__acceso.nuevousuario(username, password)
    
    def modificarUsuarioCont(self, usernameviejo:str, passwordviejo:str, username:str, password:str):
        return self.__acceso.modificar(usernameviejo, passwordviejo, username, password)
        
    
        
    
        