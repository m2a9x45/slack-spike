from dao import db


def list_all_wf_steps_by_id(wf_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_steps WHERE wf_id = %s"
    val = (wf_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()


def get_step_by_id(wf_id, step_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_steps WHERE wf_id = %s AND step_id = %s"
    val = (wf_id, step_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()


def get_branches_by_step_id(step_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_branches WHERE step_id = %s"
    val = (step_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()


def get_branches_by_action_id(action_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_branches WHERE action_id = %s"
    val = (action_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()


def get_model_options_by_step_id(step_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_options WHERE step_id = %s"
    val = (step_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()
