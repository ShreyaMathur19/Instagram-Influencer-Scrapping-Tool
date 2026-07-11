import csv
import os
from config import OUTPUT_DIR

# --------------------------------------------------
# PATHS
# --------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

USERNAMES_FILE = os.path.join(OUTPUT_DIR, "usernames.csv")
PROFILES_FILE  = os.path.join(OUTPUT_DIR, "profiles.csv")

print("✅ USERNAMES_FILE =", USERNAMES_FILE, flush=True)
print("✅ PROFILES_FILE  =", PROFILES_FILE, flush=True)

# --------------------------------------------------
# HEADERS
# --------------------------------------------------
HEADERS = [
    "username",
    "profile_url",
    "followers",
    "following",
    "posts",
    "category",
]

# --------------------------------------------------
# INTERNAL CACHE (PERSISTENT)
# --------------------------------------------------
_seen_usernames = set()
_seen_profiles = set()


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def _ensure_file(path):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()


def _normalize_username(data):
    return (data.get("username") or "").strip().lower()


def _clean_row(data):
    return {h: data.get(h, "") for h in HEADERS}


def _load_existing_usernames(path, target_set):
    if not os.path.exists(path):
        return

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = (row.get("username") or "").strip().lower()
            if u:
                target_set.add(u)


# --------------------------------------------------
# LOAD EXISTING DATA ON START
# --------------------------------------------------
_load_existing_usernames(USERNAMES_FILE, _seen_usernames)
_load_existing_usernames(PROFILES_FILE, _seen_profiles)


# --------------------------------------------------
# SAVE FUNCTIONS
# --------------------------------------------------
def save_username(data):
    username = _normalize_username(data)
    if not username or username in _seen_usernames:
        return False

    _ensure_file(USERNAMES_FILE)

    with open(USERNAMES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(_clean_row(data))

    _seen_usernames.add(username)
    return True


def save_profile(data):
    username = _normalize_username(data)
    if not username or username in _seen_profiles:
        return False

    _ensure_file(PROFILES_FILE)

    with open(PROFILES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(_clean_row(data))

    _seen_profiles.add(username)
    return True
