"""
This is the database module. It contains DB class.
"""

import os
import sqlite3
import time


class HolidayDB():
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
        'CREATE TABLE users (ID integer, date, username, password, status, '
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
        date = time.strftime('%Y.%m.%d.%H.%m')
        cur.execute(
            'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)',
            (usid, username, password, date, "user", name, department, 28)
            )
        db.commit()
        db.close()

    def add_application(self, username, start_date, end_date):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        date = time.strftime('%Y-%m-%d.%H:%m')
        cur.execute('SELECT MAX(ID) FROM applications')
        maxid = cur.fetchone()[0]
        new_id = maxid + 1 if maxid is not None else 0
        cur.execute(
            'INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?)',
            (new_id, username, date, start_date, end_date, 'pending')
            )
        db.commit()
        db.close()

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
            'SELECT name, department, status FROM users WHERE username = ?',
            (username, )
            )
        user_data = cur.fetchall()[0]
        db.commit()
        db.close()
        return user_data

    def userExists(self, name):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT username FROM users WHERE username = ?', (name, ))
        if cur.fetchone()[0]:
            db.commit()
            db.close()
            return name
        cur.execute('SELECT username FROM users WHERE name = ?', (name, ))
        username = cur.fetchone()[0]
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
        for i, line in enumerate(apps):
            y, m, d = self.parse_date(line[1])
            if y >= tm.tm_year and m >= tm.tm_mon and d >= tm.tm_mday:
                apps[i] = {
                'ID': line[0],
                'start_date': line[1],
                'end_date': line[2],
                'status': line[3]
                }
        db.close()
        return apps

    def get_stats(self, username):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT name, department FROM users WHERE username = ?', (username, ))
        user_data = cur.fetchall()
        user_data = "name"
        cur.execute('SELECT * FROM applications WHERE username = ?', (username, ))
        app_data = cur.fetchall()
        db.commit()
        db.close()
        return data

    def parse_date(self, date):
        start_date = [int(el) for el in date.split('-')]
        return tuple(start_date)
