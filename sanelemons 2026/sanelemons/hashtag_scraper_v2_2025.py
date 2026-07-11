 # hashtag_scraper.py

import time
import random
from playwright.sync_api import sync_playwright, TimeoutError

from config import *
from csv_utils import save_username
from profile_scraper import scrape_profile_from_page

print("🔥 RUNNING ROUND-BASED HASHTAG SCRAPER", flush=True)
print("📍 FILE:", __file__, flush=True)

MAX_SCROLL_ROUNDS = 40
NO_NEW_ROUNDS_STOP = 6
SCROLL_PIXELS = 6000
SCROLL_SLEEP = 1.5


# --------------------------------------------------
# ✅ FINAL CORRECT POST TYPE DETECTION (2025 SAFE)
#
# REAL POST:
#   - Has at least one CONTENT image (srcset or width)
# REEL:
#   - Video-only OR no content images
# --------------------------------------------------
def is_real_post(page):
    try:
        # content images only (ignore avatars/icons)
        content_imgs = page.locator(
            "article img[srcset], article img[width]"
        ).count()

        video_count = page.locator("article video").count()

        # image or carousel post
        if content_imgs > 0:
            return True

        # reel / video-only
        if video_count > 0:
            return False

        return False
    except:
        return False


def scrape_hashtag(hashtag, post_limit, session_file, round_no):
    print(f"\n[TAG START] #{hashtag}", flush=True)

    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    processed = set()
    all_links = []
    saved_profiles = 0
    no_new_rounds = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        try:
            ctx = browser.new_context(storage_state=session_file)
            tag_page = ctx.new_page()
            post_page = ctx.new_page()

            tag_page.set_default_timeout(8000)
            post_page.set_default_timeout(30000)

            tag_page.goto(url, timeout=60000)
            tag_page.wait_for_timeout(PAGE_LOAD_WAIT)

            # force grid render
            tag_page.evaluate("window.scrollTo(0, 900)")
            tag_page.wait_for_timeout(1500)
            tag_page.evaluate("window.scrollTo(0, 0)")
            tag_page.wait_for_timeout(1000)

            # login wall detection
            try:
                if tag_page.locator("text=Log in").first.is_visible():
                    print("[LOGIN WALL] Session invalid", flush=True)
                    return (0, 0)
            except:
                pass

            for scroll_round in range(1, MAX_SCROLL_ROUNDS + 1):
                print(
                    f"[SCROLL] round={scroll_round}, collected={len(all_links)}, "
                    f"processed={len(processed)}, saved={saved_profiles}",
                    flush=True
                )

                before = len(all_links)

                # collect ONLY /p/ links
                tag_page.wait_for_timeout(800)
                hrefs = tag_page.locator(
                    "a[href^='/p/']"
                ).evaluate_all(
                    "els => els.map(e => e.getAttribute('href')).filter(Boolean)"
                )

                for href in hrefs:
                    link = "https://www.instagram.com" + href
                    if link not in all_links:
                        all_links.append(link)

                new_links = all_links[before:]
                print(f"[LINKS] +{len(new_links)} new", flush=True)

                if not new_links:
                    no_new_rounds += 1
                    if no_new_rounds >= NO_NEW_ROUNDS_STOP:
                        print("[STOP] No new posts", flush=True)
                        break
                else:
                    no_new_rounds = 0

                for link in new_links:
                    if len(processed) >= post_limit:
                        break
                    if link in processed:
                        continue

                    processed.add(link)
                    print(f"[POST] {len(processed)}/{post_limit} → {link}", flush=True)

                    try:
                        # fast & safe navigation
                        try:
                            post_page.goto(
                                link,
                                wait_until="domcontentloaded",
                                timeout=30000
                            )
                        except TimeoutError:
                            print("[RETRY] Reload after timeout", flush=True)
                            post_page.reload(
                                wait_until="domcontentloaded",
                                timeout=30000
                            )

                        time.sleep(1.5)

                        # 🚫 DISCARD ONLY TRUE REELS
                        if not is_real_post(post_page):
                            print("[DISCARD] Reel / video post", flush=True)
                            continue

                        # extract post owner from header ONLY
                        href = post_page.locator(
                            "header a[href^='/']"
                        ).first.get_attribute("href")

                        if not href:
                            print("[SKIP] Username not found", flush=True)
                            continue

                        username = href.strip("/")

                        if username.lower() in {"reels", "explore"}:
                            continue

                        save_username(username, f"hashtag:{hashtag}")

                        ok = scrape_profile_from_page(
                            post_page, username, hashtag
                        )

                        if ok:
                            saved_profiles += 1

                        time.sleep(random.uniform(
                            ACTION_DELAY_MIN, ACTION_DELAY_MAX
                        ))

                    except Exception as e:
                        print(f"[SKIP] Post error: {e}", flush=True)

                tag_page.mouse.wheel(0, SCROLL_PIXELS)
                tag_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(SCROLL_SLEEP)

            print(
                f"[TAG DONE] #{hashtag} saved={saved_profiles} "
                f"attempted={len(processed)}",
                flush=True
            )
            return (saved_profiles, len(processed))

        finally:
            browser.close()
