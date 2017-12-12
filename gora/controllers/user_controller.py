from flask import render_template, redirect, url_for
from flask import request, session
from flask_login import login_user, logout_user, login_required

from gora import app, login_manager
from gora.security.iam import get_user_by_username
from gora.models.graph import User

import uuid


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('get_account_login'))
    

# --------------------------------------------------------------------------
# GET /SIGNUP
# --------------------------------------------------------------------------
# Root resource
@app.route('/signup', methods=['GET'])
def get_account_signup():
    return render_template("authentication/signup.html")
    
    
# --------------------------------------------------------------------------
# GET /SIGNUP
# --------------------------------------------------------------------------
# Root resource
@app.route('/signup', methods=['POST'])
def post_account_signup():
    
    try:
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        instruments = request.form['instruments']
        username = request.form['username']
        password = request.form['password']
        
        user = User(
            user_id=str(uuid.uuid4()),
            name=name,
            last_name=lastname,
            username=username,
            email=email,
            instruments=instruments,
            is_active = True
        )

        # We set the password by calling the update function that handles
        # proper hashing of the password so we never store the actual
        # password

        user.update_password(password)
        user.save()
        return redirect(url_for('get_dashboard_root'))
    except Exception as ex:
        print(ex)
        return render_template("authentication/signup.html", error="You must fill all required fields")
    


# --------------------------------------------------------------------------
# GET /LOGIN
# --------------------------------------------------------------------------
# Root resource
@app.route('/login', methods=['GET'])
def get_account_login():
    return render_template("authentication/login.html")


# --------------------------------------------------------------------------
# POST /LOGIN
# --------------------------------------------------------------------------
# Root resource
@app.route('/login', methods=['POST'])
def post_account_login():
    """
        First we need to verify the request contains a username and a password
        if not, then we must display an error.
        :return:
    """
    app.logger.info('Reading credentials from request...')
    username = request.form['username']
    password = request.form['password']

    if username is None:
        return render_template("authentication/login.html", error="Debe proporcionar un usuario")
    if password is None:
        return render_template("authentication/login.html", error="Debe proporcionar una contrasena")

    app.logger.info('Credentials OK, now authenticating...')

    user = get_user_by_username(username)
    if user is None:
        return render_template("authentication/login.html", error="No se ha encontrado el usuario proporcionado")

    if user.authenticate(password):
        app.logger.info('Credentials are correct...')
        session['logged_in'] = True
        login_user(user)
        return redirect(url_for('get_dashboard_root'))
    else:
        app.logger.info('Credentials are not correct...')
        error = "Su contraseña no es correcta"
        return render_template("authentication/login.html", error=error)


# --------------------------------------------------------------------------
# POST /LOGOUT
# --------------------------------------------------------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_account_login'))
