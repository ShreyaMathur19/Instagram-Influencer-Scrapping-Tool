from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.instagram.com/accounts/login/")
    print("👉 Log in manually, then press ENTER here")
    input()

    context.storage_state(path="ig_session.json")
    browser.close()

print("✅ Session saved as ig_session.json")
