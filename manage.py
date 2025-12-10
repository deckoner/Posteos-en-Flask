from app import create_app, db
from app.models import User, Post

# Crea la aplicación utilizando el factory
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Agrega objetos al contexto del shell de Flask.
    
    Esto permite acceder a 'db', 'User' y 'Post' directamente
    al ejecutar `flask shell`, facilitando la depuración y pruebas manuales.
    
    Returns:
        dict: Diccionario con los objetos a exponer.
    """
    return {"db": db, "User": User, "Post": Post}

if __name__ == "__main__":
    """
    Punto de entrada principal si se ejecuta el script directamente.
    Inicia el servidor en modo debug.
    
    Uso: python manage.py
    """
    app.run(debug=True)
