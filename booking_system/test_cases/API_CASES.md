# EventHub API test cases (H / E / X / P / S)

Source skill: `01_测试用例生成.md`  
Base URL: `https://api.eventhub.rahulshettyacademy.com`  
Machine-readable: [cases_draft.json](./cases_draft.json)

Credentials: use `.env` (`COURSE_EMAIL` / `COURSE_PASSWORD`) — never commit secrets.

---

## Coverage map

| Layer | Meaning | Case IDs |
|-------|---------|----------|
| **H** | Happy path | `EH-API-LOGIN-H-001`, `EH-API-EVENTS-H-002` |
| **E** | Contract / boundary | `EH-API-LOGIN-E-001` … `E-003` |
| **X** | Auth / business reject | `EH-API-LOGIN-X-001`, `EH-API-EVENTS-X-001` … `X-002` |
| **P** | Latency sanity | `EH-API-LOGIN-P-001` |
| **S** | Security sanity | `EH-API-EVENTS-S-001` |

**Floor for public APIs:** at least H + X (done for login + events).

---

## Case table

| ID | Layer | Interface | Preconditions | Request body | Expect | Teardown |
|----|-------|-----------|---------------|--------------|--------|----------|
| EH-API-LOGIN-H-001 | H | `POST /api/auth/login` | Valid account in `.env` | `{"email":"${COURSE_EMAIL}","password":"${COURSE_PASSWORD}"}` | **200**; token present | none |
| EH-API-EVENTS-H-002 | H | `GET /api/events` | After H-001; `Bearer ${token}` | — | **200**; events list/payload | none |
| EH-API-LOGIN-E-001 | E | `POST /api/auth/login` | — | `{"email":"invalid@example.com","password":"123"}` | **400**; password min-length validation | none |
| EH-API-LOGIN-E-002 | E | `POST /api/auth/login` | — | `{}` | **400**; missing fields | none |
| EH-API-LOGIN-E-003 | E | `POST /api/auth/login` | — | `{"email":"not-an-email","password":"abcdef"}` | **400**; email format (confirm msg) | none |
| EH-API-LOGIN-X-001 | X | `POST /api/auth/login` | — | `{"email":"invalid@example.com","password":"WrongPass1"}` | **401/400/403**; no token | none |
| EH-API-EVENTS-X-001 | X | `GET /api/events` | No auth | — | **401**; Unauthorized | none |
| EH-API-EVENTS-X-002 | X | `GET /api/events` | Garbage Bearer | — | **401** | none |
| EH-API-LOGIN-P-001 | P | `POST /api/auth/login` | Valid `.env` | same as H-001 | **200**; `< 3000ms` | none |
| EH-API-EVENTS-S-001 | S | `GET /api/events` | Anonymous | — | **401** | none |

---

## Scenario (ordered)

| ID | Steps | Notes |
|----|-------|-------|
| EH-API-SCEN-LOGIN-EVENTS-001 | 1) LOGIN-H-001 → capture `token` 2) EVENTS-H-002 with Bearer | Use `scenarios` when scripting (see `02_测试脚本生成.md` §6) |

---

## Self-check (from skill §4)

- [ ] Lock exact status for `LOGIN-X-001` after one real run  
- [ ] Confirm token JSON path before `extract_vars`  
- [ ] Avoid asserts that only check “any 200” on H cases — require token / events shape  
- [ ] E-layer cases marked `review_required` until messages match prod  

---

## Open questions

1. Official Swagger/OpenAPI URL?  
2. Booking APIs (`POST /api/bookings` …) schema?  
3. Exact login success JSON field for token?

---

## Next step

Per skill §5 → hand reviewed cases to **`02_测试脚本生成.md`** (pytest / api_lib spec).  
In this repo you can also ask: “generate API pytest scripts from `cases_draft.json`”.
