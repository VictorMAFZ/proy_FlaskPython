# Importar las funciones necesarias de Flask y las funciones personalizadas desde otros archivos
from models import lista_bl, buscar_bl, eliminar, registrar_view, modificar_view, index, login_bl, logout


# Función para registrar las rutas de la aplicación
def register_routes(app):
    # Rutas de la aplicación
    app.add_url_rule('/', view_func=login_bl, methods=['GET', 'POST'])
    app.add_url_rule('/index', view_func=index)
    app.add_url_rule('/lista_bl', view_func=lista_bl, methods=['GET', 'POST'])
    app.add_url_rule('/buscar_bl', view_func=buscar_bl, methods=['GET', 'POST'])
    app.add_url_rule('/eliminar/<rut>', view_func=eliminar, methods=['POST'])
    app.add_url_rule('/registrar_bl', view_func=registrar_view, methods=['GET', 'POST'], endpoint='registrar_view')
    app.add_url_rule('/modificar_bl/<rut>/<dv>', view_func=modificar_view, methods=['GET', 'POST'], endpoint='modificar_view')
    app.add_url_rule("/logout", view_func=logout)
