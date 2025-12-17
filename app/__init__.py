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
    app = Flask(__name__, static_folder="static", template_folder="vista")
    app.config.from_object(config_class)

    # REINICIO DE BASE DE DATOS (Cada vez que arranca la app)
    import shutil
    
    # 1. Determinar rutas
    # La ruta de destino depende de la configuración (puede ser local o /tmp en Vercel)
    # Extraemos la ruta del archivo de la URI de SQLALCHEMY
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if db_uri.startswith("sqlite:///"):
        db_path = db_uri.replace("sqlite:///", "")
        
        # Ruta de la 'imagen estanca' (siempre en la raíz del proyecto)
        # Asumimos que app_estanca.db está en el mismo nivel que config.py/run.py, 
        # es decir, el basedir configurado en Config, o el root_path de la app.
        backup_path = os.path.join(app.root_path, "..", "app_estanca.db") 
        # app.root_path apunta a /app, así que subimos un nivel.
        
        # 2. Copiar si existe el backup
        if os.path.exists(backup_path):
            try:
                # Asegurar que el directorio destino existe (por si es /tmp)
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                shutil.copy(backup_path, db_path)
                print(f" [INFO] Base de datos restaurada desde {backup_path} a {db_path}")
            except Exception as e:
                 print(f" [ERROR] No se pudo restaurar la base de datos: {e}")
        else:
             print(f" [WARN] No se encontró {backup_path}, se usará DB existente o nueva.")

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
    from .controlador.auth import bp as auth_bp
    from .controlador.main import bp as main_bp
    
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
