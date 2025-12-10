import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config

# Inicialización de extensiones (sin vincular a app aún)
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    """
    Patrón Factory para crear la aplicación Flask.
    
    Esto permite crear múltiples instancias de la app (útil para pruebas)
    y mantener el código organizado.
    
    Args:
        config_class: Clase de configuración a utilizar (por defecto Config).
        
    Returns:
        app: La instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    # Crear carpeta de uploads si no existe
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Inicializar las extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configurar vista de login para redireccionar si no está autenticado
    login_manager.login_view = "auth.login"
    
    csrf.init_app(app)

    # Registrar Blueprints (módulos de la aplicación)
    # Esto separa las rutas en componentes lógicos.
    from .auth import bp as auth_bp
    from .main import bp as main_bp
    
    app.register_blueprint(auth_bp, url_prefix="/auth") # Rutas auth tendrán prefijo /auth
    app.register_blueprint(main_bp)                     # Rutas main estarán en la raíz /

    # Crear la base de datos si no existe.
    # Nota: En producción, se recomienda usar migraciones (Flask-Migrate) en lugar de create_all.
    with app.app_context():
        db.create_all()

    @app.errorhandler(413) # RequestEntityTooLarge
    def request_entity_too_large(e):
        from flask import flash, redirect, url_for
        flash("El archivo es demasiado grande. El límite es de 5 MB.", "error")
        return redirect(url_for("main.upload"))

    return app
