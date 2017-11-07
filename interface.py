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
from flask import jsonify
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
        name, department, status, days_free = DB.get_user_data(self.id)
        self.name = name
        self.department = department
        self.status = status
        self.days_free = days_free

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
        else:
            error = "Either login or password is wrong, try again!"
            return render_template("log_in.html", login_error=error)
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
        if request.form['password'] != request.form['sec_password']:
            error = "The passwords you've entered don't match, try again!"
            return render_template('log_in.html', error_message=error)
        username = request.form['username']
        if DB.userExists(username):
            error = "A user with this name already exists. Please choose another name."
            return render_template('log_in.html', error_message=error)
        password = request.form['password']
        name = request.form['name'] + ' ' + request.form['surname']
        department = request.form['department']
        if username and password and name and department:
            DB.add_user(username, password, name, department)
            user = User(username)
            login_user(user)
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    applications = DB.active_apps(current_user.id)
    if request.method == 'POST':
        if request.form['submit'] == 'Apply for holday!':
            return render_template('home.html',
                current_user=current_user, create=True)
        if request.form['submit'] == 'Send':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            success = DB.add_application(current_user.id, start_date, end_date)
            if success:
                return redirect(url_for('home'))
            else:
                error = 'It seems that you don\'t have enough free days!'
                return render_template('home.html', current_user = current_user,
                    create=True, error=error)
    return render_template('home.html', current_user=current_user,
        applications=applications)


@app.route('/revert', methods=['GET', 'POST'])
@login_required
def revert_app():
    if request.method == 'POST':
        app_id = request.form['app_id']
        success = DB.remove_application(app_id)
    return jsonify({'success': success})


@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    if request.method == 'POST':
        employee = request.form['employee']
        user = DB.userExists(employee)
        if user:
            data = DB.get_stats(user)
            return render_template('stats.html',
                employee = employee, found=True, data = data)
        else:
            return render_template('stats.html',
                employee = employee, found = False)
    return render_template('stats.html')


if __name__ == '__main__':
    DB = HolidayDB(DBNAME)
    app.secret_key = '0jhsijnj=c1el[80ez5.h=82'
    app.run(debug = True, port = 5555)
