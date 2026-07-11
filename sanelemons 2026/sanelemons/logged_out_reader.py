import re
import time
import random
from csv_utils import save_profile, save_username

MOBILE_UA = (
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Mobile Safari/537.36"
)

MAX_PER_CONTEXT = 12
DELAY_RANGE = (4.5, 7.5)

class LoggedOutReader:
    def __init__(self, browser):
        self.browser = browser
        self.ctx = None
        self.count = 0
        self._new_ctx()

    def _new_ctx(self):
        if self.ctx:
            self.ctx.close()

        self.ctx = self.browser.new_context(
            storage_state=None,
            user_agent=MOBILE_UA,
            is_mobile=True,
            has_touch=True,
            locale="en-US",
            timezone_id="Asia/Kolkata"
        )
        self.count = 0
        print("[LOGGED-OUT] New context", flush=True)

    def _login_wall(self, page):
        return page.evaluate("""
        () => !!(
            document.querySelector("input[name='username']") ||
            document.querySelector("form[action*='login']")
        )
        """)

    def scrape(self, username, category):
        if self.count >= MAX_PER_CONTEXT:
            self._new_ctx()

        page = self.ctx.new_page()
        profile_url = f"https://www.instagram.com/{username}/"

        followers = following = posts = ""

        try:
            page.goto(profile_url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(800)

            if self._login_wall(page):
                print("[LOGIN WALL] Rotating context", flush=True)
                page.close()
                self._new_ctx()
                return False

            desc = page.evaluate("""
            () => document.querySelector("meta[property='og:description']")?.content || null
            """)

            if desc:
                m = re.search(
                    r"([\d.,KMB]+)\sFollowers,?\s([\d.,KMB]+)\sFollowing,?\s([\d.,KMB]+)\sPosts",
                    desc
                )
                if m:
                    followers, following, posts = m.groups()

        finally:
            page.close()

        self.count += 1
        time.sleep(random.uniform(*DELAY_RANGE))

        data = {
            "username": username,
            "profile_url": profile_url,
            "followers": followers,
            "following": following,
            "posts": posts,
            "category": category
        }

        save_profile(data)
        save_username(data)

        print(f"[PROFILE SAVED] @{username} | followers={followers or 'N/A'}", flush=True)
        return True
