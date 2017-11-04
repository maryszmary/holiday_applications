"""
This is а Flask server for my test task in profi.ru.
The interface allows to send the applications for holidays for users
and to see the holidat stats for administers.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask.ext.login import LoginManager
from flask.ext.login import UserMixin
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import logout_user
from db import HolidayDB


DBNAME = 'holiday.db'
app = Flask(__name__, static_folder='./static')
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    """docstring for User"""
    def __init__(self, username):
        self.id = username
        self.get_user_data()

    def get_user_data(self):
        name, department, status = DB.get_user_data(self.id)
        self.name = name
        self.department = department
        self.status = status
    
    def __repr__():
        return self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    return render_template("log_in.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if DB.passwordCorrect(username, password):
            user = User(username)
            login_user(user)
        return redirect(url_for('home'))
    return redirect(url_for('index'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name'] + ' ' + request.form['name']


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form['submit'] == 'Apply for holiday!':
            pass
    return render_template('home.html', name=current_user.name)


if __name__ == '__main__':
    DB = HolidayDB(DBNAME)
    app.secret_key = '0jhsijnj=c1el[80ez5.h=82'
    app.run(debug = True, port = 5555)
