from Modelo import *

class controlador:
    def __init__(self, controlador = BaseMySQL(), acceso = manejoUsuarios(), manejodicom = manejodicom()):
        self.__controlador = controlador
        self.__acceso = acceso
        self.__manejodicom = manejodicom
    
    def conectar(self):
        return self.__controlador.conectar()
    
    def desconectar(self):
        self.__controlador.desconectar()
    
    def ingresarPacCont(self, namepac:str, lastnamepac:str, agepac:str, idpac:str, medpac:str, url:str):
        return self.__controlador.ingresarPac(namepac, lastnamepac, agepac, idpac, medpac, url)
        
    def eliminarPacCont(self, identificacion:str):
        return self.__controlador.eliminarPac(identificacion)
    
    def editarPacCont(self, idpac:str, nueva_id:str, namepac:str, lastnamepac:str, agepac:str, medpac:str, url:str):
        return self.__controlador.editarPac(idpac, nueva_id, namepac, lastnamepac, agepac, medpac, url)
    
    def lista_medicosCont(self):
        return self.__controlador.lista_medicos()
        
    def ingresoCont(self, username:str, password:str):
        return self.__acceso.ingreso(username, password)
    
    def nuevoUsuarioCont(self, username:str, password:str):
        return self.__acceso.nuevousuario(username, password)
    
    def modificarUsuarioCont(self, usernameviejo:str, passwordviejo:str, username:str, password:str):
        return self.__acceso.modificar(usernameviejo, passwordviejo, username, password)
        
    def manejodicompath(self, path):
        self.__manejodicom.dicom(path) 
        
    def apply_modality_lut(self):
        return  self.__manejodicom.apply_modality_lut()
        
    
        