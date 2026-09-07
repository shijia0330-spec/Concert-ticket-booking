# AI Playwright — EventHub

Python + pytest-playwright practice project for [EventHub](https://eventhub.rahulshettyacademy.com/).

You own the business steps and asserts. Page objects hold locators; tests hold the flow.

## Setup (once)

```bash
cd ~/AI-playwright   # or your clone path
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

Edit `.env` with your EventHub email / password (never commit `.env`).

## Run tests locally

```bash
source .venv/bin/activate
pytest booking_system/test_cases --headed    # watch browser
pytest booking_system/test_cases             # headless (like CI)
```

## CI/CD (GitHub Actions)

Workflow file: `.github/workflows/playwright.yml`

### 1. Put the project on GitHub

```bash
cd ~/AI-playwright
git init
git add .
git commit -m "Add EventHub Playwright tests and CI"
# create a repo on GitHub, then:
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

### 2. Add secrets (required)

GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Secret | Value |
|--------|--------|
| `COURSE_EMAIL` | your EventHub email |
| `COURSE_PASSWORD` | your EventHub password |

### 3. What CI does

On every push / PR to `main` (and on manual **Run workflow**):

1. Install Python + dependencies  
2. Install Chromium  
3. Write `.env` from secrets  
4. Run `pytest booking_system/test_cases` (headless)  
5. On failure, upload `test-results/` as an artifact  

Open the **Actions** tab on GitHub to see green/red runs.

## Layout

| Path | What it is |
|------|------------|
| `booking_system/pages/` | Page objects (locators + actions) |
| `booking_system/test_cases/` | E2E tests + case docs (`*_testcases.md`) |
| `booking_system/conftest.py` | Fixtures |
| `.github/workflows/playwright.yml` | CI pipeline |
| `.cursor/skills/` | Skills for testcase / Playwright help |
