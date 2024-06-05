import mysql.connector
import json
import pandas as pd
import scipy.io as sio

class BaseMySQL:
    def __init__(self):
        self.__host = 'localhost'
        self.__username = 'admin123'
        self.__password = 'contrasena123'
        self.__database = 'database'
        self.__connection = None

    def conectar(self):
        self.__connection = mysql.connector.connect(
            host = self.__host,
            user = self.__username,
            password = self.__password,
            database = self.__database
        )
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
            
    def ingresarPac(self, namepac:str, lastnamepac:str, agepac:str, idpac:str, medpac:str,):
        if self.validarPac(idpac):
            query = 'INSERT INTO pacientes (nombre, apellido, edad, identificacion, med_cabecera) VALUES (%s, %s, %s, %s, %s, %s)'
            values = (namepac, lastnamepac, agepac, idpac, medpac)
            cursor = self.__connection.cursor()
            cursor.execute(query, values)
            self.__connection.commit()
            cursor.close()
            return True
        return False
        
    def eliminarPac(self, idpac:str):
        if self.validarPac(idpac) == None:
            return False
        else:             
            query = 'DELETE FROM pacientes WHERE identificacion = %s'
            cursor = self.__connection.cursor()
            cursor.execute(query, (idpac,))
            self.__connection.commit()
            cursor.close()
            return True
    
    def editarPac(self, idpac:str, nueva_id:str, namepac:str, lastnamepac:str, agepac:str, medpac:str):
        # Verificar si la nueva ID ya existe
        if not self.validarPac(nueva_id):
            return False
        cursor = self.__connection.cursor()
        sql = "UPDATE pacientes SET identificacion = %s, nombre = %s, apellido = %s, edad = %s, med_cabecera = %s WHERE identificacion = %s"
        val = (nueva_id, namepac, lastnamepac, agepac, medpac, idpac)
        cursor.execute(sql, val)
        self.__connection.commit()
        cursor.close()
        return True















    def insertarArchivo(self, clave, tipo, ruta):
        query = 'INSERT INTO archivos (clave, tipo, ruta) VALUES (%s, %s, %s)'
        values = (clave, tipo, ruta)
        cursor = self.__connection.cursor()
        cursor.execute(query, values)
        self.__connection.commit()
        archivo_id = cursor.lastrowid
        cursor.close()
        return archivo_id

    def insertarDatosMat(self, archivo_id, nombre_matriz):
        query = 'INSERT INTO datos_mat (archivo_id, nombre_matriz) VALUES (%s, %s)'
        values = (archivo_id, nombre_matriz)
        cursor = self.__connection.cursor()
        cursor.execute(query, values)
        self.__connection.commit()
        cursor.close()

    def insertarDatosCsv(self, archivo_id, nombre_columna):
        query = 'INSERT INTO datos_csv (archivo_id, nombre_columna) VALUES (%s, %s)'
        values = (archivo_id, nombre_columna)
        cursor = self.__connection.cursor()
        cursor.execute(query, values)
        self.__connection.commit()
        cursor.close()

    def cargarMat(self, ruta, controlador):
        try:
            data = sio.loadmat(ruta)
            return data, None 
        except Exception as e:
            mensaje_error = f'Error al cargar archivo MAT: {e}'
            controlador.mostrarMensajeError(mensaje_error)
            return None, mensaje_error

    def cargarCsv(self, ruta, controlador, delimiter=','): #el código solo recibe delimitaciones por comas ',' 
        try:
            data = pd.read_csv(ruta, delimiter=delimiter)
            return data
        except Exception as e:
            mensaje_error = f'Error al cargar archivo CSV: {e}'
            controlador.mostrarMensajeError(mensaje_error)
            return None, mensaje_error
        
    def obtenerArchivos(self, tipo=None, clave=None):
        query = 'SELECT id, clave, tipo, ruta FROM archivos'
        values = ()
        if tipo and clave:
            query += ' WHERE tipo = %s AND clave = %s'
            values = (tipo, clave)
        elif tipo:
            query += ' WHERE tipo = %s'
            values = (tipo,)
        elif clave:
            query += ' WHERE clave = %s'
            values = (clave,)
    
        cursor = self.__connection.cursor()
        cursor.execute(query, values)
        archivos = cursor.fetchall()
        cursor.close()
        return archivos
            
    def descargarArchivoMat(self, clave):
        archivos = self.obtenerArchivos(tipo='MAT', clave=clave)
        if archivos:
            archivo = archivos[0]  
            ruta = archivo[3]
            data = sio.loadmat(ruta)
            return data
        return None

    def descargarArchivoCsv(self, clave):
        archivos = self.obtenerArchivos(tipo='CSV', clave=clave)
        if archivos:
            archivo = archivos[0]  
            ruta = archivo[3]
            df = pd.read_csv(ruta)
            return df
        return None
    
    def eliminarArchivo(self, clave):
        try:
            archivos = self.obtenerArchivos(clave=clave)
            if archivos:
                archivo = archivos[0]
                with self.__connection.cursor() as cursor:
                    # Eliminar el archivo de la tabla 'archivos'
                    query_delete_archivo = 'DELETE FROM archivos WHERE clave = %s'
                    cursor.execute(query_delete_archivo, (clave,))
                    self.__connection.commit()

                    # Eliminar los datos asociados en la tabla 'datos_csv' o 'datos_mat'
                    if archivo[2] == 'CSV':
                        query_delete_datos_csv = 'DELETE FROM datos_csv WHERE archivo_id = %s'
                        cursor.execute(query_delete_datos_csv, (archivo[0],))
                        self.__connection.commit()
                    elif archivo[2] == 'MAT':
                        query_delete_datos_mat = 'DELETE FROM datos_mat WHERE archivo_id = %s'
                        cursor.execute(query_delete_datos_mat, (archivo[0],))
                        self.__connection.commit()

                return True  
            else:
                print("No se encontró el archivo con la clave especificada.")
                return False
        except Exception as e:
            print(f"Error al eliminar archivo: {e}")
            return False
  
