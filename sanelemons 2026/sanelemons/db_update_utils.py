import mysql.connector
from db_config import DB_CONFIG

UPDATE_SQL = """
UPDATE instagram_profiles
SET
    profile_url = %s,
    followers   = %s,
    following   = %s,
    posts       = %s,
    last_updated = CURRENT_TIMESTAMP
WHERE username = %s;
"""

def update_profile(data):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        UPDATE_SQL,
        (
            data.get("profile_url"),
            data.get("followers"),
            data.get("following"),
            data.get("posts"),
           
            data.get("username"),
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    print(f"[MYSQL UPDATED] @{data.get('username')}", flush=True)
