import math
import sqlite3
import time
import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, surname, name, second_surname, phone_number, weight, distance, password):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE phone_number LIKE '{phone_number}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return False

            tm = int(math.floor(time.time()))
            dt = datetime.datetime.fromtimestamp(tm)
            time_formatted = dt.strftime("%H:%M")
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (
                surname, name, second_surname, phone_number, weight, distance, password, time_formatted))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def getUsers(self):
        try:
            self.__cur.execute(
                f"SELECT id, surname, name, second_surname, phone_number, weight, distance, password, time FROM users ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения данных об водителях из БД")

        return []

    def getUserByPhone(self, phone_number):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE phone_number = '{phone_number}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения логина из БД")
        return []

    def getPassword(self, password):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE password = '{password}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения логина из БД")
        return []

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
