import mysql.connector
from db_config import DB_CONFIG

INSERT_SQL = """
INSERT IGNORE INTO instagram_profiles (
    username,
    profile_url,
    followers,
    following,
    posts,

)
VALUES (%s, %s, %s, %s, %s);
"""

def upsert_profile(data):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        INSERT_SQL,
        (
            data.get("username"),
            data.get("profile_url"),
            data.get("followers"),
            data.get("following"),
            data.get("posts"),
            
        )
    )

    conn.commit()

    # 🔍 Check if row was actually inserted
    if cur.rowcount == 1:
        print(f"[MYSQL INSERTED] @{data.get('username')}", flush=True)
    else:
        print(f"[MYSQL DUPLICATE SKIPPED] @{data.get('username')}", flush=True)

    cur.close()
    conn.close()
