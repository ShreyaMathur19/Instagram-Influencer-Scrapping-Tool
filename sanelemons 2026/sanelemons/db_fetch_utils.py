import mysql.connector
from db_config import DB_CONFIG

def fetch_all_usernames(limit=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    sql = "SELECT username FROM instagram_profiles"
    if limit:
        sql += f" LIMIT {int(limit)}"

    cur.execute(sql)
    usernames = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return usernames
