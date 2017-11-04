"""
This is the database module. It contains DB class.
"""

import os
import sqlite3


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
        'CREATE TABLE users (ID integer, username, password, status, name, department, days_free);',
        'CREATE TABLE applications (ID integer, person_id, date, holiday_start, holiday_duration);',
        ]
        for line in creation:
            cur.execute(line)
        db.commit()

    def add_user(self, username, password):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT ID FROM users')
        # TODO: регистрация
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
        db.close()
        return user_data


    def get_stats(self, username):
        db = sqlite3.connect(self.name)
        cur = db.cursor()
        cur.execute('SELECT * FROM stats WHERE user = ?', (username, ))
        results = cur.fetchall()
        db.commit()
        db.close()
        return results