class manejoUsuarios:
    def __init__(self):
        self.__username = ''
        self.__password = ''

    def ingreso(self, username:str, password:str):
        self.__username = username
        self.__password = password
        acceso = open('acceso.json', mode = 'r', encoding = 'utf8')
        a = json.load(acceso)
        acceso.close()
        if a[0]['usuario'] == self.__username and a[0]['contrasena'] == self.__password:
            return True
        return False
    
    def nuevousuario(self, username:str, password:str):
        self.__username = username
        self.__password = password
        def verificar_usuario_nuevo(usuario, datos):
            for entry in datos:
                if entry['usuario'] == usuario:
                    return False  # El usuario ya existe en el JSON
            return True

        def agregar_usuario(usuario, contraseña, datos):
            nuevo_usuario = {'usuario': usuario, 'contrasena': contraseña}
            datos.append(nuevo_usuario)

        # Leer el archivo JSON
        try:
            with open('acceso.json', 'r') as f:
                datos = json.load(f)
        except FileNotFoundError:
            datos = []

        # Verificar si el usuario ya existe
        if verificar_usuario_nuevo(self.__username, datos):
            # Agregar nuevo usuario
            agregar_usuario(self.__username, self.__password, datos)
            # Guardar los datos actualizados en el archivo JSON
            with open('acceso.json', 'w') as f:
                json.dump(datos, f, indent=4)
            return True
        return False
            
            

    def modificar(self, usernameviejo:str, passwordviejo:str ,username:str, password:str):
        if self.ingreso(usernameviejo, passwordviejo):
            self.__username = username
            self.__password = password
            with open('acceso.json', 'r+') as file:
                datos = json.load(file)
                usuario_encontrado = False
                for dic in datos:
                    if dic['usuario'] == usernameviejo:
                        dic['usuario'] = self.__username
                        dic['contrasena'] = self.__password
                        usuario_encontrado = True
                        break
                if usuario_encontrado:
                    file.seek(0)
                    json.dump(datos, file, ensure_ascii=False, indent=4)
                    file.truncate()
                    return True
                else:
                    return False

class manejoArchivos:
    def __init__(self):

