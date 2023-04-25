from db import connect
from flask import  render_template, request, redirect, url_for, flash, session, jsonify, make_response, g
from utils import obtener_registro_por_rut_dv, registrar_usuario, modificar_registro


# funcion para mostrar todos los registros de la tabla
def lista_bl():
    print("sesion: ", session)
    if "usuario" in session:
        # Establecer conexión con la base de datos
        conn = connect()
        cur = conn.cursor()
        # Consulta para obtener todos los registros de la tabla black_list
        cur.execute("SELECT * FROM public.black_list")
        all_rows = cur.fetchall()
        # Contar el número total de registros
        total_rows = len(all_rows)
        # Renderizar la plantilla lista_bl.html y pasar los registros recuperados
        return render_template('lista_bl.html', all_rows=all_rows, total_rows=total_rows)
    else:
        return redirect(url_for("login_bl", unauthorized=True))


# Función para registrar un nuevo registro en la base de datos:
def registrar_view():
    if "usuario" in session:
        if request.method == 'POST':
            # Recuperar los datos del formulario
            rut = request.form.get('rut')
            dv = request.form.get('dv')
            afiliado = request.form.get('afiliado') is not None
            prestador = request.form.get('prestador') is not None

            # Registrar el nuevo usuario y redireccionar en caso de éxito
            if registrar_usuario(rut, dv, afiliado, prestador):
                return redirect(url_for('registrar_view'))
            else:
                return redirect(url_for('registrar_view'))

        # Si la solicitud es GET, renderizar la plantilla de registro
        return render_template('registrar_bl.html')
    else:
        return redirect(url_for("login_bl", unauthorized=True))




# funcion para eliminar un registro
def eliminar(rut):
    if "usuario" in session:
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM public.black_list WHERE rut_bl = %s", (rut,))
            conn.commit()
            cur.close()
            # Agrega un mensaje flash para informar al usuario que el registro se eliminó correctamente
            flash('El registro con RUT {} ha sido eliminado correctamente.'.format(rut))
        except Exception as e:
            flash(f'Error al eliminar el registro: {e}', 'danger')

        # Redirige al usuario a la página principal
        return redirect(url_for('buscar_bl'))
    else:
        return redirect(url_for("login_bl", unauthorized=True))


# Función para modificar un registro
def modificar_view(rut, dv):
    if "usuario" in session:
        if request.method == 'GET':
            registro = obtener_registro_por_rut_dv(rut, dv)
            if registro:
                # Si el registro existe, renderizar la plantilla de modificación
                return render_template('modificar_bl.html', registro=registro)
            else:
                # Si el registro no se encuentra, retornar un mensaje de error y un código de estado 404
                return "Registro no encontrado", 404

        elif request.method == 'POST':
            # Recuperar los datos del formulario
            rut_nuevo = request.form['rut']
            dv_nuevo = request.form['dv']
            afiliado_nuevo = True if request.form.get('afiliado') else False
            prestador_nuevo = True if request.form.get('prestador') else False

            # Modificar el registro y redireccionar en caso de éxito
            if modificar_registro(rut, rut_nuevo, dv_nuevo, afiliado_nuevo, prestador_nuevo):
                flash("Registro modificado correctamente", 'success')
                return redirect(url_for('buscar_bl'))

            # Si la modificación falla, renderizar la plantilla de modificación con los datos originales
            registro = obtener_registro_por_rut_dv(rut, dv)
            return render_template('modificar_bl.html', registro=registro)
    else:
        return redirect(url_for("login_bl", unauthorized=True))


# Función para renderizar la página de inicio
def index():
    if "usuario" in session:
        return render_template('index.html')
    else:
        return redirect(url_for("login_bl", unauthorized=True))


# Función para buscar un registro en la base de datos
def buscar_bl():
    if "usuario" in session:
        conn = connect()
        cur = conn.cursor()
        filtered_rows = []
        try:
            if request.method == 'POST':
                busqueda_rut = request.form.get('busqueda')
                busqueda_dv = request.form.get('busqueda_dv')
                if busqueda_rut and busqueda_dv:
                    # Realizar la búsqueda en la base de datos
                    cur.execute("SELECT * FROM black_list WHERE CAST(rut_bl AS TEXT) = %s AND CAST(dv_bl AS TEXT) = %s",
                                (busqueda_rut, busqueda_dv))
                    datos = cur.fetchall()
                    if not datos:
                        flash(
                            'No se encontraron resultados para RUT "' + busqueda_rut + '" y DV "' + busqueda_dv + '".')
                    else:
                        filtered_rows = datos
                else:
                    flash('Por favor, ingrese un RUT y DV válidos para buscar.')
        except Exception as e:
            flash(f'Error al buscar registro: {e}', 'danger')

        return render_template('buscar_bl.html', filtered_rows=filtered_rows)
    else:
        return redirect(url_for("login_bl", unauthorized=True))


# Función para acceder al login
def login_bl():
    conn = connect()
    cur = conn.cursor()
    if request.method == 'POST':
        # Recibir usuario y contraseña desde el formulario
        usuario = request.form['usuario']
        password = request.form['password']
        print("usuario: ", usuario)
        print("contraseña: ", password)
        # Hashear la contraseña
        # hashed_password = generate_password_hash(password)

        # Verificar si el usuario y contraseña (hasheada) existen en la tabla Usuario
        cur.execute("SELECT * FROM Usuario WHERE usuario = %s AND password = %s", (usuario, password))
        data = cur.fetchone()
        print("data: ", data)

        if data is not None:
            # Iniciar sesión
            session['usuario'] = data[1]

            # Redireccionar a la página index.html
            return redirect('/index')

        else:
            # Mostrar un mensaje de error
            return render_template('login_bl.html', error="Usuario o contraseña inválidos")

    return render_template('login_bl.html')


def logout():
    session.pop("usuario", None)
    # flash("¡Tienes que iniciar sesión primero!")
    return redirect(url_for("login_bl"))
