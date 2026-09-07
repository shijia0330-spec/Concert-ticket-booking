# EventHub Home test cases

## Document info
- Based on requirements: `booking_system/test_cases/EventHub_Home_requirements.md` (observed UI; URL https://eventhub.rahulshettyacademy.com/)
- Generator version: rules 1.2.0 (skills V3 · testcase-generator, English)
- RAG retrieval: hits present but **seckill samples — not adopted** (unrelated to EventHub Home)
- Scope: Home `/` — anonymous redirect + authenticated home browse/nav/featured events
- Structure: 3 levels (H2 → H3 → H4)
- Open questions total: 5

## Knowledge-base retrieval summary

RAG returned seckill/sample material — **not used**. Treat as no usable EventHub Home hits.

## Requirements traceability

| Requirement section | Case IDs | Notes |
|---------------------|----------|-------|
| Anon `/` → `/login` | F-01, P-01 | Observed redirect |
| Auth home hero + Logout | F-02, P-02 | After login |
| Nav: Home / Events / My Bookings / API Docs | L-01…L-04 | Authenticated |
| Featured Events cards + Book Now | L-05, L-06, D-01 | Titles observed |
| Browse / Explore All Events → `/events` | L-07 | CTA |
| My Bookings → `/bookings` | L-08 | Auth rules TBD (T-01) |
| Admin / Manage Events | T-02, T-03 | Role unclear |
| Login form details | — | See Login module |

## Core-flow tests

### Flow 1: Anonymous opens site root → login gate

```text
Open https://eventhub.rahulshettyacademy.com/
  → Redirected to /login
  → Sign In is available
```

#### F-01 Anonymous `/` redirects to login <!-- P0 -->
- Without a session, open `https://eventhub.rahulshettyacademy.com/`; final URL contains `/login` and the **Sign In** control is visible

### Flow 2: Authenticated user sees home with featured events

```text
Login with valid account
  → Land on /
  → Hero + Featured Events + Logout visible
```

#### F-02 After login, home shows hero, Featured Events, and Logout <!-- P0 -->
- Sign in with a valid account; URL is `https://eventhub.rahulshettyacademy.com/` (no `/login`); heading text for Discover & Book (or equivalent hero) is visible; **Featured Events** section is visible; **Logout** is visible

## Detailed feature tests

### Access / permission

#### P-01 Unauthenticated user cannot stay on home content <!-- P0 -->
- Open `/` anonymously; page does not show authenticated chrome (**Logout** absent) and user is on `/login`

#### P-02 Authenticated session shows user email and Logout on home <!-- P1 -->
- After valid login on home `/`, the signed-in email text is visible and **Logout** is visible

### Navigation & lists (authenticated)

#### L-01 Home nav link stays on or returns to `/` <!-- P1 -->
- From authenticated home, click nav **Home**; URL is `/` (or home) and Featured Events remain reachable

#### L-02 Events nav opens `/events` <!-- P1 -->
- From authenticated home, click nav **Events**; URL contains `/events`

#### L-03 My Bookings nav opens `/bookings` <!-- P1 -->
- From authenticated home, click nav **My Bookings**; URL contains `/bookings` (if redirected to login instead → record actual behavior; clarify T-01)

#### L-04 API Docs opens Swagger docs URL <!-- P2 -->
- From authenticated home, click **API Docs**; destination is `https://api.eventhub.rahulshettyacademy.com/api/docs` (new tab or same — confirm T-04)

#### L-05 Featured Events lists at least one event card <!-- P0 -->
- On authenticated home, **Featured Events** shows one or more event titles (e.g. observed: Dilli Diwali Mela / Hollywood Monsoon Night / World Tech Summit — exact set may change)

#### L-06 Each featured card exposes Book Now to `/events/{id}` <!-- P1 -->
- On a Featured Event card, **Book Now** is visible and its link path matches `/events/` + an id (e.g. `/events/1`)

#### L-07 Browse / Explore All Events goes to `/events` <!-- P1 -->
- Click **Browse Events →** or **Explore All Events** (or **View all →**); URL contains `/events`

#### L-08 My Bookings CTA from hero area goes to `/bookings` <!-- P2 -->
- Click hero/area **My Bookings** control; URL contains `/bookings`

### Detail entry from home

#### D-01 Clicking a featured event title opens that event detail <!-- P1 -->
- Click a featured event title link (e.g. **World Tech Summit**); URL matches `/events/{id}` for that card

### Pending / clarify

#### T-02 Admin nav visibility by role (to clarify) <!-- P3 -->
- （待澄清）When is **Admin** shown? Who can open `/admin/events`?

#### T-03 Manage Events footer link authorization (to clarify) <!-- P3 -->
- （待澄清）Does **Manage Events** require admin? Expected 403 vs hide link for normal users?

## Case review table

| ID | Name | Priority | Type | Tags |
|----|------|----------|------|------|
| F-01 | EventHub > Home > Anonymous `/` redirects to login | P0 | smoke_sanity | access |
| F-02 | EventHub > Home > Auth home hero + Featured + Logout | P0 | smoke_sanity | home |
| P-01 | EventHub > Home > Anon cannot see auth home chrome | P0 | security | access |
| P-02 | EventHub > Home > Email + Logout when authenticated | P1 | security | session |
| L-01 | EventHub > Home > Nav Home | P1 | functional | nav |
| L-02 | EventHub > Home > Nav Events → `/events` | P1 | functional | nav |
| L-03 | EventHub > Home > Nav My Bookings → `/bookings` | P1 | functional | nav |
| L-04 | EventHub > Home > API Docs → Swagger | P2 | functional | nav |
| L-05 | EventHub > Home > Featured Events has cards | P0 | functional | list |
| L-06 | EventHub > Home > Book Now → `/events/{id}` | P1 | functional | list |
| L-07 | EventHub > Home > Browse/Explore → `/events` | P1 | functional | cta |
| L-08 | EventHub > Home > My Bookings CTA → `/bookings` | P2 | functional | cta |
| D-01 | EventHub > Home > Event title → detail | P1 | functional | detail |
| T-02 | EventHub > Home > Admin visibility (to clarify) | P3 | pending_clarification | admin |
| T-03 | EventHub > Home > Manage Events auth (to clarify) | P3 | pending_clarification | admin |

## Universal coverage matrix self-check

| Dimension | Triggered? | Covered / to clarify | Notes |
|-----------|------------|----------------------|-------|
| A Input & validation | No | — | Home is browse/nav, not a form |
| B List & query | Yes | L-05, L-06, D-01 | Featured list |
| C Auth & roles | Yes | F-01, F-02, P-01, P-02; T-02/T-03 | Redirect + Admin TBD |
| D Resource by ID | Yes | L-06, D-01 | `/events/{id}` |
| E Time & state | Partial | T-05 | Seats/date display — copy may change |
| F Repeat & consistency | No | — | No submit on home |
| G Errors & usability | Yes | F-01 | Redirect instead of crash |
| H API contract | No | — | UI module |
| I NFR appendix | No | — | Not requested |

## Open questions

| # | Question | Related IDs |
|---|----------|-------------|
| T-01 | Must user be logged in for `/bookings`, or is empty/login gate shown? | L-03, L-08 |
| T-02 | Admin nav: which roles see it? | T-02 |
| T-03 | Manage Events: hide vs 403 for non-admin? | T-03 |
| T-04 | API Docs: same tab or new tab? | L-04 |
| T-05 | Are featured event titles/seat counts stable for automation asserts, or assert “≥1 card” only? | L-05 |

---

**Automation (Playwright):** `test_home_access.py` (F/P) · `test_home_nav.py` (L/D). **T-02 / T-03** not automated.

```bash
pytest booking_system/test_cases/test_home_access.py booking_system/test_cases/test_home_nav.py --headed
```
