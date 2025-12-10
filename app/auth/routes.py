from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import bp
from ..forms import LoginForm, RegistrationForm
from ..models import User
from .. import db

@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Ruta para iniciar sesión de usuario.

    Proceso:
    1. Si el usuario ya está autenticado, redirige al índice.
    2. Instancia LoginForm.
    3. Si es POST y el formulario es válido:
       - Busca el usuario por nombre de usuario.
       - Verifica la contraseña hash.
       - Si es correcto, inicia sesión con `login_user`.
       - Redirige a la página solicitada (next) o al índice.
    4. Si falla la autenticación, muestra un mensaje flash.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("¡Bienvenido, " + user.username + "!")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))
        flash("Usuario o contraseña incorrectos.", "error")
    return render_template("login.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    """
    Ruta para cerrar sesión.

    Requiere autenticación (@login_required).
    Cierra la sesión del usuario actual y redirige al índice.
    """
    logout_user()
    flash("Sesión cerrada.")
    return redirect(url_for("main.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Ruta para registro de nuevos usuarios.

    Proceso:
    1. Si ya está autenticado, redirige al índice.
    2. Instancia RegistrationForm.
    3. Si el formulario es válido (validaciones en forms.py aseguran unicidad):
       - Crea instancia de User.
       - Genera hash de la contraseña.
       - Guarda el usuario en la BD.
       - Redirige al login para que inicie sesión.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado. Ya puedes iniciar sesión.")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)
