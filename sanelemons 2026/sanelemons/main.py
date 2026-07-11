import random
import time
from playwright.sync_api import sync_playwright
from profile_scraper import ProfileReader
from search_post_profile_scraper import scrape_hashtag_profiles

HEADLESS = True
PROFILES_PER_TAG = 60

CATEGORY_HASHTAGS = {

    "Mela & Festival Promotion": [
        "meladiaries",
        "melavibes",
        "desimela",
        "indianmela",
        "melamoments",
        "exploremela",
        "melalife",
        "melatime",
        "melareels"
    ],

    "Mela Food & Foodies": [
        "melafood",
        "melaeats",
        "foodiemela",
        "tasteofmela",
        "streetfoodmela"
    ],

    "Mela Fashion & Shopping": [
        "melalook",
        "melashopping",
        "craftmela",
        "ethnicmela",
        "handmademela"
    ],

    "Mela Photography & Visuals": [
        "melaframes",
        "colorsofmela",
        "melavibesindia",
        "festivalframes"
    ],

    "Location-Specific Melas": [
        "pushkarmeladiaries",
        "surajkundmela",
        "kumbhmelavibes",
        "rajasthanmela",
        "punjabmela",
        "upmela"
    ]
}


SESSIONS = [
    "ig_session_1.json",
    "ig_session_2.json",
    "ig_session_3.json",
    "ig_session_4.json",
    "ig_session_5.json",
     "ig_session_6.json",
    "ig_session_7.json",
    "ig_session_8.json",
    "ig_session_9.json",
    "ig_session_10.json",
]

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=80
        )

        reader = ProfileReader(browser)

        for category, hashtags in CATEGORY_HASHTAGS.items():
            print(f"\n=== CATEGORY: {category} ===", flush=True)

            for hashtag in hashtags:
                session = random.choice(SESSIONS)

                scrape_hashtag_profiles(
                    hashtag=hashtag,
                    category=category,
                    profile_limit=PROFILES_PER_TAG,
                    session_file=session,
                    reader=reader,
                    browser=browser
                )

                time.sleep(random.uniform(4, 7))

        browser.close()
