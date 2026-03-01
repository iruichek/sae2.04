from flask import g
import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="localhost",
            user="root",
            password="secret",
            database="BDD_iruichek",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        activate_db_options(db)
    return db


def activate_db_options(db):
    cursor = db.cursor()


    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            cursor.execute(
                "SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))"
            )
            db.commit()
        else:
            print('MYSQL : mode ONLY_FULL_GROUP_BY ok')


    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result:
        print(
            'MYSQL : lower_case_table_names =',
            result['Value'],
            '(non modifiable sous Windows)'
        )

    cursor.close()
