import os

# Obtiene la ruta absoluta del directorio base del archivo actual
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Clase de configuración de Flask.
    Define variables de entorno y opciones para la aplicación y sus extensiones.
    """
    
    # Clave secreta para firmar cookies y tokens CSRF (IMPORTANTE: cambiar en producción)
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-me"
    
    # Configuración para Vercel (Sistema de archivos efímero /tmp)
    if os.environ.get('VERCEL'):
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/app.db"
        UPLOAD_FOLDER = "/tmp/uploads"
    else:
        # URI de conexión a la base de datos.
        # Por defecto usa SQLite en un archivo local 'app.db'
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
            "sqlite:///" + os.path.join(basedir, "app.db")
        
        # Carpeta donde se guardarán los archivos subidos
        UPLOAD_FOLDER = os.path.join(basedir, "uploads")
    
    # Tamaño máximo de archivo permitido (5 MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
