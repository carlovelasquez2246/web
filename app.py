from flask import Flask, request, render_template, redirect, url_for, make_response, jsonify
import MariaDB as db
from fpdf import FPDF
from PIL import Image

#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 
'''from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys
'''
'''pip install reportlab
    pip install Pillow

'''

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        cursoID = request.form['id']
        db.delete_curso(cursoID)
        return redirect(url_for('index'))
        
    curso = db.Cursos_all()
    alumnos = db.Read_estudiantes()
    return render_template('index.html' , cursos = curso , estudiantes = alumnos)

@app.route('/eliminar_lista', methods=['GET', 'POST'])
def eliminar_lista():
    if request.method == 'POST':
        alumno = request.form['id']
        db.delete_estudiantes(alumno)
        return redirect(url_for('index'))

    curso = db.Cursos_all()    
    alumnos = db.Read_estudiantes()
    return render_template('index.html', estudiantes=alumnos, cursos = curso)        

@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    if request.method == 'POST':
        alumno       = request.form['id'] 
        foto         = request.form['foto'] 
        db.delete_estudiantes(alumno)
        
        basepath = os.path.dirname (__file__) 
        url_File = os.path.join (basepath , 'static\\fotos_Estudiantes' , foto)
        '''os.remove(url_File)'''
        if os.path.exists(url_File):
            os.remove(url_File)
        else:
            print("la foto no se pudo eliminar")    
            return redirect(url_for('index'))
        
    curso = db.Cursos_all()    
    alumnos = db.Read_estudiantes()
    return render_template('index.html', estudiantes=alumnos, cursos = curso)


