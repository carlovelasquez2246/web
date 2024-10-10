'''class todos_los_cursos:
    def __init__(self, CursoID, NombreCurso, Centro, Servicio, TipoServicio, FechaInicio, FechaEntrada, ProfesorID ): 
        self.CursoID = CursoID
        self.NombreCurso = NombreCurso
        self.Centro = Centro
        self.Servicio = Servicio
        self.TipoServicio = TipoServicio
        self.FechaInicio = FechaInicio
        self.FechaEntrada = FechaEntrada
        self.ProfesorID = ProfesorID
        '''
'''@staticmethod'''

"estudiantes.EstudianteID, estudiantes.dniEstudiante, estudiantes.Nombre, estudiantes.Apellido1"



'''@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        cursoID = request.form['id']
        db.delete_curso(cursoID)
        return redirect(url_for('index'))
        
    curso = db.Cursos_all()
    return render_template('index.html' , curso = curso)

@app.route('/personas', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        EstudianteID = request.form['id']
        db.delete_estudiantes(EstudianteID)
        return redirect(url_for('index'))
        
    estudiantes = db.Read_estudiantes()
    return render_template('index.html' , estudiantes = estudiantes)
'''

'''@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        cursoID = request.form['id']
        EstudianteID = request.form['id']
 
        if cursoID:
           db.delete_estudiantes(EstudianteID)
        if EstudianteID:   
           db.delete_curso(cursoID)
           
        return jsonify({'status': 'success', 'message': 'Elemento eliminado correctamente'})

        
    curso = db.Cursos_all()
    estudiantes = db.Read_estudiantes()
 '''
