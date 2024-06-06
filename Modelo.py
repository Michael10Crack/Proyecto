import mysql.connector

class BaseMySQL:
    def __init__(self):
        self.__host = 'localhost'
        self.__username = 'admin123'
        self.__password = 'contrasena123'
        self.__database = 'database'
        self.__connection = None
#nea n

    def validarIngreso(self, username:str, password:str):
        if username == self.__username and password == self.__password:
            return True
        return False
    
    def conectar(self, username:str , password:str):
        if self.validarIngreso(username, password):
            self.__connection = mysql.connector.connect(
                host = self.__host,
                user = self.__username,
                password = self.__password,
                database = self.__database
            )
            return True
        return False
    
    def desconectar(self):
        if self.__connection:
            self.__connection.close()
            self.__connection = None
            return True
        return False

    def validarPac(self, identificacion:str):
        query = 'SELECT * FROM pacientes WHERE identificacion = %s'
        cursor = self.__connection.cursor()
        cursor.execute(query, (identificacion,))
        results = cursor.fetchall()
        cursor.close()
        return len(results) == 0
            
    def ingresarPac(self, nombre:str, apellido:str, edad:str, identificacion:str):
        if self.validarPac(identificacion):
            query = 'INSERT INTO pacientes (nombre, apellido, edad, identificacion) VALUES (%s, %s, %s, %s)'
            values = (nombre, apellido, edad, identificacion)
            cursor = self.__connection.cursor()
            cursor.execute(query, values)
            self.__connection.commit()
            cursor.close()
            return True
        return False
        
    def eliminarPac(self, identificacion:str):
        if not self.validarPac(identificacion):
            query = 'DELETE FROM pacientes WHERE identificacion = %s'
            cursor = self.__connection.cursor()
            cursor.execute(query, (identificacion,))
            self.__connection.commit()
            cursor.close()
        return False
    
    def buscar(self, nombre):
        query = 'SELECT nombre, apellido, edad, identificacion FROM pacientes'
        cursor = self.__connection.cursor()
        cursor.execute(query)
        valores_columna = cursor.fetchall()
        cursor.close()
        if nombre:
            pacientes = [fila for fila in valores_columna if fila[0].startswith(nombre)]
        else:
            pacientes = valores_columna
        return pacientes

        
