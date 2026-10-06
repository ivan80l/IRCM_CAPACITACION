from flask import Flask, request, redirect, render_template, url_for,flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'ClaveSecreta'

# Funcion para conectar la base de datos
def get_db_connection():
    conn = sqlite3.connect('sistema_medico.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route

@app.route('/')
def index():
    return redirect(url_for('medicos'))

@app.route('/medicos')
def medicos():
    conn = get_db_connection()
    medicos = conn.execute('SELECT * FROM medicos').fetchall()
    conn.close()
    return render_template('medicos.html', medicos=medicos)

@app.route('/pacientes')
def pacientes():
    conn = get_db_connection()
    pacientes = conn.execute('SELECT * FROM pacientes').fetchall()
    conn.close()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/consultas')
def consultas():
    conn = get_db_connection()
    consultas = conn.execute(
        """
        SELECT c.id, c.fecha || ' ' || c.hora AS fecha_hora, m.nombre AS nombre_medico, p.nombre AS nombre_paciente
        FROM consultas c 
        JOIN medicos m ON c.id_medico = m.id
        JOIN pacientes p ON c.id_paciente = p.id
        """
        )
    conn.close()
    return render_template('consultas.html', consultas=consultas)

if __name__ == '__main__':
    app.run(debug=True)