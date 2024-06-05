import mysql.connector
import json
import numpy as np
from pydicom.pixel_data_handlers.util import apply_modality_lut
import pydicom
from PyQt5.QtGui import QImage

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

########## PACIENTES ###############

    def validarPac(self, identificacion:str):
        query = 'SELECT * FROM pacientes WHERE identificacion = %s'
        cursor = self.__connection.cursor()
        cursor.execute(query, (identificacion,))
        results = cursor.fetchall()
        cursor.close()
        return len(results) == 0
            
    def ingresarPac(self, namepac:str, lastnamepac:str, agepac:str, idpac:str, medpac:str, url:str):
        if self.validarPac(idpac):
            query = 'INSERT INTO pacientes (nombre, apellido, edad, identificacion, med_cabecera, url) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            values = (namepac, lastnamepac, agepac, idpac, medpac, url)
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
    
    def editarPac(self, idpac:str, nueva_id:str, namepac:str, lastnamepac:str, agepac:str, medpac:str, url:str):
        # Verificar si la nueva ID ya existe
        if not self.validarPac(nueva_id):
            return False
        cursor = self.__connection.cursor()
        sql = "UPDATE pacientes SET identificacion = %s, nombre = %s, apellido = %s, edad = %s, med_cabecera = %s, url = %s WHERE identificacion = %s"
        val = (nueva_id, namepac, lastnamepac, agepac, medpac, url, idpac)
        cursor.execute(sql, val)
        self.__connection.commit()
        cursor.close()
        return True

    def lista_medicos(self):
        nombres_completos = []
        cursor = self.__connection.cursor()
        cursor.execute("SELECT CONCAT(nombre, ' ', apellido) FROM medicos ORDER BY nombre, apellido")
        resultados = cursor.fetchall()
        nombres_completos = [nombre[0] for nombre in resultados]
        cursor.close()
        return nombres_completos

    def paciente(self, identificacion:str):
        query = 'SELECT * FROM pacientes WHERE identificacion = %s'
        cursor = self.__connection.cursor()
        cursor.execute(query, (identificacion,))
        paciente = cursor.fetchone()
        cursor.close()
        namepac, lastnamepac, agepac, idpac, medpac, url, = self.paciente_variables(paciente)
        return namepac, lastnamepac, agepac, idpac, medpac, url

    def paciente_variables(tupla):
        if tupla:
            return tupla  # Si la tupla no está vacía, simplemente devuélvela
        else:
            return None  # Si la tupla está vacía, devuelve None

########## MEDICOS ###############

    def validarMed(self, identificacion:str):
        query = 'SELECT * FROM medicos WHERE identificacion = %s'
        cursor = self.__connection.cursor()
        cursor.execute(query, (identificacion,))
        results = cursor.fetchall()
        cursor.close()
        return len(results) == 0
            
    def ingresarMed(self, namemed:str, lastnamemed:str, agemed:str, num_registro:str, esp:str):
        if self.validarPac(num_registro):
            query = 'INSERT INTO medicos (nombre, apellido, edad, num_registro, especialidad) VALUES (%s, %s, %s, %s, %s, %s)'
            values = (namemed, lastnamemed, agemed, num_registro, esp)
            cursor = self.__connection.cursor()
            cursor.execute(query, values)
            self.__connection.commit()
            cursor.close()
            return True
        return False
        
    def eliminarMed(self, idmed:str):
        if self.validarPac(idmed) == None:
            return False
        else:             
            query = 'DELETE FROM medicos WHERE identificacion = %s'
            cursor = self.__connection.cursor()
            cursor.execute(query, (idmed,))
            self.__connection.commit()
            cursor.close()
            return True
    
    def editarMed(self, idmedc:str, nueva_id:str, namemed:str, lastnamemed:str, agemed:str, num_registro:str, esp:str):
        # Verificar si la nueva ID ya existe
        if not self.validarPac(nueva_id):
            return False
        cursor = self.__connection.cursor()
        sql = "UPDATE medicos SET identificacion = %s, nombre = %s, apellido = %s, edad = %s, num_registro = %s, especialidad = %s WHERE identificacion = %s"
        val = (nueva_id, namemed, lastnamemed, agemed, num_registro, esp, idmedc)
        cursor.execute(sql, val)
        self.__connection.commit()
        cursor.close()
        return True

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


    def _init_(self,path):
        self.dicom = pydicom.dcmread(self.path)
        self.path = path

    def apply_modality_lut(self): #funcion para hacer más visible/clara la imagen (contraste,brillo...)
        dm = self.dicom
        imagen = apply_modality_lut(dm.pixel_array, dm)

        if imagen.dtype != np.uint8: #normalicemos la imagen 
            imagen = (np.maximum(imagen, 0) / imagen.max()) * 255.0 
            imagen = np.uint8(imagen) #formato final np.uint8

        return QImage(imagen, imagen.shape[1], imagen.shape[0], QImage.Format_Grayscale8)
    #convertimos la imagen a QImage para verla en la ventana 
    #-pixeles-ancho(columnas)-altura(filas)-escala de grises

class manejodicom:
    def _init_(self):
        pass
        
    def dicom(path):
        return pydicom.dcmread(path)

    def apply_modality_lut(self): #funcion para hacer más visible/clara la imagen (contraste,brillo...)
        dm = self.dicom()
        imagen = apply_modality_lut(dm.pixel_array, dm)

        if imagen.dtype != np.uint8: #normalicemos la imagen 
            imagen = (np.maximum(imagen, 0) / imagen.max()) * 255.0 
            imagen = np.uint8(imagen) #formato final np.uint8

        return QImage(imagen, imagen.shape[1], imagen.shape[0], QImage.Format_Grayscale8)
    
    
    
    
    def __init__(self):
        pass  # Eliminamos los atributos del constructor

    def apply_modality_lut(self, pixel_array):
        # Aplicar el ajuste de contraste u otros ajustes según sea necesario
        imagen = pixel_array

        if imagen.dtype != np.uint8: #normalizamos la imagen 
            imagen = (np.maximum(imagen, 0) / imagen.max()) * 255.0 
            imagen = np.uint8(imagen) #formato final np.uint8

        # Convertir la imagen a QImage
        height, width = imagen.shape
        qimage = QImage(width, height, QImage.Format_Grayscale8)

        for y in range(height):
            for x in range(width):
                pixel_value = imagen[y][x]
                qimage.setPixel(x, y, qRgb(pixel_value, pixel_value, pixel_value))

        return qimage