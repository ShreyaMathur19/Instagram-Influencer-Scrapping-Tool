import re
import time
import random
from excel_utils import save_profile_excel

# 🔥 FOLLOWER RANGE FILTER
MIN_FOLLOWERS = 50_000   # ✅ minimum 50K followers

DELAY_RANGE = (4.5, 7.5)

def normalize_count(value):
    if not value:
        return None
    value = value.replace(",", "").upper()
    if value.endswith("K"):
        return int(float(value[:-1]) * 1000)
    if value.endswith("M"):
        return int(float(value[:-1]) * 1_000_000)
    return int(value)

class ProfileReader:
    def __init__(self, browser):
        self.browser = browser
        self.seen = set()

    def scrape_and_save(self, username, category):
        if username in self.seen:
            return False
        self.seen.add(username)

        page = self.browser.new_page()
        profile_url = f"https://www.instagram.com/{username}/"

        try:
            page.goto(profile_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)

            desc = page.evaluate("""
            () => document.querySelector("meta[property='og:description']")?.content || ""
            """)

            m = re.search(
                r"([\d.,KMB]+)\sFollowers.*?"
                r"([\d.,KMB]+)\sFollowing.*?"
                r"([\d.,KMB]+)\sPosts",
                desc
            )

            if not m:
                return False

            followers = normalize_count(m.group(1))
            following = normalize_count(m.group(2))
            posts = normalize_count(m.group(3))

            # 🚫 Skip profiles below 50K followers
            if not followers or followers < MIN_FOLLOWERS:
                print(f"[SKIPPED] @{username} ({followers}) - below 50K", flush=True)
                return False

            save_profile_excel({
                "username": username,
                "profile_url": profile_url,
                "followers": followers,
                "following": following,
                "posts": posts,
                "category": category,
            })

            print(f"[SAVED] @{username} ({followers})", flush=True)
            time.sleep(random.uniform(*DELAY_RANGE))
            return True

        finally:
            page.close()