from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    """
    Modelo de Usuario.
    Hereda de UserMixin para facilitar la integración con Flask-Login (is_authenticated, etc.)
    y de db.Model para la integración con SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    about = db.Column(db.String(300))

    # Relación con Post (One-to-Many).
    # 'author' será accesible desde el objeto Post (post.author).
    posts = db.relationship("Post", backref="author", lazy=True)

    def set_password(self, password):
        """
        Genera un hash seguro para la contraseña y lo almacena.
        Nunca guardes contraseñas en texto plano.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

@login_manager.user_loader
def load_user(user_id):
    """
    Función requerida por Flask-Login para cargar un usuario dado su ID.
    Flask-Login maneja la sesión almacenando el ID del usuario,
    y esta función recupera el objeto User completo de la base de datos.
    """
    return User.query.get(int(user_id))

class Post(db.Model):
    """
    Modelo de Post (Publicación).
    Representa una entrada en el blog/feed.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clave foránea que vincula el post a un usuario.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
