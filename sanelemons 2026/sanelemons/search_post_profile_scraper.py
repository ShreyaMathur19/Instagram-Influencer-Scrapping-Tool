import time
import random

MAX_SCROLL_ROUNDS = 25


def scrape_hashtag_profiles(
    hashtag,
    category,
    profile_limit,
    session_file,
    reader,
    browser
):
    print(f"\n[TAG START] #{hashtag} | CATEGORY={category}", flush=True)

    search_url = f"https://www.instagram.com/explore/tags/{hashtag}/"

    collected = set()
    seen_posts = set()
    saved = 0
    no_new_rounds = 0

    ctx = browser.new_context(
        storage_state=session_file,
        viewport={"width": 390, "height": 844}
    )
    page = ctx.new_page()
    page.set_default_timeout(20000)

    try:
        page.goto(search_url, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        for round_no in range(MAX_SCROLL_ROUNDS):
            posts = page.locator("a[href^='/p/']")
            count = posts.count()
            new_found = False

            print(f"[SCROLL ROUND {round_no+1}] posts_in_dom={count}", flush=True)

            for i in range(count):
                if saved >= profile_limit:
                    return

                post_url = posts.nth(i).get_attribute("href")
                if not post_url or post_url in seen_posts:
                    continue

                seen_posts.add(post_url)

                try:
                    posts.nth(i).click()
                    page.wait_for_timeout(2500)

                    username = page.evaluate("""
                    () => {
                        const a = document.querySelector("header a[href^='/']");
                        return a ? a.getAttribute("href").replaceAll("/", "") : null;
                    }
                    """)

                    page.keyboard.press("Escape")
                    page.wait_for_timeout(1000)

                    if not username or username in collected:
                        continue

                    collected.add(username)
                    new_found = True

                    print(f"[PROFILE FOUND ✔] @{username}", flush=True)

                    if reader.scrape_and_save(username, category):
                        saved += 1

                    time.sleep(random.uniform(2.5, 5.5))

                except Exception as e:
                    print("[POST ERROR]", e, flush=True)

            if not new_found:
                no_new_rounds += 1
                print(f"[NO NEW POSTS] {no_new_rounds}", flush=True)
            else:
                no_new_rounds = 0

            if no_new_rounds >= 2:
                print(f"[EXHAUSTED] #{hashtag}", flush=True)
                return

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000)

    finally:
        page.close()
        ctx.close()