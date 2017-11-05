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
        'CREATE TABLE users (ID integer, date, username, password, status, name, department, days_free integer);',
        'CREATE TABLE applications (ID integer, user_id, date, holiday_start, holiday_duration);',
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
        cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)',
            (usid, username, password, date, "user", name, department, 28))
        db.commit()
        db.close()

    def add_application(self, username, holiday_start, holiday_duration):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        date = time.strftime('%Y.%m.%d.%H.%m')
        db.commit()
        db.close()


    def passwordCorrect(self, username, password):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT password FROM users WHERE username = ?',
                    (username, ))
        stored_password = cur.fetchall()[0][0]
        db.close()
        return stored_password == password

    def get_user_data(self, username):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT name, department, status FROM users '
            'WHERE username = ?', (username, ))
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