'''
CREATE TABLE imagenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_imagen VARCHAR(255),
    datos_imagen LONGBLOB
);



def guardar_imagen_en_base_de_datos(nombre_imagen, ruta_imagen):
    try:
        # Conectar a la base de datos
        conn = get_connection()
        cursor = conn.cursor()

        # Leer el archivo de imagen en modo binario
        with open(ruta_imagen, 'rb') as file:
            imagen_binaria = file.read()

        # Insertar en la base de datos
        cursor.execute('''
            INSERT INTO imagenes (nombre_imagen, datos_imagen) 
            VALUES (%s, %s)'''
        ''' ''', (nombre_imagen, imagen_binaria))

        # Confirmar la transacción
        conn.commit()

        print("Imagen guardada correctamente en la base de datos.")

    except db.Error as err:
        conn.rollback()
        print(f"Error al guardar la imagen: {err}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

             pdf.cell(200, 10, txt=f"ID: {dato[0]},             Nombre: {dato[1]}", ln=True)
                
        pdf.cell(200, 10, txt=f"Nº Expediente: {dato[0]}", ln=True)
        pdf.cell(200, 10, txt=f"Nombre: {dato[1]}", ln=True)
        pdf.cell(200, 10, txt=f"Apellidos: {dato[2]}", ln=True)
        pdf.cell(200, 10, txt=f"DNI/NIE: {dato[3]}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha Nacimiento: {dato[4]}", ln=True)
        pdf.cell(200, 10, txt=f"Dirección: {dato[5]}", ln=True)
        pdf.cell(200, 10, txt=f"Población: {dato[6]}", ln=True)
        pdf.cell(200, 10, txt=f"Código Postal: {dato[7]}", ln=True)
        pdf.cell(200, 10, txt=f"Teléfono: {dato[8]}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {dato[9]}", ln=True)


           pdf.cell(200, 10, txt=f"Nº Expediente: {dato[8]}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.set_xy(10, 10)  # Coloca el texto a 10mm del borde izquierdo y 10mm del borde superior
        pdf.cell(200, 10, txt="Formulario de Inscripción", ln=True, align='C')

        



        from flask import Flask, render_template, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mariadb
import sys

app = Flask(__name__)

try:
    conn = mariadb.connect(
        user="tu_usuario",
        password="tu_contraseña",
        host="localhost",
        port=3306,
        database="tu_base_de_datos"
    )
except mariadb.Error as e:
    print(f"Error conectando a MariaDB: {e}")
    sys.exit(1)

cur = conn.cursor()

@app.route('/')
def index():
    cur.execute("SELECT * FROM tu_tabla")
    datos = cur.fetchall()
    return render_template('documento.html', datos=datos)

@app.route('/generar_pdf')
def generar_pdf():
    cur.execute("SELECT * FROM tu_tabla")
    datos = cur.fetchall()

    response = make_response()
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=documento.pdf'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Datos desde MariaDB")
    y = height - 150

    for dato in datos:
        c.drawString(100, y, f"ID: {dato[0]}, Nombre: {dato[1]}")
        y -= 20

    c.showPage()
    c.save()

    return response

if __name__ == '__main__':
    app.run(debug=True)

    

# Cadena hexadecimal
hex_string = "44554e4954454159584748373433354d56365f522e6a7067"

# Decodificar a texto
decoded_string = bytes.fromhex(hex_string).decode('utf-8')

print(decoded_string)  # Esto imprimirá: DUNITAXYGH7435MV6_R.jpg

@app.route('/edit_alumno/<int:id>', methods=['GET', 'POST'])
def edit_alumno(id): 
    alumno = db.read_estudiante_id(id)  # Obtener los datos actuales del alumno
    
    if request.method == 'POST':
        dniEstudiante     = request.form['dni']
        Nombre            = request.form['name']
        Apellido1         = request.form['last1']
        Apellido2         = request.form['last2']
        FechaDeNacimiento = request.form['date_birt']
        CorreoElectronico = request.form['email']
        Sexo              = request.form['sexinput']
        TipoDocuemento    = request.form['type_id']
        paisOrigen        = request.form['ori_country']
        Nacionalidad      = request.form['nationality']
        direccion         = request.form['addres']
        CodigoPostal      = request.form['cp']
        Telefono          = request.form['phont']
        Notas             = request.form['grade'] 
        CursoID           = request.form['idcursoinput']
        FechaInscripcion  = request.form['registration_date']

        # Verificar si se subió una nueva foto
        if 'foto' in request.files and request.files['foto'].filename != '':
            file = request.files['foto']
            newNameFaile = recibeFoto(file)  # Procesar la nueva imagen
        else:
            newNameFaile = alumno[17]  # Mantener la imagen actual

        # Actualizar el estudiante en la base de datos
        db.update_estudiante(id, dniEstudiante, Nombre, Apellido1, Apellido2, FechaDeNacimiento, 
                             CorreoElectronico, Sexo, TipoDocuemento, paisOrigen, Nacionalidad, 
                             direccion, CodigoPostal, Telefono, Notas, CursoID, 
                             FechaInscripcion, newNameFaile)
        
        return redirect(url_for('index'))

    # Si es un método GET, mostrar el formulario con los datos actuales
    return render_template('edit_alumno.html', alumno=alumno)


'''

'''
@app.route('/generar_pdf/<int:id>', methods=['GET', 'POST'])
def generar_pdf(id):
    datos = db.descargar_pdf(id)

    if not datos:
        return "No se encontraron datos para generar el PDF", 404

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="FICHAS CLARA", ln=True, align='C')

    logo_path = "static/img/logo_adsis.jpg"  # Ruta a la imagen del logo
    pdf.image(logo_path, x=10, y=8, w=60, h=35)

    for dato in datos:
        photo_path = os.path.join('static', 'fotos_Estudiantes', f"{dato[14]}")  # Ajustar la ruta

        # Verificar si la foto del estudiante existe antes de intentar insertarla
        if os.path.exists(photo_path):
            try:
                pdf.image(photo_path, x=150, y=8, w=40, h=50)  # Ajustar posición y tamaño
            except RuntimeError as e:
                pdf.set_xy(150, 8)
                pdf.set_font("Arial", size=10)
                pdf.cell(40, 10, txt="Foto no válida", border=0)
        else:
            pdf.set_xy(150, 8)
            pdf.set_font("Arial", size=10)
            pdf.cell(40, 10, txt="Foto no disponible", border=0)

        # Resto del contenido del PDF...
        # Aquí mantienes el mismo formato que tienes para los datos.

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=documento.pdf'

    return response
'''

