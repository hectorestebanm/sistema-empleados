from flask import Flask
from flask import render_template, redirect, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='integrador_cac'
mysql.init_app(app) 

@app.route("/")
def index():
    sql = "INSERT INTO `integrador_cac`.`oradores` (`id_orador`, `nombre`, `apellido`, `mail`, `tema`, `fecha_alta`) VALUES (NULL, 'Ana Maria', 'Paez', 'anamaria@gmail.com', 'python', '2024-06-28');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template("empleados/index.html")

@app.route("/create")
def create():
    return render_template("empleados/create.html")

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _correo = request.form['txtCorreo']
    _tema = request.form['txtTema']
    _fecha = request.form['txtFecha']

    datos = (_nombre, _apellido, _correo, _tema, _fecha)

    sql = "INSERT INTO `integrador_cac`.`oradores` (`id_orador`, `nombre`, `apellido`, `mail`, `tema`, `fecha_alta`) VALUES (NULL, %s, %s, %s, %s, %s);"
    conn = mysql.connect() # Nos conectamos a la base de datos
    cursor = conn.cursor() # En cursor vamos a realizar las operaciones
    cursor.execute(sql, datos) # Ejecutamos la sentencia SQL en el cursor
    conn.commit() # Hacemos el commit
    return render_template('empleados/index.html') # Volvemos a index.html

if __name__ == "__main__":
    app.run(debug = True)