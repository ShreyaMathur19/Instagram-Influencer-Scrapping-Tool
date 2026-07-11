import time, random
from playwright.sync_api import sync_playwright, TimeoutError
from config import *
from csv_utils import save_username

def scrape_post_likers(post_url, limit=3000):

    # ❌ Skip reels (likes modal often disabled)
    if "/reel/" in post_url:
        print("[SKIP] Reel detected")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(storage_state="ig_session.json")
        page = context.new_page()

        page.goto(post_url, timeout=60000)
        page.wait_for_timeout(PAGE_LOAD_WAIT)

        opened = False

        # ✅ Strategy 1: aria-label (MOST RELIABLE)
        try:
            page.locator("button[aria-label*='like']").first.click(timeout=5000)
            opened = True
        except:
            pass

        # ✅ Strategy 2: likes link (/liked_by/)
        if not opened:
            try:
                page.locator("a[href*='/liked_by/']").first.click(timeout=5000)
                opened = True
            except:
                pass

        # ✅ Strategy 3: span text → click parent
        if not opened:
            try:
                likes_text = page.locator("span:has-text('likes')").first
                likes_text.evaluate("el => el.closest('a')?.click()")
                opened = True
            except:
                pass

        if not opened:
            print("[SKIP] Likes modal not clickable for this post")
            browser.close()
            return

        # ✅ Wait for modal
        page.wait_for_timeout(3000)
        modal = page.locator("div[role='dialog']")

        collected = set()
        last_count = 0

        while len(collected) < limit:
            users = modal.locator("a").all()
            for u in users:
                href = u.get_attribute("href")
                if href and href.count("/") == 2:
                    collected.add(href.strip("/"))

            # 🛑 stop if no new users
            if len(collected) == last_count:
                break
            last_count = len(collected)

            page.mouse.wheel(0, 4000)
            time.sleep(2)

        browser.close()

        for username in collected:
            save_username(username, "liker")

        print(f"[OK] {len(collected)} likers saved")

        time.sleep(random.uniform(ACTION_DELAY_MIN, ACTION_DELAY_MAX))
