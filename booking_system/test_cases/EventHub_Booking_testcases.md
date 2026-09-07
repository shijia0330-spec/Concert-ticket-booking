# EventHub Booking test cases

## Document info
- Based on requirements: `booking_system/test_cases/EventHub_Booking_requirements.md` + user steps (Dilli Diwali Mela × 2)
- Generator version: rules 1.2.0 (skills V3 · testcase-generator, English)
- RAG retrieval: skipped for this focused user story / `RAG: not run`
- Scope: Book **Dilli Diwali Mela**, qty **2**, compulsory fields, confirm, verify under **My Bookings**
- Structure: 3 levels (H2 → H3 → H4)
- Open questions total: 2

## Knowledge-base retrieval summary

RAG: not run (single user-specified flow).

## Requirements traceability

| Requirement section | Case IDs | Notes |
|---------------------|----------|-------|
| Book Dilli Diwali Mela qty 2 + compulsory fields + Confirm | F-01 | User steps |
| Booking Confirmed shown | F-01 | Observed UI |
| My Bookings shows transaction | F-01, L-01 | User assert |
| Compulsory field empties | V-01 | Matrix A |
| Qty 2 price line | V-02 | |
| Qty 2 total = $600 | V-03 | User assert |
| Qty boundaries max | T-02 | max 8 observed |

## Core-flow tests

### Flow 1: Book Dilli Diwali Mela (2 tickets) → see booking under My Bookings

```text
Login
  → Open Dilli Diwali Mela (/events/3)
  → Set qty to 2
  → Fill Full Name*, Email*, Phone Number*
  → Confirm Booking
  → See Booking Confirmed (ref, 2 tickets, total)
  → My Bookings lists that transaction
```

#### F-01 Book Dilli Diwali Mela qty 2 and see transaction under My Bookings <!-- P0 -->
- After login, open **Dilli Diwali Mela**; set tickets to **2** (use **+** from default 1); fill compulsory **Full Name**, **Email**, and **Phone Number** with valid values; click **Confirm Booking**
- **Booking Confirmed!** is visible; confirmation shows **Tickets** = **2** and a **Booking Ref** value
- Open **My Bookings** (`/bookings`); a row/card for **Dilli Diwali Mela** is visible with **2 tickets** (and the same Booking Ref when shown)

## Detailed feature tests

### Validation (booking form)

#### V-01 Confirm Booking with empty compulsory fields does not succeed <!-- P1 -->
- On Dilli Diwali Mela book form, leave Full Name / Email / Phone empty (or clear them), click **Confirm Booking**; **Booking Confirmed!** does not appear (browser or UI validation blocks)

#### V-02 Quantity shows 2 tickets in price line before confirm <!-- P2 -->
- On book form, increase qty to 2; UI shows a line equivalent to `$300 × 2 tickets` (or current unit price × 2) before confirm

#### V-03 Quantity 2 shows total price $600 <!-- P1 -->
- On Dilli Diwali Mela book form, set tickets to **2**; **Total** displays **$600** (unit $300 × 2)

### My Bookings list

#### L-01 My Bookings lists confirmed Dilli Diwali Mela booking after F-01 <!-- P0 -->
- After a successful F-01 booking, `/bookings` shows status **confirmed** (or equivalent) for that Dilli Diwali Mela entry with **2 tickets**

## Case review table

| ID | Name | Priority | Type | Tags |
|----|------|----------|------|------|
| F-01 | EventHub > Event detail > Book Dilli Diwali Mela ×2 → Confirmed → My Bookings | P0 | smoke_sanity | booking |
| V-01 | EventHub > Event detail > Empty compulsory fields block confirm | P1 | boundary | validation |
| V-02 | EventHub > Event detail > Qty 2 updates price line | P2 | functional | qty |
| V-03 | EventHub > Event detail > Qty 2 total equals $600 | P1 | functional | price |
| L-01 | EventHub > My Bookings > Confirmed transaction for Dilli Diwali Mela ×2 | P0 | functional | bookings |

## Universal coverage matrix self-check

| Dimension | Triggered? | Covered / to clarify | Notes |
|-----------|------------|----------------------|-------|
| A Input & validation | Yes | V-01; F-01 fills required | Name/Email/Phone required |
| B List & query | Yes | L-01 | My Bookings list |
| C Auth & roles | Yes | F-01 precondition login | Must be logged in |
| D Resource by ID | Yes | F-01 `/events/3` | Event id 3 |
| E Time & state | Partial | L-01 confirmed | Cancel not in scope |
| F Repeat & consistency | No | T-02 | Double confirm TBD |
| G Errors & usability | Yes | V-01 | |
| H API contract | No | — | UI flow |
| I NFR | No | — | |

## Open questions

| # | Question | Related IDs |
|---|----------|-------------|
| T-02 | Double-click Confirm Booking — one booking or two? | F-01 |

---

**User assert (owned):** After confirm, **My Bookings** contains the transaction for **Dilli Diwali Mela** with **2** tickets. Qty **2** total = **$600**.

**Automation (Playwright):** `test_booking_flows.py` (F-01 includes L-01; V-01, V-02, V-03).

```bash
pytest booking_system/test_cases/test_booking_flows.py --headed
```
