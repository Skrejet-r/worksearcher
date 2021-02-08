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

    def set_uid(self):  # proof language
        with self.connection:
            return self.cursor.execute('SELECT "user_id" FROM "users"').fetchall()

    def set_uid2(self, usid):
        with self.connection:
            return self.cursor.execute('SELECT "user_id" FROM "users" WHERE "id"=?',
                                       (usid,)).fetchone()

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
                                       '("user_id", "ad_status")=(?,1)', (a[0], user_id,))

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
            ader_id = (self.cursor.execute('SELECT ("user_id") FROM "ads" WHERE "id"=?',
                                           (ad_id,)).fetchone())[0]
            n = (self.cursor.execute('SELECT ("n") FROM "ads" WHERE "id"=?',
                                     (ad_id,)).fetchone())[0]
            source = (self.cursor.execute('SELECT ("ader_source") FROM "ads" WHERE "id"=?',
                                           (ad_id,)).fetchone())[0]

            all_infos = (title, ader, city, contact, about, ader_id, n, source)
            return all_infos

    def add_favorite(self, user_id, ader_id, n, ad_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO "favorites" ("user_id", "ader_id", "n_ad", "id_ad") VALUES (?,?,'
                                       '?,?)',
                                       (user_id, ader_id, n, ad_id,))

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

    def get_favs(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "id_ad" FROM "favorites" WHERE "user_id"=?',
                                       (user_id,)).fetchall()

    def add_myadtext(self, text):
        with self.connection:
            return self.cursor.execute('UPDATE "sent" SET "text"=? WHERE "id"=1',
                                       (text,))

    def add_myadkopf(self, text):
        with self.connection:
            return self.cursor.execute('UPDATE "sent" SET "kopf"=? WHERE "id"=1',
                                       (text,))

    def set_myad(self):
        with self.connection:
            kopf = (self.cursor.execute('SELECT "kopf" FROM "sent" WHERE "id"=1').fetchone())[0]
            text = (self.cursor.execute('SELECT "text" FROM "sent" WHERE "id"=1').fetchone())[0]
            pic = (self.cursor.execute('SELECT "n" FROM "sent" WHERE "id"=1').fetchone())[0]
            status = (self.cursor.execute('SELECT "status" FROM "sent" WHERE "id"=1').fetchone())[0]

            ad_infos = (kopf, text, pic, status)
            return ad_infos

    def useradstatus(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT "adstatus" FROM "users" WHERE "user_id"=?',
                                       (user_id,)).fetchone()

    def upd_useradstatus(self, user_id, adid):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "adstatus"=? WHERE "user_id"=?',
                                       (adid, user_id,))

    def sav_ad(self):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "adstatus"=1')

    def sawadusers(self):
        with self.connection:
            return self.cursor.execute('SELECT "user_id" FROM "users" WHERE "adstatus"=0').fetchall()

    def us0rs(self):
        with self.connection:
            return self.cursor.execute('SELECT "user_id" FROM "users" WHERE "status"=0').fetchall()

    def us1rs(self):
        with self.connection:
            return self.cursor.execute('SELECT "user_id" FROM "users" WHERE "status"=1').fetchall()

    def close(self):
        self.connection.close()
