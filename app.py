from flask import Flask, request, redirect, render_template, url_for,flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'ClaveSecreta'

# Funcion para conectar la base de datos
def get_db_connection():
    conn = sqlite3.connect('sistema_medico.db')
    conn.row_factory = sqlite3.Row
    return conn

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
@app.route("/nuevo_paciente", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        #leer contenido del formulario
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        fecha_nacimiento = request.form["fecha_nacimiento"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO pacientes (nombre, email, telefono, fecha_nacimiento) VALUES (?, ?, ?, ?)",
            (nombre, email, telefono, fecha_nacimiento)
        )
        conn.commit()
        conn.close()
        flash("Paciente agregado exitosamente.", "success")
        return redirect(url_for("pacientes"))
    return render_template("formulario_pacientes.html")
@app.route("/paciente/editar/<int:id_paciente>", methods=["GET", "POST"])
def editar_paciente(id_paciente):
    conn = get_db_connection()
    paciente = conn.execute("SELECT * FROM pacientes WHERE id_paciente = ?", (id_paciente,)).fetchone()
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        fecha_nacimiento = request.form["fecha_nacimiento"]

        conn.execute(
            "UPDATE pacientes SET nombre = ?, email = ?, telefono = ?, fecha_nacimiento = ? WHERE id_paciente = ?",
            (nombre, email, telefono, fecha_nacimiento, id_paciente)
        )
        conn.commit()
        conn.close()
        flash("Paciente actualizado exitosamente.", "success")
        return redirect(url_for("pacientes"))

    return render_template("formulario_pacientes.html", paciente=paciente)
@app.route("/paciente/eliminar/<int:id_paciente>")
def eliminar_paciente(id_paciente):
    conn = get_db_connection()
    conn.execute("DELETE FROM pacientes WHERE id_paciente = ?", (id_paciente,))
    conn.commit()
    conn.close()
    flash("Paciente eliminado exitosamente.", "success")
    return redirect(url_for("pacientes"))

@app.route('/consultas')
def consultas():
    conn = get_db_connection()
    consultas = conn.execute(
        """
        SELECT c.id_consulta, c.fecha AS fecha, c.motivo AS motivo, m.nombre AS nombre_medico, p.nombre AS nombre_paciente
        FROM consultas c 
        JOIN medicos m ON c.id_medico = m.id_medico
        JOIN pacientes p ON c.id_paciente = p.id_paciente
        """
        ).fetchall()
    conn.close()
    return render_template('consultas.html', consultas=consultas)
@app.route("/consulta/nueva", methods=["GET", "POST"])
def nueva_consulta():
    conn = get_db_connection()
    
    if request.method == "POST":
        fecha = request.form["fecha"]
        motivo = request.form["motivo"]
        id_medico = request.form["id_medico"]
        id_paciente = request.form["id_paciente"]

        conn.execute(
            "INSERT INTO consultas (fecha, motivo, id_medico, id_paciente) VALUES (?, ?, ?, ?)",
            (fecha, motivo, id_medico, id_paciente)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("consultas"))
    
    medicos = conn.execute("SELECT id_medico, nombre FROM medicos").fetchall()
    pacientes = conn.execute("SELECT id_paciente, nombre FROM pacientes").fetchall()
    conn.close()
    
    return render_template("formulario_consultas.html", consulta=None, medicos=medicos, pacientes=pacientes)
@app.route("/consulta/eliminar/<int:id_consulta>")
def eliminar_consulta(id_consulta):
    conn = get_db_connection()
    conn.execute("DELETE FROM consultas WHERE id_consulta = ?", (id_consulta,))
    conn.commit()
    conn.close()
    return redirect(url_for("consultas"))
@app.route("/consulta/editar/<int:id_consulta>", methods=["GET", "POST"])
def editar_consulta(id_consulta):  
    conn = get_db_connection()
    consulta = conn.execute("SELECT * FROM consultas WHERE id_consulta = ?", (id_consulta,)).fetchone()
    
    if request.method == "POST":
        fecha = request.form["fecha"]
        motivo = request.form["motivo"]
        id_medico = request.form["id_medico"]
        id_paciente = request.form["id_paciente"]

        conn.execute(
            "UPDATE consultas SET fecha = ?, motivo = ?, id_medico = ?, id_paciente = ? WHERE id_consulta = ?",
            (fecha, motivo, id_medico, id_paciente, id_consulta)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("consultas"))
    
    medicos = conn.execute("SELECT id_medico, nombre FROM medicos").fetchall()
    pacientes = conn.execute("SELECT id_paciente, nombre FROM pacientes").fetchall()
    conn.close()
    
    return render_template("formulario_consultas.html", consulta=consulta, medicos=medicos, pacientes=pacientes)

if __name__ == '__main__':
    app.run(debug=True)