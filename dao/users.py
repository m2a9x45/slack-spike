from dao import db


def create(slack_user_id, slack_team_id, email, name, profile_img, access_token):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "INSERT INTO users (slack_user_id, slack_team_id, email, name, profile_img, access_token) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (slack_user_id, slack_team_id, email,
           name, profile_img, access_token)
    cursor.execute(sql, val)

    con.commit()


def find_by_slack_id(slack_user_id):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE slack_user_id = %s"
    val = (slack_user_id, )
    cursor.execute(sql, val)

    return cursor.fetchall()
