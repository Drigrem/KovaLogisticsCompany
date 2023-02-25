from flask import Flask, render_template, request, url_for, g, flash, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from FDataBase import FDataBase
import sqlite3
import os

DATABASE = '/tmp/appsite.db'
DEBUG = True
SECRET_KEY = 'aeoiAdawhdo3h22h3io@H#$UOIH@'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'appsite.db')))


login_manager = LoginManager(app)



@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        user = dbase.getUserByPhone(request.form['login'])
        password = dbase.getPassword(request.form['password'])
        if user and password:
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('profile'))
        else:
            flash("Неверный логин или пароль")
    return render_template('index.html')


@app.route("/register_driver", methods=["POST", "GET"])
def register_driver():
    if request.method == "POST":
        if len(request.form['phone_number']) == 11:
            if request.form['password'] == request.form['password2']:
                res = dbase.addUser(request.form['surname'], request.form['name'], request.form['second_surname'],
                                    request.form['phone_number'], request.form['weight'], request.form['distance'],
                                    request.form['password'])
                flash("Вы успешно зарегистрировались")
                return redirect(url_for('index'))
            else:
                flash('Пароли не совпадают')
        else:
            flash('Проверьте правильность введённого номера телефона')
    return render_template("register-driver.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы")
    return redirect(url_for('index'))


@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True)
