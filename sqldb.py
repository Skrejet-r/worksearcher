import sqlite3


class dbfuncs:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):  # proof if it is here
        with self.connection:
            return self.cursor.execute('SELECT * FROM "users" WHERE "user_id"=?', (user_id,)).fetchall()

    def add_user(self, user_id):  # add new user
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO "users" ("user_id") VALUES(?)', (user_id,))

    def upd_lang(self, user_id, language):  # set language for user
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "language"=? WHERE "user_id"=?',
                                       (language, user_id))

    def set_lang(self, user_id):  # proof language
        with self.connection:
            return self.cursor.execute('SELECT "language" FROM "users" WHERE "user_id"=?',
                                       (user_id,))

    def upd_name(self, user_id, name):  # set name for user
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "name"=? WHERE "user_id"=?',
                                       (name, user_id))

    def set_name(self, user_id):  # return the name
        with self.connection:
            return self.cursor.execute('SELECT "name" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def upd_status(self, user_id, status):  # set status for user
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "status"=? WHERE "user_id"=?',
                                       (status, user_id))

    def set_status(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "status" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def upd_age(self, user_id, age):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "age" =? WHERE "user_id" =?',
                                       (age, user_id))

    def set_age(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "age" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def upd_city(self, user_id, city):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "city" =? WHERE "user_id" =?',
                                       (city, user_id))

    def set_city(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "city" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def close(self):
        self.connection.close()