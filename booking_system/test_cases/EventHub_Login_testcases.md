# EventHub Login test cases

## Document info
- Based on requirements: `booking_system/test_cases/EventHub_Login_requirements.md` (observed UI scope; no formal PRD)
- Generator version: rules 1.2.0 (skills V3 · testcase-generator, English)
- RAG retrieval: 5 hits (query: EventHub Login test cases / rules / acceptance / boundary) — **all sample seckill content; not adopted** (conflict with EventHub scope)
- Scope: EventHub **Login** page only (`/login`) — Sign In with email/password; success vs reject
- Structure: 3 levels (H2 → H3 → H4)
- Open questions total: 6

## Knowledge-base retrieval summary

RAG returned seckill/Redis sample bugs and planner docs — **not applicable** to EventHub Login.  
Documented as `RAG: hits unrelated — treat as no usable hits for this module`.

## Requirements traceability

| Requirement section | Case IDs | Notes |
|---------------------|----------|-------|
| Login page fields & Sign In | F-01, V-01…V-07, G via V/P | Observed UI |
| Success → authenticated home / Logout | F-01, P-01 | Observed: Logout visible |
| Invalid credentials must not grant access | F-02, V-05, V-06, P-02 | Exact error copy TBD (T-01) |
| Register entry on page | T-02 | Out of scope until clarified |
| Password min length (API observed ≥6) | V-03, V-04, T-03 | Confirm UI vs API rule |
| Events / Bookings / Admin | — | Explicitly out of scope |

## Core-flow tests

### Flow 1: Sign in with valid credentials → authenticated home

```text
Open /login
  → Enter valid email + password
  → Click Sign In
  → Land on home (not /login)
  → Logout control is available
```

#### F-01 Valid credentials reach home and show Logout <!-- P0 -->
- On `https://eventhub.rahulshettyacademy.com/login`, enter a valid registered email and password, click **Sign In**; URL leaves `/login` and the **Logout** control is visible

### Flow 2: Sign in with invalid credentials → remain unauthenticated

```text
Open /login
  → Enter invalid email and/or password
  → Click Sign In
  → Remain unauthenticated (still on login / no Logout)
```

#### F-02 Invalid credentials do not grant Logout/home access <!-- P0 -->
- On the login page, enter a non-registered email with a password of at least 6 characters (e.g. `invalid@example.com` / `WrongPass1`), click **Sign In**; page stays on `/login` (or equivalent unauthenticated state) and **Logout** is not shown

## Detailed feature tests

### Login form — input validation

#### V-01 Submit with empty email and empty password <!-- P1 -->
- Leave Email and Password empty, click **Sign In**; login does not succeed (no Logout / still unauthenticated); validation or error feedback is shown (exact copy → T-01)

#### V-02 Submit with email filled and password empty <!-- P1 -->
- Enter a well-formed email, leave Password empty, click **Sign In**; login does not succeed; password-related validation or error is shown (exact copy → T-01)

#### V-03 Password shorter than 6 characters is rejected <!-- P1 -->
- Enter a well-formed email and password `12345` (5 chars), click **Sign In**; login does not succeed (aligns with observed API min length 6; if UI allows submit, server/UI must still block — confirm T-03)

#### V-04 Password exactly 6 characters with wrong account stays failed <!-- P2 -->
- Enter `invalid@example.com` and password `abcdef` (exactly 6), click **Sign In**; login does not succeed; still unauthenticated

#### V-05 Malformed email format is rejected or blocked <!-- P1 -->
- Enter Email `not-an-email` and a password of 6+ chars, click **Sign In**; login does not succeed; email-format feedback appears or field prevents continue (exact behavior → T-04)

#### V-06 Wrong password for a known-format email does not authenticate <!-- P1 -->
- Enter a syntactically valid email that is not the user’s account (or wrong password for a real account if product allows), click **Sign In**; no Logout; remain on login / unauthenticated

#### V-07 Email and password fields accept normal printable input without crash <!-- P3 -->
- Enter a normal email and password containing letters+digits+symbol (e.g. `Test1!`), click **Sign In**; page does not crash; result is either success (if account matches) or controlled failure (no stack trace / blank error page)

