# Instagram Profile Discovery Framework

A Python-based browser automation framework built with **Playwright** for discovering public Instagram profiles through hashtag exploration and collecting publicly visible profile information. The framework supports authenticated sessions, mobile browser emulation, configurable scraping workflows, and structured CSV export.

> **Disclaimer**
>
> This project is intended for educational purposes, browser automation research, and collecting publicly available information. Users are responsible for ensuring their use complies with Instagram's Terms of Use and applicable laws.

---

# Features

- Hashtag-based profile discovery
- Automated navigation using Playwright
- Mobile browser emulation
- Multi-session support using Playwright storage states
- Public profile metadata extraction
- DOM-based profile parsing
- Meta tag fallback for profile statistics
- CSV export
- Modular architecture
- Configurable scraping limits
- Error handling and recovery
- Progress logging

---

# Project Structure

```
instagram-profile-framework/
│
├── main.py
├── search_post_profile_scraper.py
├── csv_utils.py
├── config.py
│
├── output/
│   ├── usernames.csv
│   └── profiles.csv
│
├── ig_session_1.json
├── ig_session_2.json
├── ...
└── README.md
```

---

# Tech Stack

- Python 3.x
- Playwright
- Chromium
- Regular Expressions
- CSV
- JavaScript DOM Evaluation

---

# Installation

Clone the repository

```bash
git clone <repository-url>
cd instagram-profile-framework
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browsers

```bash
playwright install
```

---

# Configuration

Modify `config.py`

```python
HEADLESS = False

ACTION_DELAY_MIN = 2

ACTION_DELAY_MAX = 4

OUTPUT_DIR = "output"
```

---

# Session Setup

The framework uses Playwright storage states.

Example:

```
ig_session_1.json
ig_session_2.json
...
ig_session_10.json
```

Each session contains the authentication state for a browser profile.

---

# Running

```bash
python main.py
```

---

# Workflow

1. Load an authenticated session.
2. Open Instagram hashtag search.
3. Discover post URLs.
4. Open individual posts.
5. Extract profile username.
6. Visit public profile.
7. Extract publicly available statistics.
8. Save results to CSV.
9. Continue until configured limits are reached.

---

# Output

The framework generates two CSV files.

## profiles.csv

| username | profile_url | followers | following | posts | category |
|----------|-------------|-----------|------------|--------|-----------|

---

## usernames.csv

Contains the discovered usernames together with associated profile information.

---

# Configuration Parameters

| Variable | Description |
|----------|-------------|
| PROFILES_PER_TAG | Profiles collected per hashtag |
| MAX_SCROLL_ROUNDS | Maximum hashtag scrolling rounds |
| ACTION_DELAY_MIN | Minimum delay between actions |
| ACTION_DELAY_MAX | Maximum delay between actions |
| HEADLESS | Browser visibility |
| SESSION_COOLDOWN_SECONDS | Cooldown between sessions |

---

# Core Components

### main.py

Coordinates the scraping pipeline.

Responsible for:

- Session management
- Hashtag scheduling
- Progress tracking
- Cooldowns
- Failure handling

---

### search_post_profile_scraper.py

Responsible for

- Hashtag exploration
- Profile discovery
- Profile parsing
- Public statistics extraction
- Login wall detection
- Mobile browser emulation

---

### csv_utils.py

Handles

- CSV creation
- Duplicate prevention
- Data persistence

---

### config.py

Contains all configurable runtime parameters.

---

# Browser Automation

The framework uses Playwright Chromium with

- Mobile browser emulation
- Touch support
- Custom User-Agent
- Authenticated browser sessions
- Configurable delays

---

# Data Extraction

The framework extracts publicly available information including

- Username
- Profile URL
- Followers
- Following
- Number of Posts
- Source Hashtag

Data is collected using:

- DOM evaluation
- HTML parsing
- Meta tag extraction (fallback)

---

# Logging

Example output

```
[PIPELINE] Started

[SESSION START] ig_session_1.json

[TAG START] #travel

[PROFILE FOUND] @example

[PROFILE SAVED] @example | followers=12500

[ROUND SUMMARY] saved=120

[SESSION DONE]
```

---

# Requirements

- Python 3.10+
- Playwright
- Chromium Browser

---

# Future Improvements

- Database support
- PostgreSQL integration
- Async Playwright
- Parallel scraping
- Better retry strategies
- Structured logging
- Docker support
- Cloud deployment
- Monitoring dashboard

---

# License

This project is released for educational and research purposes.

Users are responsible for ensuring compliance with the terms of service of any platform they interact with.

---

# Author

**Shreya Mathur**

Python Developer | Browser Automation | Web Automation | Playwright
