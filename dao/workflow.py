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


def get_wf_id_by_action_id(action_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT wf_id FROM wf_branches AS b INNER JOIN wf_steps AS s ON b.step_id=s.step_id WHERE action_id = %s"
    val = (action_id, )
    cursor.execute(sql, val)

    return cursor.fetchone()


def get_model_options_by_step_id(step_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_options WHERE step_id = %s"
    val = (step_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()


def update_workflow_step(step_id, message):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "UPDATE wf_steps SET message = %s WHERE step_id = %s"
    val = (message, step_id)
    cursor.execute(sql, val)
    con.commit()

    return cursor.rowcount


def update_branch(id, next_step_id, message):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "UPDATE wf_branches SET next_step_id=%s, text=%s WHERE id = %s"
    val = (next_step_id, message, id)
    cursor.execute(sql, val)
    con.commit()

    return cursor.rowcount


def create_step(wf_id, step_id, action, message):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "INSERT INTO wf_steps (wf_id, step_id, action, message) VALUES (%s, %s, %s, %s)"
    val = (wf_id, step_id, action, message)
    cursor.execute(sql, val)
    con.commit()

    return cursor.rowcount


def create_step_location(wf_id, step_id, left, top):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "INSERT INTO wf_steps_position (wf_id, step_id, `left`, top) VALUES (%s, %s, %s, %s)"
    val = (wf_id, step_id, left, top)
    cursor.execute(sql, val)
    con.commit()

    return cursor.rowcount


def update_step_location(step_id, left, top):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "UPDATE wf_steps_position SET `left`=%s, top=%s WHERE step_id=%s"
    val = (left, top, step_id)
    cursor.execute(sql, val)
    con.commit()

    return cursor.rowcount


def read_step_locations(step_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_steps_position WHERE step_id = %s"
    val = (step_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()


def list_step_locations_by_wf_id(wf_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM wf_steps_position WHERE wf_id = %s"
    val = (wf_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()


def create_branch(step_id, action_id, next_step_id, text):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "INSERT INTO wf_branches (step_id, action_id, next_step_id, text) VALUES (%s, %s, %s, %s)"
    val = (step_id, action_id, next_step_id, text)
    cursor.execute(sql, val)
    con.commit()

    return cursor.rowcount
