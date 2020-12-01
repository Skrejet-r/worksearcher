from sqldb import dbfuncs

db = dbfuncs("db_ws.db")


def lang(user_id):
    a = user_id
    b = db.set_lang(a)  # proof language
    b1 = ''.join(map(str, b))
    return int(b1[1])


class extraFuncs:
    pass
