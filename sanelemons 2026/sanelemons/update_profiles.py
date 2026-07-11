import time
import random
from playwright.sync_api import sync_playwright

from config import *
from profile_scraper import ProfileReader
from db_fetch_utils import fetch_all_usernames
from db_update_utils import update_profile


DELAY_RANGE = (5, 9)
MAX_PROFILES_PER_SESSION = 300


def run_update():
    usernames = fetch_all_usernames()
    print(f"[UPDATE] Total profiles to refresh: {len(usernames)}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=80
        )

        reader = ProfileReader(browser)
        updated = 0

        for username in usernames:
            try:
                data = reader.scrape_for_update(username)

                if not data:
                    continue

                update_profile(data)
                updated += 1

                print(
                    f"[MYSQL UPDATED] @{username} | followers={data['followers']}",
                    flush=True
                )

                time.sleep(random.uniform(*DELAY_RANGE))

                if updated >= MAX_PROFILES_PER_SESSION:
                    print("[LIMIT] Update session limit reached", flush=True)
                    break

            except Exception as e:
                print(f"[UPDATE ERROR] @{username} → {e}", flush=True)
                continue

        browser.close()

    print(f"[UPDATE DONE] Updated profiles: {updated}", flush=True)


if __name__ == "__main__":
    run_update()
