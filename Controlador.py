from Modelo import *

class controlador:
    def __init__(self, controlador = BaseMySQL()):
        self.__controlador = controlador
    
    def conectarCont(self, username:str, password:str):
        bool = self.__controlador.conectar(username, password)         
        return bool
    
    def ingresarPacCont(self, nombre:str, apellido:str, edad:str, identificacion:str):
        bool = self.__controlador.ingresarPac(nombre, apellido, edad, identificacion)
        return bool
    
    def listaPacCont(self, nombre):
        return self.__controlador.buscar(nombre)
    
    def eliminarPacCont(self, identificacion:str):
        return self.__controlador.eliminarPac(identificacion)

    
    
        
    
    
        