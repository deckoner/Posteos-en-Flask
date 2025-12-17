import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.modelo.forms import PostForm, UploadForm
from app.modelo.models import Post

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    """
    Ruta principal (Index).

    Esta función maneja la página de inicio que muestra:
    1. Un formulario para crear nuevos posts (solo para usuarios autenticados).
    2. Una lista de todos los posts ordenados cronológicamente (más recientes primero).

    Proceso:
    - Instancia el formulario PostForm.
    - Si se envía un POST y el formulario es válido (y el usuario está autenticado):
        - Crea un nuevo objeto Post asociado al usuario actual.
        - Lo guarda en la base de datos.
        - Redirige al índice para evitar reenvíos del formulario (patrón Post/Redirect/Get).
    - Si es GET o el formulario no es válido:
        - Obtiene todos los posts de la base de datos.
        - Renderiza la plantilla 'index.html', pasando el formulario y la lista de posts.
    """
    form = PostForm()
    if current_user.is_authenticated and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post publicado correctamente.")
        return redirect(url_for("main.index"))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", form=form, posts=posts)

@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """
    Ruta para subir archivos.

    Requiere que el usuario haya iniciado sesión (@login_required).

    Proceso:
    - Instancia UploadForm.
    - Si el formulario es válido (archivo subido correctamente):
        - Obtiene el archivo del formulario.
        - Asegura un nombre de archivo seguro con `secure_filename` (evita rutas maliciosas).
        - Guarda el archivo en la carpeta configurada (UPLOAD_FOLDER).
        - Muestra un mensaje de éxito.
        - Redirige a la misma página para limpiar el formulario.
    """
    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        # Construye la ruta completa de destino
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        f.save(save_path)
        flash(f"Archivo subido exitosamente: {filename}")
        return redirect(url_for("main.upload"))
    
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template("upload.html", form=form, files=files)

@bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """
    Ruta para servir (descargar/ver) archivos subidos.

    Args:
        filename (str): Nombre del archivo a recuperar.

    Returns:
        Response: El archivo solicitado servido desde el directorio UPLOAD_FOLDER.
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@bp.route("/api/posts", methods=["GET"])
def api_posts():
    """
    API Endpoint que devuelve la lista de posts en formato JSON.

    Ideal para ser consumido por clientes externos o aplicaciones frontend (React, Vue, etc.)
    o simplemente para demostrar cómo construir una API REST básica con Flask.

    Returns:
        Response (JSON): Una lista de objetos representando los posts.
    """
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    # Convertimos los objetos de la base de datos a un diccionario serializable
    data = [{
        "id": p.id,
        "title": p.title,
        "body": p.body,
        "author": p.author.username if p.author else None,
        "timestamp": p.timestamp.isoformat()
    } for p in posts]
    return jsonify(data)

@bp.app_errorhandler(404)
def not_found(e):
    """
    Manejador de errores personalizado para el error 404 (Página no encontrada).

    En lugar de la página de error por defecto, renderiza una plantilla '404.html'
    con un diseño acorde al sitio.

    Args:
        e: La excepción del error.

    Returns:
        tuple: (plantilla renderizada, código de estado 404)
    """
    return render_template("404.html"), 404
