from dao import db


def set_command(data):
    con = db.get_connection()
    cursor = con.cursor()

    sql = "INSERT INTO commands (path_id, command, workflow_id) VALUES (%s, %s, %s)"
    val = (data["path_id"], data["command"], data["workflow_id"])
    cursor.execute(sql, val)

    con.commit()

    print(cursor.rowcount, "record inserted.")