@app.route('/add_curso', methods=['GET', 'POST'])
def add_curso():
    if request.method == 'POST':
        NombreCurso = request.form['name']
        Centro = request.form['center']
        Servicio = request.form['serviceinput']
        TipoServicio = request.form['type_serviceinput']
        FechaInicio = request.form['start_date']
        FechaEntrada = request.form['entry_date']
        ProfesorID = request.form['teacherinput']
        db.create_curso(NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID)
        return redirect(url_for('index'))
    
    return render_template('add_curso.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_curso(id): 
    
    if request.method == 'POST':
        NombreCurso = request.form['name']
        Centro = request.form['center']
        Servicio = request.form['serviceinput']
        TipoServicio = request.form['type_serviceinput']
        FechaInicio = request.form['start_date']
        FechaEntrada = request.form['entry_date']
        ProfesorID = request.form['teacherinput']
        db.update_curso(id, NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID)
        return redirect(url_for('index'))
    
    curso = db.Cursos_all_id(id)
    return render_template('edit_curso.html', curso=curso)


@app.route('/add_alumno', methods=['GET', 'POST'])
def add_alumno():
    if request.method == 'POST':
        dniEstudiante     = request.form['dni']
        Nombre            = request.form['name']
        Apellido1         = request.form['last1']
        Apellido2         = request.form['last2']
        FechaDeNacimiento = request.form['date_birt']
        CorreoElectronico = request.form['email']
        Sexo              = request.form['sexinput']
        TipoDocuemento    = request.form['type_idinput']
        paisOrigen        = request.form['ori_country']
        Nacionalidad      = request.form['nationality']
        direccion         = request.form['addres']
        CodigoPostal      = request.form['cp']
        Telefono          = request.form['phont']

        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            newNameFaile = recibeFoto(file) #Llamado la funcion que procesa la imagen
            db.create_estudiante(dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, newNameFaile)
            return redirect(url_for('index'))
    
    return render_template('add_alumno.html')
            
@app.route('/edit_alumno/<int:id>', methods=['GET', 'POST'])
def edit_alumno(id): 
    
    if request.method == 'POST':
        dniEstudiante     = request.form['dni']
        Nombre            = request.form['name']
        Apellido1         = request.form['last1']
        Apellido2         = request.form['last2']
        FechaDeNacimiento = request.form['date_birt']
        CorreoElectronico = request.form['email']
        Sexo              = request.form['sexinput']
        TipoDocuemento    = request.form['type_idinput']
        paisOrigen        = request.form['ori_country']
        Nacionalidad      = request.form['nationality']
        direccion         = request.form['addres']
        CodigoPostal      = request.form['cp']
        Telefono          = request.form['phont']
        Notas             = request.form['gradeinput'] 
        CursoID           = request.form['idcursoinput']
        FechaInscripcion  = request.form['registration_date']

        if 'foto' in request.files and request.files['foto'].filename != '':
            file     = request.files['foto'] #recibiendo el archivo
            newNameFaile = recibeFoto(file) #Llamado la funcion que procesa la imagen  
        else:
            newNameFaile = request.form['foto']

        db.update_estudiante(id ,dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, 
                                 Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, Notas, 
                                 CursoID, FechaInscripcion, newNameFaile)
        return redirect(url_for('index'))
    
    alumno = db.read_estudiante_id(id)
    return render_template('edit_alumno.html', alumno=alumno)

@app.route('/listado/<id>', methods=['GET', 'POST'])
def listado(id):   
    dato = db.ver_lista(id)
    return render_template('ver_lista.html', listar = dato)

@app.route('/resumen', methods=['GET', 'POST'])
def resumen():
    resumen= db.resumen()
    return render_template('resumen.html', resumen=resumen)
      
@app.route('/reportNacional', methods=['GET', 'POST'])
def reportNacional():
    nacional= db.nacionalidad()
    return render_template('reporteNacionalidad.html', nacionalidad=nacional)

@app.route('/inscribir', methods=['GET', 'POST'])
def inscribir():
    if request.method == 'POST':
        dniEstudiante     = request.form['dni']
        Nombre            = request.form['name']
        Apellido1         = request.form['last1']
        Apellido2         = request.form['last2']
        FechaDeNacimiento = request.form['date_birth']
        CorreoElectronico = request.form['email']
        Sexo              = request.form['sexinput']
        TipoDocuemento    = request.form['type_idinput']
        paisOrigen        = request.form['ori_country']
        Nacionalidad      = request.form['nationality']
        direccion         = request.form['addres']
        CodigoPostal      = request.form['cp']
        Telefono          = request.form['phont']
        Notas             = request.form['gradeinput'] 
        CursoID           = request.form['idcursoinput']
        FechaInscripcion  = request.form['registration_date']

        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            newNameFaile = recibeFoto(file) #Llamado la funcion que procesa la imagen
        db.inscribirEstudiante(dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, direccion, CodigoPostal, Telefono, Notas, CursoID, FechaInscripcion, newNameFaile)
        return redirect(url_for('index'))
    
    return render_template('inscribirAlumno.html')



@app.route('/generar_pdf/<int:id>', methods=['GET', 'POST'])
def generar_pdf(id):
    datos = db.descargar_pdf(id)

    if not datos:
        return "No se encontraron datos para generar el PDF", 404

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    

    logo_path = "static/img/logo_adsis.jpg"  # Ruta a la imagen del logo
    pdf.image(logo_path, x=10, y=8, w=60, h=40)  # Insertar imagen. Ajustar 'x', 'y', 'w', 'h' para posición y tamaño

    '''logo_path1 = "static/fotos_Estudiantes/5WKECH4MAJ_GORI9UFB2.jpg"  # Ruta a la imagen del logo
    pdf.image(logo_path1, x=150, y=8, w=40, h=50)  # Insertar imagen. Ajustar 'x', 'y', 'w', 'h' para posición y tamaño
'''
    for dato in datos:
        
        photo_path = os.path.join('static', 'fotos_Estudiantes', f"{dato[14]}")  # Suponiendo que la foto está en formato JPG
    
        # Verificar si la foto del estudiante existe antes de intentar insertarla
        if os.path.exists(photo_path):
            try:
                # Abrir la imagen con Pillow y convertirla a formato JPG si no lo es
                img = Image.open(photo_path)
                if img.format != 'JPEG':
                    jpg_photo_path = os.path.join('static', 'fotos_Estudiantes', 'temp_image.jpg')
                    img = img.convert('RGB')  # Convertir a RGB si es necesario
                    img.save(jpg_photo_path, format='JPEG')
                    pdf.image(jpg_photo_path, x=150, y=8, w=35, h=40)
                else:
                    pdf.image(photo_path, x=150, y=8, w=35, h=40)
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
                pdf.set_xy(150, 8)
                pdf.set_font("Arial", size=10)
                pdf.cell(40, 10, txt="Foto no disponible", border=0)
        else:
            pdf.set_xy(150, 8)
            pdf.set_font("Arial", size=10)
            pdf.cell(40, 10, txt="Foto no disponible", border=0)


        # Nº Expediente
        pdf.set_xy(10, 50)  # Coordenadas para el texto del número de expediente
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Nº Expediente:", border=0)
        pdf.set_xy(45, 50)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[0]}", border=0)  # Ejemplo de un número de expediente


        # Especialidad
        pdf.set_xy(90, 50)  # Coordenadas para el campo de especialidad (más a la derecha)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Especialidad:", border=0)
        pdf.set_xy(120, 50)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[1]}" ,  border=0)  # Ejemplo de especialidad

        # Nombre
        pdf.set_xy(10, 60)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Nombre:", border=0)
        pdf.set_xy(45, 60)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[2]}", border=0)  # Ejemplo de un nombre

        # Apellidos y DNI/NIE
        pdf.set_xy(10, 70)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Apellidos:", border=0)
        pdf.set_xy(45, 70)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[3]} {dato[4]}" , border=0)  # Ejemplo de apellidos

        pdf.set_xy(110, 70)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="DNI/NIE:", border=0)
        pdf.set_xy(150, 70)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[5]}" , border=0)  # Ejemplo de DNI/NIE

        # Lugar y Fecha de Nacimiento
        pdf.set_xy(10, 80)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Lugar Nacimiento:", border=0)
        pdf.set_xy(50, 80)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[6]}", border=0)  # Ejemplo de lugar de nacimiento

        pdf.set_xy(110, 80)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Fecha Nacimiento:", border=0)
        pdf.set_xy(150, 80)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[7]}" ,border=0)  # Ejemplo de fecha de nacimiento

        # Dirección
        pdf.set_xy(10, 90)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Dirección:", border=0)
        pdf.set_xy(45, 90)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[8]}", border=0)  # Ejemplo de dirección

        # Población y Código Postal
        pdf.set_xy(10, 100)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Codigo Postal:", border=0)
        pdf.set_xy(45, 100)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[9]}" , ln=True, border=0)  # Ejemplo de población

        pdf.set_xy(110, 90)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Telefono Alno:", border=0)
        pdf.set_xy(150, 90)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[10]}", ln=True, border=0)  # Ejemplo de código postal

        # Teléfono y Email
        pdf.set_xy(10, 110)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Email Alumno:", border=0)
        pdf.set_xy(45, 110)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[11]}", ln=True, border=0)  # Ejemplo de teléfono

        pdf.set_xy(110, 100)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Curso Inicio:", border=0)
        pdf.set_xy(150, 100)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"{dato[12]}" , ln=True, border=0)  # Ejemplo de email

        pdf.set_xy(10, 120)
        pdf.set_font("Arial", size=13)
        pdf.cell(40, 10, txt="Fecha Entrada", border=0)
        pdf.set_xy(45, 120)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt= f"{dato[13]}"  , ln=True, border=0)  # Ejemplo de email


        # Guardar el PDF en un archivo local
    '''pdf.output("formulario_relleno.pdf")'''

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=documento.pdf'

    return response


def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = db.stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/fotos_Estudiantes', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile
 
  

if __name__ == '__main__':
    app.run(debug=True)

      




