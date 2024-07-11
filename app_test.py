from flask import Flask
from flask import render_template, redirect, request
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os

app = Flask(__name__)
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistema'
mysql.init_app(app) 

@app.route("/")
def index():
    sql = "SELECT * FROM `sistema`.`empleados`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    db_empleados = cursor.fetchall()
    conn.commit()
    return render_template("empleados/index.html", empleados = db_empleados)

@app.route("/create")
def create():
    return render_template("empleados/create.html")

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename !="":
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    datos = (_nombre, _correo, nuevoNombreFoto)
    sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    conn = mysql.connect() # Nos conectamos a la base de datos
    cursor = conn.cursor() # En cursor vamos a realizar las operaciones
    cursor.execute(sql, datos) # Ejecutamos la sentencia SQL en el cursor
    conn.commit() # Hacemos el commit
    return redirect('/') # Volvemos a index.html

@app.route("/destroy/<int:id>")
def destroy(id):
    sql = "DELETE FROM `sistema`.`empleados` WHERE id = %s"
    conn = mysql.connect()
    cursor = conn.cursor()

    # Prueba para borrar fotos de carpeta
    cursor.execute("SELECT `foto` FROM `sistema`.`empleados` WHERE `id` = %s", id)
    fila= cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    conn.commit()
    # Fin de prueba para borrar fotos de carpeta

    cursor.execute(sql, id)
    conn.commit()
    return redirect('/')

@app.route("/edit/<int:id>")
def edit(id):
    sql = "SELECT * FROM `sistema`.`empleados` WHERE id = %s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    _id=request.form['txtID']
    sql = "UPDATE `sistema`.`empleados` SET `nombre` = %s, `correo` = %s WHERE `id` = %s;"
    datos=(_nombre, _correo, _id)
    conn = mysql.connect()
    cursor = conn.cursor()
    now = datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)
        cursor.execute("SELECT `foto` FROM `sistema`.`empleados` WHERE `id` = %s", _id)
        fila= cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE `sistema`.`empleados` SET `foto` = %s WHERE `id` = %s;", (nuevoNombreFoto, _id))
        conn.commit()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

@app.route('/uploads/<nuevoNombreFoto>')
def uploads(nuevoNombreFoto):
    return send_from_directory(app.config['CARPETA'], nuevoNombreFoto)

if __name__ == "__main__":
    app.run(debug = True)