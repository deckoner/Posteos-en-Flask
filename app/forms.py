from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
    """
    Formulario de inicio de sesión.
    Campos: usuario, contraseña y botón de enviar.
    """
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Entrar")

class RegistrationForm(FlaskForm):
    """
    Formulario de registro de usuario.
    Incluye validación personalizada para verificar si el usuario ya existe.
    """
    username = StringField("Usuario", validators=[DataRequired(), Length(1, 80)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(6, 128)])
    password2 = PasswordField("Repetir contraseña", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrarse")

    def validate_username(self, username):
        """
        Validación personalizada: verifica en la BD si el usuario ya existe.
        Si existe, lanza un ValidationError que WTForms capturará y mostrará.
        """
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Nombre de usuario ya existe. Elige otro.")

class PostForm(FlaskForm):
    """
    Formulario para crear un nuevo post.
    Validaciones de longitud para título y presencia de contenido.
    """
    title = StringField("Título", validators=[DataRequired(), Length(1,140)])
    body = TextAreaField("Contenido", validators=[DataRequired()])
    submit = SubmitField("Publicar")

class UploadForm(FlaskForm):
    """
    Formulario para subir archivos.
    Simplemente un campo de archivo y botón.
    """
    file = FileField("Archivo", validators=[DataRequired()])
    submit = SubmitField("Subir")
