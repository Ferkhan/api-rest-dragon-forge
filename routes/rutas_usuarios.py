def rutas_usuarios(app):
    @app.get('/usuario')
    def usuario():
        return "Usuario endpoint"