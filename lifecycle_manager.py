import subprocess
import time
import os
import shutil
import sys
import signal

# Configuración
APP_DB_PATH = "app.db"
BACKUP_DB_PATH = "app_estanca.db"
UPLOADS_FOLDER = "uploads"
RESET_INTERVAL_SECONDS = 24 * 60 * 60  # 24 horas

def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def clean_environment():
    """Realiza la limpieza de la base de datos y la carpeta de uploads."""
    log("Iniciando mantenimiento...")
    
    # 1. Borrar app.db
    if os.path.exists(APP_DB_PATH):
        try:
            os.remove(APP_DB_PATH)
            log(f"Eliminado {APP_DB_PATH}")
        except Exception as e:
            log(f"Error eliminando {APP_DB_PATH}: {e}")
    else:
        log(f"{APP_DB_PATH} no existe.")

    # 2. Copiar app_estanca.db a app.db
    if os.path.exists(BACKUP_DB_PATH):
        try:
            shutil.copy(BACKUP_DB_PATH, APP_DB_PATH)
            log(f"Restaurado {APP_DB_PATH} desde {BACKUP_DB_PATH}")
        except Exception as e:
            log(f"Error copiando db: {e}")
    else:
        log(f"ALERTA: {BACKUP_DB_PATH} no existe. No se pudo restaurar la base de datos.")

    # 3. Limpiar carpeta uploads
    if os.path.exists(UPLOADS_FOLDER):
        for filename in os.listdir(UPLOADS_FOLDER):
            file_path = os.path.join(UPLOADS_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    log(f"Borrado archivo: {filename}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    log(f"Borrado directorio: {filename}")
            except Exception as e:
                log(f"Error borrando {file_path}: {e}")
    else:
        log(f"Carpeta {UPLOADS_FOLDER} no existe. Creándola...")
        os.makedirs(UPLOADS_FOLDER)

    log("Mantenimiento completado.")

def run_flask_app():
    """Ejecuta la aplicación Flask como un subproceso."""
    # Asume que 'flask run' funciona en este entorno.
    # Si usas venv, asegúrate de ejecutar este script con el python del venv o ajustar la llamada.
    cmd = [sys.executable, "-m", "flask", "run", "--host=0.0.0.0"]
    return subprocess.Popen(cmd)

def main():
    while True:
        # Asegurarse de empezar limpio o mantener estado anterior?
        # El requerimiento dice: "cada 24 horas coja apague... limpie...".
        # Asumiremos que arrancamos, esperamos 24h, y luego limpiamos.
        
        log("Iniciando aplicación Flask...")
        process = run_flask_app()
        
        try:
            log(f"Aplicación corriendo (PID: {process.pid}). Esperando {RESET_INTERVAL_SECONDS} segundos...")
            # Esperar el intervalo
            time.sleep(RESET_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            log("Interrupción manual recibida. Deteniendo...")
            process.terminate()
            break
        
        # El tiempo ha pasado, detener la app
        log("Tiempo límite alcanzado. Deteniendo aplicación...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            log("La aplicación no se detuvo, forzando kill...")
            process.kill()
            
        # Realizar limpieza
        clean_environment()
        
        # El bucle reiniciará la app
        log("Reiniciando ciclo...")

if __name__ == "__main__":
    # Asegurarse de estar en el directorio correcto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
