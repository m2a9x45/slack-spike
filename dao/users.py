from dao import db


def create(slack_user_id, slack_team_id, email, name, profile_img, access_token):
    con = db.get_connection()
    cursor = con.cursor(dictionary=True)

    sql = "INSERT INTO users (slack_user_id, slack_team_id, email, name, profile_img, access_token) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (slack_user_id, slack_team_id, email,
           name, profile_img, access_token)
    cursor.execute(sql, val)

    con.commit()
