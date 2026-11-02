from flask import Flask
from .extensions import db, login_manager, migrate
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from . import models

    from .main.routes import bp as main_bp
    from .auth.routes import bp as auth_bp
    from .usuarios.routes import bp as usuarios_bp
    from .categorias.routes import bp as categorias_bp
    from .anuncios.routes import bp as anuncios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp, url_prefix="/anuncios")

    return app