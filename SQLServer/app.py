from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

db = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ADRIAN\SQLEXPRESS01;'
    'DATABASE=flask;'
    'Trusted_Connection=yes;'
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
        "INSERT INTO PERSONA (ci, nombre, apellido) VALUES (?, ?, ?);", (ci, nombre, apellido))
    db.commit()
    return redirect(url_for('index'))


@app.route('/eliminar/<int:ci>')
def eliminar(ci):
    cursor = db.cursor()
    print(ci)
    cursor.execute(
        "DELETE FROM PERSONA WHERE CI = ?;", (ci,))
    db.commit()
    return redirect(url_for('index'))


@app.route('/actualizar', methods=['POST'])
def actualizar():
    ci = request.form['ci']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cursor = db.cursor()
    cursor.execute(
        "UPDATE PERSONA SET nombre = ?, apellido = ? WHERE ci = ?;", (nombre, apellido, ci))
    db.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
