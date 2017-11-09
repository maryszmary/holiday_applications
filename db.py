"""
This is the database module. It contains DB class.
"""

import os
import sqlite3
import time
from datetime import datetime


class VacationDB():
    '''the db fith tests and users'''

    def __init__(self, name):
        self.name = name
        if not os.path.exists(self.name):
            self.create() # create the database if there's none yet

    def create(self):
        """
        Creates the database.
        """
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        creation = [
        'CREATE TABLE users (ID integer, username, password, status, '
        'name, department, days_free integer);',
        'CREATE TABLE applications (ID integer, username, date, '
        'start_date date, end_date date, status);',
        ]
        for line in creation:
            cur.execute(line)
        db.commit()

    def add_user(self, username, password, name, department):
        """
        Registers a new user.
        """
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT MAX(ID) FROM users')
        maxid = cur.fetchone()[0]
        usid = maxid + 1 if maxid is not None else 0
        date = time.strftime('%Y.%m.%d')
        cur.execute(
            'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)',
            (usid, username, password, "user", name, department, 28)
            )
        db.commit()
        db.close()

    def add_application(self, username, start_date, end_date):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        if self.enough_days(cur, username, start_date, end_date):
            sucsess = True
            date = time.strftime('%Y-%m-%d')
            cur.execute('SELECT MAX(ID) FROM applications')
            maxid = cur.fetchone()[0]
            new_id = maxid + 1 if maxid is not None else 0
            cur.execute(
                'INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?)',
                (new_id, username, date, start_date, end_date, 'pending')
                )
        else:
            sucsess = False
        db.commit()
        db.close()
        return sucsess

    def enough_days(self, cur, username, start_date, end_date):
        """
        Chacks if there're enough free days for the holliday applied for.
        """
        cur.execute('SELECT days_free FROM users WHERE username = ?', (username,))
        days_free = cur.fetchone()[0]
        days_between = abs(self.days_difference(start_date, end_date))
        return days_free >= days_between

    def days_difference(self, start_date, end_date):
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')
        return (d2 - d1).days

    def remove_application(self, app_id):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT start_date FROM applications WHERE ID = ?', (app_id,))
        start_date = cur.fetchone()[0]
        y, m, d = self.parse_date(start_date)
        tm = time.localtime()
        if y == tm.tm_year and m == tm.tm_mon and d > tm.tm_mday + 3:
            cur.execute('DELETE FROM applications WHERE ID = ?', (app_id,))
            sucsess = True
        else:
            sucsess = False
        db.commit()
        db.close()
        return sucsess

    def passwordCorrect(self, username, password):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute(
            'SELECT password FROM users WHERE username = ?', (username, ))
        stored_password = cur.fetchone()[0]
        db.close()
        return stored_password == password

    def get_user_data(self, username):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute(
            'SELECT name, department, status, days_free FROM users WHERE username = ?',
            (username, )
            )
        user_data = cur.fetchall()[0]
        db.commit()
        db.close()
        return user_data

    def get_month_data(self):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT start_date, end_date FROM applications')
        apps = cur.fetchall()

        # counting the number of vacation days in each month
        app_dicts = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0,
        '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0}
        for line in apps:
            if self.days_difference(line[0], time.strftime('%Y-%m-%d')) > 0:
                sm = str(line[0].split('-')[1])
                em = str(line[1].split('-')[1])
                next_days = 0
                if sm == em:
                    cur_days = self.days_difference(line[0], line[1])
                else:
                    fday = line[1].rsplit('-', 1)[0] + '-01'
                    cur_days = self.days_difference(line[0], fday)
                    next_days = self.days_difference(fday, line[1])
                app_dicts[sm] += cur_days
                app_dicts[em] += next_days

        # transforms the dictionary into a list of tuples
        apps = self.transform_monthly_data(app_dicts)
        db.commit()
        db.close()
        return apps

    def days_by_year(self, username):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT start_date, end_date FROM applications '
            'WHERE username = ?', (username, )
            )
        apps = cur.fetchall()
        app_dicts = {}
        for line in apps:
            if self.days_difference(line[0], time.strftime('%Y-%m-%d')) > 0:
                print(line[0], line[1])
                sy = str(line[0].split('-')[0])
                ey = str(line[1].split('-')[0])
                next_days = 0
                if sy == ey:
                    cur_days = self.days_difference(line[0], line[1])
                else:
                    fday = line[1].rsplit('-', 1)[0] + '-01'
                    cur_days = self.days_difference(line[0], fday)
                    next_days = self.days_difference(fday, line[1])
                app_dicts[sy] = cur_days + app_dicts.get(sy, 0)
                app_dicts[ey] = next_days + app_dicts.get(ey, 0)
        db.commit()
        db.close()
        return app_dicts

    def transform_monthly_data(self, app_dicts):
        apps = sorted(app_dicts.items(), key=lambda x: x[0])
        max_days = max(apps, key=lambda x: x[1])
        min_days = min(apps, key=lambda x: x[0])
        for i, line in enumerate(apps):
            if line[1] == max_days[1]:
                css_class = 'end'
            elif line[1] == min_days[1]:
                css_class = 'pending'
            else:
                css_class = 'id'
            apps[i] = (line[0], line[1], css_class)
        return apps

    def userExists(self, name):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT username FROM users WHERE username = ?', (name, ))
        if cur.fetchone():
            db.commit()
            db.close()
            return name
        cur.execute('SELECT username FROM users WHERE name = ?', (name, ))
        username = cur.fetchone()
        if username:
            username = username[0]
        db.commit()
        db.close()
        return username

    def active_apps(self, username):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        tm = time.localtime()
        cur.execute(
            'SELECT ID, start_date, end_date, status FROM applications WHERE username = ?',
            (username, )
            )
        apps = cur.fetchall()
        app_dicts = []
        for i, line in enumerate(apps):
            y, m, d = self.parse_date(line[1])
            if y >= tm.tm_year and m >= tm.tm_mon and d >= tm.tm_mday:
                app_dicts.append({
                'ID': line[0],
                'start_date': line[1],
                'end_date': line[2],
                'status': line[3]
                })
        db.close()
        return app_dicts

    def get_personal_data(self, username):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT name, username, department FROM users WHERE username = ?', (username, ))
        user_data = cur.fetchall()[0]
        db.commit()
        db.close()
        return user_data

    def parse_date(self, date):
        start_date = [int(el) for el in date.split('-')]
        return tuple(start_date)
