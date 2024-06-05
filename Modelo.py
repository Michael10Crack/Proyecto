import mysql.connector
import json
import pandas as pd
import scipy.io as sio
import numpy as np
from pydicom.pixel_data_handlers.util import apply_modality_lut
import pydicom
from PyQt5.QtGui import QImage
#
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

    def nombre_com(self):
        cursor = self.__connection.cursor()
        cursor.execute("SELECT CONCAT(nombre, ' ', apellido) FROM medicos ORDER BY nombre, apellido")
        resultados = cursor.fetchall()
        self.nombres_completos = [nombre[0] for nombre in resultados]
        cursor.close()
        return 


  
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
SERVER = 'localhost'
USER = 'admin123'
PASSWORD = 'contrasena123'
DB = 'database'

conexion = mysql.connector.connect(user=USER , password=PASSWORD , host=SERVER , database=DB)

cursor = conexion.cursor()
class manejodicom:
    def __init__(self,path):
        self.dicom = pydicom.dcmread(self.path)
        self.path = path

    def apply_modality_lut(self):
        dm = self.dicom
        imagen = apply_modality_lut(dm.pixel_array, dm)

        if imagen.dtype != np.uint8:
            imagen = (np.maximum(imagen, 0) / imagen.max()) * 255.0
            imagen = np.uint8(imagen)

        return QImage(imagen, imagen.shape[1], imagen.shape[0], QImage.Format_Grayscale8)

    def get_info_paciente(self):
        dm = self.dicom
        nombre = dm.get('PatientName', 'Desconocido')
        id_paciente = dm.get('PatientID', 'Desconocido')
        edad = dm.get('PatientAge', 'Desconocida')
        identificacion = dm.get('identificacion', 'Desconocido')
        med_cabecera = dm.get('med_cabecera', 'Desconocido')
        return nombre, id_paciente, edad, identificacion, med_cabecera
    
    def insert_patient_data(self):
        cursor = self.__connection.cursor()
        patient_info = self.get_info_paciente()
        insertarinfo = 'INSERT INTO pacientes(nombre, apellido, edad, identifiacion, med_cabecera) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(insertarinfo, patient_info)
        conexion.commit()


