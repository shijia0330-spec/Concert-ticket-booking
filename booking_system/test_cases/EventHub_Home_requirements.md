# EventHub — Home (observed UI scope)

Product: EventHub  
URL: https://eventhub.rahulshettyacademy.com/

## Access
- Unauthenticated visit to `/` redirects to `/login`.
- After successful login, user lands on (or can open) `/` as the authenticated home.

## Authenticated home
- Hero: “Discover & Book Amazing Events” (or equivalent) is visible.
- Primary nav includes: Home (`/`), Events (`/events`), My Bookings (`/bookings`), API Docs (external Swagger), Admin (entry present for this account — role rules TBD).
- User email and **Logout** are visible when authenticated.
- **Featured Events** section lists event cards with title, date, location, price, seats cue, and **Book Now** linking to `/events/{id}`.
- CTAs: Browse Events / View all / Explore All Events → `/events`; My Bookings → `/bookings`.
- Footer may include academy/marketing links and Manage Events (`/admin/events`).

## Out of scope for this document
- Login field validation (see `EventHub_Login_*`)
- Full booking payment checkout after Book Now
- Admin CRUD for events
- Register flow
