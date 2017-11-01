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
from flask.ext.login import login_user
from flask.ext.login import login_required
from db import HolidayDB


DBNAME = 'holiday.db'
app = Flask(__name__, static_folder='./static')
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    """docstring for User"""
    def __init__(self, username, name, department, status):
        self.nick = username
        self.name = name
        self.department = department
        self.status = status
    
    def __repr__():
        return self.nick


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("log_in.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = DB.get_user_data(username, password)
        if user_data:
            name, department, status = user_data
            user = User(username, name, department, status)
            print(user.department)
        return redirect(url_for('home'))
    return redirect(url_for('index'))


@app.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    return render_template('home.html')


if __name__ == '__main__':
    DB = HolidayDB(DBNAME)
    app.run(debug = True, port = 5555)
