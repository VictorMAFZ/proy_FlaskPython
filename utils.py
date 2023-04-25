import re
from db import connect
from flask import flash


# Función para verificar si un usuario ya existe en la base de datos
def usuario_existe(rut, dv):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM public.black_list WHERE rut_bl=%s AND dv_bl=%s", (rut, dv))
    existe = cur.fetchone()
    return True if existe else False

# Función para validar un RUT y su dígito verificador (DV)
def validar_rut(rut, dv):
    # Eliminar caracteres no válidos y convertir el DV a mayúsculas
    rut = re.sub('[^0-9kK]', '', rut)
    dv = dv.upper()
    if len(rut) < 7 or len(rut) > 8:
        return False
    suma = 0
    for i, v in enumerate(reversed(str(rut))):
        suma += int(v) * (i % 6 + 2)

    dv_calculado = 11 - suma % 11
    dv_calculado = 'K' if dv_calculado == 10 else str(dv_calculado)
    dv_calculado = '0' if dv_calculado == '11' else dv_calculado
    # Comprobar si el DV calculado coincide con el DV proporcionado
    return dv_calculado == dv

# Función para registrar un nuevo usuario en la base de datos

def registrar_usuario(rut, dv, afiliado, prestador):
    # Validar el RUT y el DV
    if not validar_rut(rut, dv):
        flash("RUT y/o DV inválido(s)", 'error')
        return False
    # Verificar si el usuario ya existe en la base de datos
    if usuario_existe(rut, dv):
        flash("El usuario ya existe en la base de datos", 'error')
        return False
    # Insertar el nuevo usuario en la base de datos
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO public.black_list (rut_bl, dv_bl, afiliado_bl, prestador_bl) VALUES (%s, %s, %s, %s)",
                    (rut, dv, afiliado, prestador))
        conn.commit()
        flash("Usuario registrado correctamente", 'success')
        return True
    except Exception as e:
        flash(f"Error al registrar el usuario: {e}", 'error')
        return False


# Función para modificar un registro existente en la base de datos
def modificar_registro(rut_original, rut_nuevo, dv_nuevo, afiliado_nuevo, prestador_nuevo):
    # Validar el RUT y el DV del registro modificado
    if not validar_rut(rut_nuevo, dv_nuevo):
        flash("RUT y/o DV inválido(s)", 'warning')
        return False
     # Actualizar el registro en la base de datos
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE public.black_list SET rut_bl = %s, dv_bl = %s, afiliado_bl = %s, prestador_bl = %s WHERE rut_bl = %s",
        (rut_nuevo, dv_nuevo, afiliado_nuevo, prestador_nuevo, rut_original))
    conn.commit()
    return True


# Función para obtener un registro de la base de datos según el RUT y DV
def obtener_registro_por_rut_dv(rut, dv):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM black_list WHERE rut_bl = %s AND dv_bl = %s", (rut, dv))
        registro = cur.fetchone()

        return registro

    except Exception as e:
        print(f"Error al obtener registro por RUT y DV: {e}")
        return None
    # Cerrar el cursor y la conexión a la base de datos
    finally:
        cur.close()
        conn.close()

