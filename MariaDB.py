import mysql.connector as db
from random import sample
import os

def get_connection():
    return db.connect(
        host = "localhost",
        port = "3305",
        user = "root",
        password = "12345",
        database = "adsis"
        )

def Cursos_all():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT cu.CursoID, 
                       cu.NombreCurso, 
                       cu.Centro, 
                       cu.Servicio, 
                       cu.TipoServicio, 
                       cu.FechaInicio, 
                       cu.FechaEntrada,
                       pf.Nombre
                       FROM cursos cu
                       JOIN profesores pf ON cu.ProfesorID=pf.ProfesorID''')
        cursos = cursor.fetchall()
        return cursos
    except db.Error as err:
        print(f"Error al leer los CURSOS: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 

def Cursos_all_id(CursoID):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cursos WHERE CursoID = %s', (CursoID,))
        curso = cursor.fetchone()
        return curso
    except db.Error as err:
        print(f"Error al leer el CURSO: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()              



def create_curso(NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO Cursos (NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID) 
                           VALUES(%s, %s, %s, %s, %s, %s, %s)''', (NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID))
        conn.commit()            
    except db.Error as err:
        print(f'Error al ingresar curso: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()


def update_curso(id, NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(''' UPDATE cursos 
                           SET NombreCurso = %s , Centro = %s, Servicio = %s, TipoServicio = %s, FechaInicio = %s, FechaEntrada = %s, ProfesorID = %s
                           WHERE CursoID = %s''', (NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID, id))
        conn.commit()            
    except db.Error as err:
        print(f'Error al actualizar curso: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()


def delete_curso(CursoID):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE CursoID = %s", (CursoID,))
        conn.commit()         
    except db.Error as err:
        print(f'Error al Eliminar el Curso: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()

def Read_estudiantes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estudiantes")
        estudiante = cursor.fetchall()
        return estudiante             
    except db.Error as err:
        print(f'Error al listar Estudiantes: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_estudiante(dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, newNameFaile):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO estudiantes (dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, foto) 
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, newNameFaile))
        conn.commit()            
    except db.Error as err:
        print(f'Error al ingresar el Estudiante: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()            


def read_estudiante_id(EstudianteID):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT estudiantes.EstudianteID,
                       estudiantes.dniEstudiante,
			estudiantes.Nombre,
			estudiantes.Apellido1,
			estudiantes.Apellido2,
			estudiantes.FechaDeNacimiento,
			estudiantes.CorreoElectronico,
			estudiantes.Sexo,
			estudiantes.TipoDocuemento,
			estudiantes.paisOrigen,
			estudiantes.Nacionalidad,
			estudiantes.direccion,
			estudiantes.CodigoPostal,
			estudiantes.Telefono,
			inscripciones.Notas,
			inscripciones.CursoID,
			inscripciones.FechaInscripcion,
			estudiantes.foto
            FROM estudiantes 
            JOIN inscripciones
            ON inscripciones.EstudianteID=estudiantes.EstudianteID
            WHERE estudiantes.EstudianteID=  %s ''', (EstudianteID,))
        alumno = cursor.fetchone()
        return alumno
    except db.Error as err:
        print(f"Error al leer el CURSO: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()              


def delete_estudiantes(EstudianteID):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE EstudianteID = %s", (EstudianteID,))     

        conn.commit()   

    except db.Error as err:
        print(f'Error al Eliminar Estudiantes: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()

def ver_lista(CursoID):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT inscripciones.CursoID,estudiantes.EstudianteID, estudiantes.dniEstudiante, estudiantes.Nombre, estudiantes.Telefono, estudiantes.foto
                          FROM estudiantes 
                          JOIN inscripciones ON inscripciones.EstudianteID=estudiantes.EstudianteID 
                          WHERE inscripciones.CursoID=%s;''', (CursoID,))
        cursos = cursor.fetchall()
        return cursos
    except db.Error as err:
        print(f"Error al leer LA LISTA DEL CURSO: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def resumen():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM resumen')
        cursos = cursor.fetchall()
        return cursos
    except db.Error as err:
        print(f"Error al leer los resumenes: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 

def nacionalidad():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT DISTINCT es.Nacionalidad, COUNT(es.EstudianteID) AS TOTAL, SUM(es.Sexo='Femenino') AS MUJ, 
                          (SUM(cu.CursoID='1')+SUM(cu.CursoID='3')+SUM(cu.CursoID='5')) AS 1er_CURSO,
                          (SUM(cu.CursoID='1' AND es.Sexo='Femenino')+SUM(cu.CursoID='3' AND es.Sexo='Femenino')+SUM(cu.CursoID='5' AND es.Sexo='Femenino')) AS 1er_CURSO_MUJ,
                          (SUM(cu.CursoID='2')+SUM(cu.CursoID='4')+SUM(cu.CursoID='6')) AS 2º_CURSO,
                          (SUM(cu.CursoID='2' AND es.Sexo='Femenino')+SUM(cu.CursoID='4' AND es.Sexo='Femenino')+SUM(cu.CursoID='6' AND es.Sexo='Femenino')) AS 2º_CURSO_MUJ
                          FROM estudiantes es 
                          JOIN inscripciones ins ON ins.EstudianteID=es.EstudianteID
                          JOIN cursos cu ON cu.CursoID=ins.CursoID 
                          GROUP BY es.Nacionalidad''')
        cursos = cursor.fetchall()
        return cursos
    except db.Error as err:
        print(f"Error al leer los reportes de nacionalidad: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()   
    

def inscribirEstudiante(dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, Notas, CursoID, FechaInscripcion, foto):
    try:
        # Conexión a la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        # 1. Insertar en la tabla 'estudiantes'
        cursor.execute(''' 
            INSERT INTO estudiantes (dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, foto) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, foto))

        # Confirmar la transacción
        
        conn.commit()
        
        EstudianteID = cursor.lastrowid
        # 2. Insertar en la tabla 'inscripciones' utilizando 'dniEstudiante' como referencia
        cursor.execute('''
               INSERT INTO Inscripciones (EstudianteID, Notas, CursoID, FechaInscripcion)
               VALUES (%s, %s, %s, %s)''', (EstudianteID , Notas, CursoID, FechaInscripcion))

        # Confirmar la transacción
        conn.commit()

    except db.Error as err:
        print(f'Error al inscribir al esTudiante: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_estudiante(id ,dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, Notas, CursoID, FechaInscripcion, newNameFaile):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(''' UPDATE estudiantes 
                           SET dniEstudiante = %s , Nombre = %s, Apellido1 = %s, Apellido2 = %s, FechaDeNacimiento = %s, CorreoElectronico = %s, Sexo = %s, TipoDocuemento = %s, paisOrigen = %s, Nacionalidad = %s, direccion = %s, CodigoPostal = %s, Telefono = %s, foto = %s
                           WHERE EstudianteID = %s''', (dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, newNameFaile, id))
        conn.commit()   

        EstudianteID = id
        # 2. Insertar en la tabla 'inscripciones' utilizando 'dniEstudiante' como referencia
        cursor.execute('''
               UPDATE Inscripciones 
               SET  Notas = %s, CursoID = %s, FechaInscripcion = %s
               WHERE EstudianteID = %s''', (Notas, CursoID, FechaInscripcion, EstudianteID))

        # Confirmar la transacción
        conn.commit()        
    except db.Error as err:
        print(f'Error al actualizar curso: {err}')
    finally:    
        if conn.is_connected():
            cursor.close()
            conn.close()

def descargar_pdf(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT es.dniEstudiante, 
                                 cu.NombreCurso, 
                                 es.Nombre, 
                                 es.Apellido1, 
                                 es.Apellido2, 
                                 es.dniEstudiante, 
                                 es.paisOrigen, 
                                 es.FechaDeNacimiento, 
                                 es.direccion, 
                                 es.CodigoPostal, 
                                 es.Telefono, 
                                 es.CorreoElectronico, 
                                 cu.FechaInicio, 
                                 cu.FechaEntrada,
                                 es.foto
                       FROM estudiantes es
                       JOIN inscripciones ins ON  es.EstudianteID=ins.EstudianteID
                       JOIN cursos cu ON cu.CursoID=ins.CursoID
                       WHERE es.EstudianteID= %s''', (id,))
        alumno = cursor.fetchall()
        return alumno
    except db.Error as err:
        print(f"Error al leer el CURSO: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 


#Crear un string aleatorio para renombrar la foto 
# y evitar que exista una foto con el mismo nombre
def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio    


def show_photo(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT es.Nombre, es.foto FROM estudiantes es WHERE es.EstudianteID = %s', (student_id,))
        Photo = cursor.fetchone()
        return Photo
        
    except db.Error as err:
        print(f"Error al Mostrar la Foto: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 