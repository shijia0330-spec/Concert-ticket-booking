# EventHub — Book Event (observed UI scope)

Product: EventHub  
Primary event for this pack: **Dilli Diwali Mela** (`/events/3`)

## Happy path (user-owned)
1. Login with a valid account.
2. Open **Dilli Diwali Mela**.
3. Set ticket quantity to **2**.
4. Fill compulsory fields: **Full Name***, **Email***, **Phone Number***.
5. Click **Confirm Booking**.
6. Open **My Bookings** and verify the transaction appears.

## Observed UI facts
- Event detail: `/events/3`
- Qty control: `−` / `+` (default 1, max 8)
- Required fields: Full Name, Email, Phone Number
- Success on same page: **Booking Confirmed!** with Booking Ref, Tickets, Total
- My Bookings: `/bookings` lists ref, event name, ticket count, total, status `confirmed`

## Out of scope
- Cancel booking / Clear all bookings (unless added later)
- Payment gateway (none observed — confirm is immediate)
- Other events (can parameterize later)
