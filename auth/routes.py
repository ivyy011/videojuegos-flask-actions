
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models import User
from . import auth_bp
from .forms import LoginForm


# Ruta para iniciar sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # Si el usuario ya inició sesión, enviarlo a videojuegos
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    # Crear el formulario de inicio de sesión
    form = LoginForm()

    # Validar los datos del formulario
    if form.validate_on_submit():

        username = form.username.data.strip()
        password = form.password.data

        # Buscar el usuario en la base de datos
        user = User.query.filter_by(username=username).first()

        # Verificar que el usuario y la contraseña sean correctos
        if user and user.verify_password(password):

            # Iniciar sesión
            login_user(user, remember=form.remember_me.data)

            flash('Inicio de sesión exitoso.', 'success')

            # Redirigir a la lista de videojuegos
            return redirect(url_for('juegos'))

        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    # Mostrar el formulario de inicio de sesión
    return render_template('login.html', form=form)


# Ruta para cerrar sesión
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():

    # Cerrar la sesión del usuario
    logout_user()

    flash('Has cerrado sesión correctamente.', 'success')

    # Regresar al formulario de inicio de sesión
    return redirect(url_for('auth.login'))
