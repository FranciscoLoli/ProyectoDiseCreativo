import functools
from flask import (Blueprint, flash, g, render_template, request, url_for, session, redirect)
from werkzeug.security import check_password_hash, generate_password_hash
from patrones.db import get_db

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        birthdate = request.form['birthdate']
        role = request.form['role']
        family = "a wuevo"

        db,c = get_db()
        error = None

        c.execute('select id from Usuario where username = %s',(username,))
        if not username:
            error = 'Nombre de usuario es requerido'
        if not password:
            error = 'Contraseña de usuario es requerida'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)

        if error is None:
            c.execute('insert into Usuario (username, password, email, address, phone, birthdate, role, family) values' 
                    '(%s,%s,%s,%s,%s,%s,%s,%s)',(username, generate_password_hash(password),email,address,phone,birthdate,role,family))
            db.commit()
            '''
            c.execute("select id from usuario where username='{}'".format(username)) 
            identification = db.commit()

            c.execute('insert into familia (familiar, family) values' 
                    '(%s,%s)',(identification,family))
            db.commit()
            '''
            send(username,email)

            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db,c = get_db()
        error = None

        c.execute('select * from Usuario where username = %s',(username,))
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña invalida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalida'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('patrones.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db,c = get_db()
        c.execute('select * from Usuario where id = %s', (user_id,))
        g.user = c.fetchone()

def login_require(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def send(usuario, correo) :
    msg = MIMEMultipart()
    message = "Bienvenido {}! \nGracias por preocuparte por los adultos mayores tanto como nosotros.\
        \nEn nuestra aplicación podras gestionar recordatorios, medicamentos y las citas médicas en veras de una vida\
        cómoda, feliz y tranquila para su familiar. Asi mismo, encontrara ejercicios de estimulación fisica y mental asegunrando\
        una buena calidad de vida.".format(usuario)
    
    password = "patrones12345"
    msg['From'] = "patronesdiseno1@gmail.com"
    msg['To'] = correo
    msg['Subject'] = "¡Bienvenido!"

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
