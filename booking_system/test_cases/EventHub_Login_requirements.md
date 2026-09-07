# EventHub — Login (observed UI scope)

Product: EventHub (https://eventhub.rahulshettyacademy.com/login)

## Login page
- User can open the login page and see Email, Password, and Sign In.
- User signs in with email and password.
- On success, user reaches the home experience and can Logout.
- Invalid credentials must not grant access (user remains unauthenticated).
- Page offers a Register entry (behavior outside this module scope until clarified).

## Observed fields
- Email (required, email format expected)
- Password (required; API layer observed min length 6 — confirm for UI)
- Sign In button

## Out of scope for this document
- Browse events, book tickets, My Bookings, Admin (separate modules)
