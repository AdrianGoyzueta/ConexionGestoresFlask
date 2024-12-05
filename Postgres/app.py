from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

db = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="",
    database="flask"
)

@app.route('/', methods=['GET'])
def index():
    cursor = db.cursor()
    cursor.execute("SELECT ci, nombre, apellido FROM PERSONA;")
    data = cursor.fetchall()
    return render_template('index.html', data=data)


@app.route('/insertar', methods=['POST'])
def insertar():
    ci = request.form['ci']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO PERSONA (ci, nombre, apellido) VALUES (%s, %s, %s);", (ci, nombre, apellido))
    db.commit()
    return redirect(url_for('index'))


@app.route('/eliminar/<int:ci>')
def eliminar(ci):
    cursor = db.cursor()
    print(ci)
    cursor.execute(
        "DELETE FROM PERSONA WHERE CI = %s;", (ci,))
    db.commit()
    return redirect(url_for('index'))


@app.route('/actualizar', methods=['POST'])
def actualizar():
    ci = request.form['ci']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cursor = db.cursor()
    cursor.execute(
        "UPDATE PERSONA SET nombre = %s, apellido = %s WHERE ci = %s;", (nombre, apellido, ci))
    db.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
