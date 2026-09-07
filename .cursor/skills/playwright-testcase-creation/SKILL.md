---
name: playwright-testcase-creation
description: >-
  Creates Python pytest-playwright test cases for this AI Playwright project
  (EventHub booking under booking_system/). Use when the user asks to create,
  add, scaffold, or generate a test case, E2E flow, or parameterized Playwright
  test; or when they provide business steps and an assert for automation.
---

# Playwright testcase creation

## Hard rules (never break)

- **User owns** business steps, the assert, and credentials in `.env` (never commit `.env`).
- **Do not** add a new test until the user lists **steps** and **assert**.
- **Do not** change or delete an assert to make a test green.
- Python + pytest-playwright only — no TypeScript / `.spec.ts`, no Appium unless asked.
- Prefer `get_by_role`, `get_by_label`, `get_by_placeholder`, `get_by_test_id`.
- Wait with `expect(...).to_be_visible()` — never random `time.sleep`.
- No long XPath or click-by-coordinates as the first choice.
- Do not copy paid Udemy lecture source into the repo.

## Project layout

```text
booking_system/
  conftest.py          # fixtures + params
  pages/               # locators + actions only
  test_cases/          # thin steps + assert (pytest)
.env                   # BASE_URL, email, password (project root)
```

Default app: [EventHub](https://eventhub.rahulshettyacademy.com/login) via `BASE_URL`.

## Before writing code — collect from user

If any are missing, ask (do not invent the assert):

1. **URL** (or confirm EventHub login URL)
2. **Steps** in order (e.g. login → find event → book → confirm)
3. **Assert** — exact “pass” condition (visible text, URL, etc.)
4. **Data to parameterize** (optional) — event names, ticket counts, etc.

Credentials: tell the user to put them in `.env`; do not hardcode secrets in tests.

## Creation workflow

Copy and track:

```text
Testcase progress:
- [ ] Steps + assert confirmed
- [ ] Page object methods for new screens
- [ ] Fixtures wired (or reused) in conftest.py
- [ ] Parameterization if user gave multiple data rows
- [ ] Thin test in booking_system/test_cases/
- [ ] Assert left exactly as user specified
```

### 1. Page objects (`booking_system/pages/`)

- One class per screen; inherit `BasePage` when useful.
- Methods = user actions (`login`, `select_event`, `book_tickets`).
- Locators stay inside pages — not in the test file.
- Reuse existing pages when the screen already exists; add new files only for new screens.

### 2. Fixtures (`booking_system/conftest.py`)

- Config from `.env` (`course_config` or a clear EventHub-named fixture).
- Page fixtures: `def login_page(page): return LoginPage(page)`.
- Parameterize with fixture `params=` **or** `@pytest.mark.parametrize` — prefer one clear pattern per suite.
- Skip (don’t fail) if credentials are still placeholders / missing.

### 3. Test file (`booking_system/test_cases/test_*.py`)

Template:

```python
def test_<flow_name>(
    login_page,
    # other page fixtures...
    course_config,
    # parameterized fixture or mark params...
):
    # Business steps only — call page methods
    ...
    # User-owned assert — do not weaken
    assert <user_condition>
```

- Keep the test thin: steps + assert.
- Name files `test_<flow>.py`; functions `test_*`.

### 4. After a red run

1. Read pytest error and any `test-results/` screenshot.
2. Classify: locator, wait, or real product bug.
3. Patch **only** locator or wait in `pages/`.
4. Keep the original assert.

## Parameterization checklist

- Multiple events/products → fixture `params=` from env (`COURSE_PRODUCTS` / similar) or `@pytest.mark.parametrize`.
- Give readable `ids=` when using fixture params.
- Do not parameterize **valid** credentials in source; keep them in `.env`.

## Negative login (invalid username / password)

- Supported: separate `test_login_invalid*.py` or parametrize invalid pairs.
- Use **fake** invalid emails/passwords in the test (or `INVALID_*` in `.env`) — never put real secrets in the skill or repo docs.
- Prefer `LoginPage.submit_credentials()` (no success wait). Do **not** call `login()` for invalid cases.
- User still owns the assert, e.g. stay on `/login`, error text visible, Sign In still shown.
- Do not invent a specific error string unless the user provided it.

## Out of scope for this skill

- Weakening asserts
- Generating tests from guessed flows without user steps/assert
- Porting TypeScript Playwright specs
- Framework rewrites unrelated to the requested testcase
