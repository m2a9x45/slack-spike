from dao import db


def create(path_id, command, worflow_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "INSERT INTO commands (path_id, command, workflow_id) VALUES (%s, %s, %s)"
    val = (path_id, command, worflow_id)
    cursor.execute(sql, val)

    con.commit()


def get_all():
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    cursor.execute('SELECT * FROM commands')

    result = cursor.fetchall()
    return result


def get_by_id(command):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM commands WHERE command = %s"
    val = (command, )
    cursor.execute(sql, val)

    return cursor.fetchall()