### Auth / session

#### P-01 After successful login, Logout is available <!-- P0 -->
- Complete F-01; **Logout** is visible and clickable on the authenticated home chrome

#### P-02 Unauthenticated user opening `/login` sees Sign In, not Logout <!-- P1 -->
- Open `/login` in a fresh session (no prior login); **Sign In** is visible and **Logout** is not shown

#### P-03 Double-click Sign In with valid credentials does not break auth <!-- P2 -->
- On `/login` with valid credentials, double-click **Sign In** quickly; end state is a single successful authenticated session (or a clear single error) — no blank page / uncaught error (exact double-submit rule → T-05)

### Register entry (matrix trigger only)

#### T-02 Register link behavior (to clarify) <!-- P3 -->
- （待澄清）Login page shows **Register** — confirm target URL, required fields, and whether Register is in scope for this module

## Case review table

| ID | Name | Priority | Type | Tags |
|----|------|----------|------|------|
| F-01 | EventHub > Login > Valid credentials → home + Logout | P0 | smoke_sanity | login,happy |
| F-02 | EventHub > Login > Invalid credentials → no access | P0 | smoke_sanity | login,negative |
| V-01 | EventHub > Login > Empty email and password | P1 | boundary | validation |
| V-02 | EventHub > Login > Empty password only | P1 | boundary | validation |
| V-03 | EventHub > Login > Password length 5 rejected | P1 | boundary | validation |
| V-04 | EventHub > Login > Password length 6 wrong account fails | P2 | boundary | validation |
| V-05 | EventHub > Login > Malformed email | P1 | boundary | validation |
| V-06 | EventHub > Login > Wrong credentials fail | P1 | functional | negative |
| V-07 | EventHub > Login > Normal input no crash | P3 | functional | resilience |
| P-01 | EventHub > Login > Logout visible after success | P0 | security | session |
| P-02 | EventHub > Login > Fresh session shows Sign In only | P1 | security | session |
| P-03 | EventHub > Login > Double-click Sign In | P2 | functional | consistency |
| T-02 | EventHub > Login > Register link (to clarify) | P3 | pending_clarification | register |

P0 count: 3 / 13 ≈ 23% — slightly over 20%; acceptable for a tiny login-only module (core auth). Drop P-01 to P1 if strict P0 cap is required.

## Universal coverage matrix self-check

| Dimension | Triggered? | Covered / to clarify | Notes |
|-----------|------------|----------------------|-------|
| A Input & validation | Yes | Covered V-01…V-07; T-01/T-03/T-04 | Form fields present |
| B List & query | No | — | Login has no list |
| C Auth & roles | Yes | F-01/F-02, P-01…P-03 | Login module |
| D Resource by ID | No | — | Not in scope |
| E Time & state | No | — | No activity window on login |
| F Repeat & consistency | Yes | P-03; T-05 | Double submit |
| G Errors & usability | Yes | V-*; T-01 | Exact copy TBD |
| H API contract | No (no OpenAPI file) | T-06 | API base known but not in this UI doc |
| I NFR appendix | No | — | Not requested |

## Open questions

| # | Question | Related IDs |
|---|----------|-------------|
| T-01 | Exact UI error text/toast for failed login and empty fields? | V-01, V-02, F-02, V-06 |
| T-02 | Is **Register** in scope? Target page and acceptance rules? | T-02 |
| T-03 | Is password minimum length **6** enforced in UI, API, or both? | V-03, V-04 |
| T-04 | Malformed email: client-side block vs server 400 message? | V-05 |
| T-05 | Double-click Sign In: ignore 2nd click, or show duplicate warning? | P-03 |
| T-06 | Should a separate **API** login case pack be generated next (OpenAPI / `api.eventhub…`)? | — |

---

**Automation (Playwright):** mapped in `test_login_flows.py` (F/P) and `test_login_validation.py` (V). **T-02** not automated (pending clarification).

```bash
pytest booking_system/test_cases/test_login_flows.py booking_system/test_cases/test_login_validation.py --headed
```
