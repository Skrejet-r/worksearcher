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
                'INSERT INTO "users" ("user_id") VALUES(?)', (user_id,)
            )

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
            return self.cursor.execute('UPDATE "users" SET "age"=? WHERE "user_id"=?',
                                       (age, user_id))

    def set_age(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "age" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def upd_city(self, user_id, city):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "city"=? WHERE "user_id"=?',
                                       (city, user_id))

    def set_city(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "city" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def upd_about(self, user_id, about):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "about"=? WHERE "user_id"=?',
                                       (about, user_id))

    def set_about(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "about" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def delete(self, user_id):
        with self.connection:
            return self.cursor.execute('DELETE FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    # -------------------------------------------------------------------------------------

    def add_ad(self, user_id, adname, city):
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO "ads" ("user_id", "ad_name", "ad_city", "ad_status") VALUES (?, ?, ?, 1 )',
                (user_id, adname, city,))

    def set_ad_title(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_name" FROM "ads" WHERE ("user_id", "ad_status")=(?,?)',
                                       (user_id, 1,)).fetchone()

    def set_ad_title2(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_name" FROM "ads" WHERE ("user_id", "id", "ad_status")=(?,?,?)',
                                       (user_id, ad_id, 0,)).fetchone()

    def upd_ad_title(self, user_id, ad_name):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_name"=? WHERE ("user_id", "ad_status")=(?, 1)',
                                       (ad_name, user_id))

    def upd_ad_minage(self, user_id, ad_age_from):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_minage"=? WHERE ("user_id", "ad_status")=(?, 1)',
                                       (ad_age_from, user_id))

    def set_ad_minage(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_minage" FROM "ads" WHERE ("user_id", "ad_status")=(?,?)',
                                       (user_id, 1,)).fetchone()

    def set_ad_minage2(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_minage" FROM "ads" WHERE ("user_id", "id", "ad_status")=(?,?,?)',
                                       (user_id, ad_id, 0,)).fetchone()

    def upd_ad_maxage(self, user_id, ad_age_to):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_maxage"=? WHERE ("user_id", "ad_status")=(?,1)',
                                       (ad_age_to, user_id))

    def set_ad_maxage(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_maxage" FROM "ads" WHERE ("user_id", "ad_status")=(?,?)',
                                       (user_id, 1,)).fetchone()

    def set_ad_maxage2(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_maxage" FROM "ads" WHERE ("user_id", "id", "ad_status")=(?,?,?)',
                                       (user_id, ad_id, 0,)).fetchone()

    def upd_ad_about(self, user_id, ad_about):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_about"=? WHERE ("user_id", "ad_status")=(?,1)',
                                       (ad_about, user_id))

    def set_ad_about(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_about" FROM "ads" WHERE ("user_id", "ad_status")=(?,?)',
                                       (user_id, 1,)).fetchone()

    def set_ad_about2(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_about" FROM "ads" WHERE ("user_id", "id", "ad_status")=(?,?,?)',
                                       (user_id, ad_id, 0,)).fetchone()

    def upd_ad_contact(self, user_id, ad_contact):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "contact"=? WHERE ("user_id", "ad_status")=(?,1)',
                                       (ad_contact, user_id))

    def set_ad_contact(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "contact" FROM "ads" WHERE ("user_id", "ad_status")=(?,?)',
                                       (user_id, 1,)).fetchone()

    def set_ad_contact2(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('SELECT "contact" FROM "ads" WHERE ("user_id", "id", "ad_status")=(?,?,?)',
                                       (user_id, ad_id, 0,)).fetchone()

    def upd_ad_city(self, user_id, city):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_city"=? WHERE ("user_id", "ad_status")=(?, 1)',
                                       (city, user_id))

    def set_ad_city2(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('SELECT "ad_city" FROM "ads" WHERE ("user_id", "id", "ad_status")=(?,?,?)',
                                       (user_id, ad_id, 0,)).fetchone()

    def ad_delete(self, user_id):
        with self.connection:
            return self.cursor.execute('DELETE FROM "ads" WHERE ("user_id", "ad_status")=(?, 1)',
                                       (user_id,)).fetchone()

    def ad_saving(self, user_id):
        with self.connection:
            a = self.cursor.execute('SELECT "source" FROM "users" WHERE "user_id"=?',
                                    (user_id,)).fetchone()
            return self.cursor.execute('UPDATE "ads" SET ("ad_status", "ader_source")=(0,?) WHERE '
                                       '("user_id", "ad_status")=(?,1)', (a, user_id,))

    def xbutton1(self, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_minage"=0 WHERE ("user_id", "ad_status")=(?, 1)',
                                       (user_id,))

    def xbutton2(self, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_maxage"=999999 WHERE ("user_id", "ad_status")=(?,1)',
                                       (user_id,))

    def nn(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "id" FROM "ads" WHERE "user_id"=?',
                                       (user_id,)).fetchall()

    def ad_admin(self, user_id, name):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ader_name"=? WHERE ("user_id", "ad_status")=(?,1)',
                                       (name, user_id,))

    def all_ads(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "n_ads" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def plus_ad(self, user_id):
        with self.connection:
            a = self.cursor.execute('SELECT "n_ads" FROM "users" WHERE "user_id"=?',
                                    (user_id,)).fetchone()
            b = a[0] + 1

            return self.cursor.execute('UPDATE "users" SET "n_ads" = ? WHERE "user_id"=?',
                                       (int(b), user_id,))

    def minus_ad(self, user_id):
        with self.connection:
            a = self.cursor.execute('SELECT "n_ads" FROM "users" WHERE "user_id"=?',
                                    (user_id,)).fetchone()
            b = a[0] - 1
            return self.cursor.execute('UPDATE "users" SET "n_ads"=? WHERE "user_id"=?',
                                       (int(b), user_id,))

    def num_ad(self, user_id):
        with self.connection:
            a = self.cursor.execute('SELECT "n_ads" FROM "users" WHERE "user_id"=?',
                                    (user_id,)).fetchone()
            return self.cursor.execute('UPDATE "ads" SET "n"=? WHERE ("user_id", "ad_status")=(?,1)',
                                       (int(a[0]), user_id,))

    def del_ad(self, ad_id):
        with self.connection:
            return self.cursor.execute('DELETE FROM "ads" WHERE "id"=?',
                                       (ad_id,)).fetchone()

    def avaiable(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ad_status"=1 WHERE ("user_id", "id")=(?,?)',
                                       (user_id, ad_id,))

    def change_ader_all_ads(self, user_id, name):
        with self.connection:
            return self.cursor.execute('UPDATE "ads" SET "ader_name"=? WHERE "user_id"=?',
                                       (name, user_id,))

    def getting_all_suitable_ads(self, city, age):
        with self.connection:
            return self.cursor.execute('SELECT "id" FROM "ads" WHERE ("ad_city")=(?) AND'
                                       '                              ("ad_minage")<=(?) AND'
                                       '                              ("ad_maxage")>=(?)',
                                       (city, age, age)).fetchall()

    def ad(self, ad_id):
        with self.connection:
            title = (self.cursor.execute('SELECT ("ad_name") FROM "ads" WHERE "id"=?',
                                         (ad_id,)).fetchone())[0]
            ader = (self.cursor.execute('SELECT ("ader_name") FROM "ads" WHERE "id"=?',
                                        (ad_id,)).fetchone())[0]
            city = (self.cursor.execute('SELECT ("ad_city") FROM "ads" WHERE "id"=?',
                                        (ad_id,)).fetchone())[0]
            contact = (self.cursor.execute('SELECT ("contact") FROM "ads" WHERE "id"=?',
                                           (ad_id,)).fetchone())[0]
            about = (self.cursor.execute('SELECT ("ad_about") FROM "ads" WHERE "id"=?',
                                         (ad_id,)).fetchone())[0]

            all_infos = (title, ader, city, contact, about)
            return all_infos

    def add_favorite(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO "favorites" ("user_id","ad_id", "send") VALUES (?,?,?)',
                                       (user_id, ad_id, 0,))

    def sending(self, user_id, ad_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO "favorites" ("user_id","ad_id", "send") VALUES (?,?,?)',
                                       (user_id, ad_id, 1,))

    def upd_source(self, user_id, source):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "source"=? WHERE "user_id"=?',
                                       (source, user_id,))

    def set_source(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "source" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()[0]

    def close(self):
        self.connection.close()
