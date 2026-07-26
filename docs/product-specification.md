# Product Specification

## Status

Approved planning baseline. Items explicitly marked `TBD` remain unresolved and must not be silently inferred during implementation.

## Project Purpose

Build a small web application for a fictional consulting service. Customers can discover available appointment slots, book an appointment, and later cancel or reschedule it. One administrator manages availability and reviews booking history.

The primary integrity requirement is that a slot can never have more than one active booking, including when requests arrive concurrently. PostgreSQL must enforce that invariant.

## Target Users And Roles

### Customer

A customer does not create an account. A customer can:

- View future appointment availability.
- Book a slot using contact information.
- Receive an on-screen confirmation and private management access.
- View one authorized booking and its event history.
- Cancel or reschedule an authorized future booking.

### Administrator

The system has one authenticated administrator. The administrator can:

- Create, close, and reopen appointment slots.
- Distinguish open, closed, booked, cancelled, and past appointments.
- Review current and historical bookings and their events.

The administrator cannot create complex roles or manage multiple tenants.

## Main User Journeys

### View Availability And Book

1. The customer opens the availability page.
2. The system shows future, open, unbooked slots with date, time, and timezone.
3. The customer selects a slot and enters contact information.
4. The system validates the request and attempts to create the booking atomically.
5. On success, the customer sees a booking reference, confirmed appointment details, and private management access.
6. If another request won the slot, the customer keeps their contact input and selects from refreshed availability.

### Cancel A Booking

1. The customer uses private management access to open the booking.
2. The system shows the current status and appointment details.
3. The customer confirms cancellation.
4. The system records the cancellation without deleting booking history.
5. The slot becomes available again if it remains open and in the future.

### Reschedule A Booking

1. The customer opens an authorized, confirmed future booking.
2. The system shows alternative available slots.
3. The customer selects and confirms a target slot.
4. The system atomically moves the booking and records the old and new times.
5. If the target is no longer available, the original booking remains unchanged.

### Manage Availability

1. The administrator authenticates.
2. The administrator reviews existing slot states.
3. The administrator creates a future slot or closes or reopens an existing slot.
4. The system rejects past, invalid, overlapping, or unsafe changes.
5. A slot with an active booking cannot be silently closed or removed.

### Review Booking History

1. The administrator opens booking history.
2. The system lists current and historical bookings in reverse chronological order.
3. The administrator filters or pages through records and opens booking details.
4. A customer can see only events belonging to the individually authorized booking.

## Functional Requirements

### Availability

- `FR-AV-01`: The system shall display future, open, unbooked appointment slots publicly.
- `FR-AV-02`: Each slot shall show its date, start time, end time, and explicit timezone.
- `FR-AV-03`: Public availability responses shall not expose customer information.
- `FR-AV-04`: The system shall derive occupancy from active bookings rather than relying on browser state.

### Booking Creation

- `FR-BK-01`: A customer shall be able to book an available slot using full name and email; phone is optional.
- `FR-BK-02`: The backend shall validate all input independently of frontend validation.
- `FR-BK-03`: A successful booking shall produce an on-screen confirmation with a reference, status, slot details, timezone, and private management access.
- `FR-BK-04`: A slot shall have at most one confirmed booking.
- `FR-BK-05`: The database, not only application checks, shall enforce booking uniqueness.
- `FR-BK-06`: Repeating a successfully committed request with the same idempotency identity shall not create another booking or creation event.
- `FR-BK-07`: Losing a concurrent race shall return a conflict and shall not create partial state.

### Customer Booking Access

- `FR-AC-01`: A customer shall manage a booking using an unguessable private credential rather than an account.
- `FR-AC-02`: A valid credential shall authorize only its associated booking.
- `FR-AC-03`: Invalid management access shall not reveal whether a booking exists.

### Cancellation

- `FR-CA-01`: An authorized customer shall be able to cancel a confirmed future booking.
- `FR-CA-02`: Cancellation shall preserve the booking and append one cancellation event.
- `FR-CA-03`: Repeated cancellation shall not create duplicate events or corrupt state.
- `FR-CA-04`: A cancelled slot shall become available only when the slot remains open and future.

### Rescheduling

- `FR-RS-01`: An authorized customer shall be able to move a confirmed future booking to another available slot.
- `FR-RS-02`: Rescheduling shall preserve booking identity and contact information.
- `FR-RS-03`: Rescheduling shall atomically secure the target and release the original slot.
- `FR-RS-04`: A failed reschedule shall leave the original booking unchanged.
- `FR-RS-05`: History shall record the old slot, new slot, actor, and event time.

### Administration

- `FR-AD-01`: Administrator pages and mutations shall require server-side authentication and authorization.
- `FR-AD-02`: The administrator shall be able to create valid future non-overlapping slots.
- `FR-AD-03`: The administrator shall be able to close and reopen future unbooked slots.
- `FR-AD-04`: The system shall reject closure of a slot with a confirmed booking.
- `FR-AD-05`: Login errors shall not disclose whether the username or password was incorrect.

### History

- `FR-HI-01`: The system shall maintain an append-only history of creation, rescheduling, and cancellation events through normal application operations.
- `FR-HI-02`: The administrator shall be able to review paginated booking history and booking details.
- `FR-HI-03`: A customer shall be able to review events only for the authorized booking.

### Delivery And Traceability

- `FR-DL-01`: A clean checkout shall start locally with `docker compose up --build`.
- `FR-DL-02`: Database schema changes shall use migrations.
- `FR-DL-03`: GitHub Actions shall run formatting, linting, unit, integration, concurrency, and end-to-end checks.
- `FR-DL-04`: The project shall record prompts, failed attempts, human interventions, manual changes, post-completion defects, and architectural changes throughout planning and implementation.

## Non-Functional Requirements

### Integrity And Reliability

- Booking creation, cancellation, rescheduling, and conflicting slot administration shall use database transactions.
- PostgreSQL shall enforce one confirmed booking per slot through a named partial unique constraint or index.
- Booking state and its corresponding history event shall commit or roll back together.
- Server time shall determine whether an appointment is past.
- A conflict shall result in a deterministic user-visible response, not a generic success or partial record.

### Architecture And Maintainability

- Domain logic shall not depend directly on Django or HTTP handling.
- Database access shall remain in persistence repositories and query objects.
- Views and API routes shall not contain booking conflict logic.
- Modules shall expose explicit application-service and query boundaries.
- Dependencies shall be pinned and additions shall include a rationale.

### Security And Privacy

- No production, personal, or reusable credentials shall be committed. Clearly labelled development-only placeholders may be documented, but production configuration shall reject them.
- Administrator authorization shall be enforced server-side.
- Passwords shall use Django's supported password hashing.
- Customer management credentials and idempotency values shall not be stored or logged in plaintext.
- State-changing browser requests shall have CSRF protection.
- Session cookies shall be `HttpOnly`, use an appropriate `SameSite` policy, and be `Secure` in HTTPS environments.
- Input shall be validated and safely rendered.
- Logs shall exclude passwords, capability credentials, cookies, and unnecessary contact data.
- Login and credential-exchange endpoints shall have basic abuse protection.

### Usability And Accessibility

- Core workflows shall be usable from a 320-pixel viewport through standard desktop widths.
- Forms shall have programmatic labels, keyboard operation, visible focus, and associated errors.
- Status shall not be communicated by color alone.
- Core workflows target WCAG 2.1 AA.
- The UI shall not claim success before the associated database transaction commits.

### Performance

- Normal page and API operations should complete within two seconds under the approved small-application profile of up to 50 concurrent requests.
- Availability and history queries shall avoid unbounded result sets and N+1 query patterns.

### Quality And Operations

- `pytest` shall cover unit, integration, concurrency, and end-to-end behavior.
- Ruff shall enforce Python formatting and linting.
- The TypeScript build shall enforce formatting, linting, and type checks.
- Local setup shall be repeatable through Docker Compose.
- CI shall pass from a clean checkout.
- No critical finding may remain after independent code review.

## Business Rules

1. The application represents one consulting resource with capacity one.
2. A slot has explicit start and end timestamps and is either open or closed.
3. A slot is available only when it is open, future, and has no confirmed booking.
4. Publicly displaying a slot does not reserve it.
5. A customer may hold bookings for multiple different slots.
6. A slot may have at most one confirmed booking regardless of request concurrency.
7. Cancelled bookings remain in history and no longer occupy their slot.
8. A cancelled slot is bookable again only if it remains open and future.
9. Rescheduling changes the slot of the existing booking rather than creating a new booking identity.
10. A failed reschedule does not release or alter the original booking.
11. Customer cancellation and rescheduling are allowed until the appointment starts.
12. At or after the start time, customer cancellation and rescheduling are unavailable.
13. Rescheduling to the current slot is rejected as no change.
14. Slots for the single consulting resource may not overlap.
15. The administrator cannot silently close or remove a slot with a confirmed booking.
16. Booking and event records are not hard-deleted through normal interfaces.
17. Concurrent mutations affecting the same booking produce one valid committed transition; losing operations return a conflict or current state.

## Error, Loading, And Empty States

| Situation | Required behavior |
| --- | --- |
| Availability loading | Show progress without presenting an unconfirmed result as current availability. |
| No future slots | Explain that no appointments are available and provide refresh or later-return guidance. |
| Availability failure | Show a non-destructive error and retry action. |
| Invalid contact data | Show field-level errors and preserve valid input. |
| Slot claimed concurrently | Explain that the slot was just booked, preserve contact input, and refresh alternatives. |
| Duplicate successful submission | Return the existing booking and show one confirmation. |
| Unknown network outcome | State that the result is uncertain and offer a safe idempotent retry. |
| Invalid management access | Show one generic unavailable-or-invalid message. |
| Already cancelled | Display cancelled state and do not append another cancellation event. |
| Past booking | Display historical state and disable cancellation and rescheduling. |
| Reschedule conflict | Preserve the original booking and refresh alternatives. |
| No alternatives | Explain that no alternative slots are available while retaining the original booking. |
| Empty administrator history | Show `No bookings found`, not an empty table. |
| Administrator login failure | Show a generic credentials error. |
| Administrator session expiry | Require reauthentication and do not imply an uncommitted mutation succeeded. |
| Invalid or overlapping slot | Explain the conflict and preserve other valid form input. |
| Closing a booked slot | Reject the action and explain that an active booking exists. |
| Unexpected server failure | Show a safe generic message with retry or navigation options and no internal details. |

## Edge Cases

- Two or more customers submit the same slot concurrently.
- Identical requests with one idempotency key arrive concurrently.
- One idempotency key is reused with different request data.
- The booking commits but its HTTP response is lost.
- A customer double-clicks submit or retries after a timeout.
- Booking creation and administrator slot closure race.
- Cancellation and rescheduling race for one booking.
- Two reschedules target the same slot.
- A reschedule target becomes unavailable after alternatives were displayed.
- A slot starts while a management page remains open.
- A slot or display crosses midnight or a daylight-saving transition.
- Browser and service timezones differ.
- A credential is missing, malformed, invalid, or associated with another booking.
- Contact values contain whitespace, international characters, or excessive lengths.
- History requires pagination.
- An administrator session expires during a mutation.
- A network failure leaves the client uncertain whether a mutation committed.

## Explicit Non-Goals

- Real payment processing.
- Real email or SMS delivery.
- Customer accounts or password recovery.
- Multi-tenant organizations.
- Multiple consultants, rooms, or bookable resources.
- Multiple service types or pricing.
- Native mobile applications.
- External calendar integration.
- Complex roles and permissions.
- Waitlists.
- Recurring appointments or recurring availability rules.
- Automated reminders.
- Administrator-initiated booking cancellation in the initial scope.
- Production infrastructure provisioning or Kubernetes.
- Message brokers, asynchronous workflow infrastructure, or event sourcing.

## Testable Acceptance Criteria

### Availability

- Given open, closed, booked, and past slots, only future open unbooked slots are selectable.
- Every displayed slot includes date, start, end, and timezone.
- Public availability contains no customer contact data.
- No slots produces the defined empty state.

### Booking Creation

- Valid input for an available slot creates one confirmed booking and one creation event.
- Invalid input creates no booking.
- Two independent simultaneous requests for one slot produce exactly one success and one conflict.
- Direct concurrent database writes cannot create two confirmed bookings for one slot.
- Retrying a committed request with the same idempotency identity returns the same booking and creates no additional event.
- Confirmation is returned only after the transaction commits.

### Customer Access

- A valid credential grants access to exactly one booking.
- An invalid credential does not reveal whether a booking exists.
- Raw credentials do not appear in persisted booking data or captured logs.

### Cancellation

- Cancelling an authorized future confirmed booking changes its status and appends one event.
- Repeated cancellation does not append another event.
- The future open slot returns to public availability.
- Past or unauthorized bookings cannot be cancelled.

### Rescheduling

- A valid reschedule moves the existing booking, appends one event, and releases the original slot.
- Losing a target-slot race returns a conflict and leaves the original booking unchanged.
- Past, cancelled, unauthorized, and same-slot requests do not change the booking.

### Administration

- Anonymous and unauthorized users cannot access administrator pages or mutations.
- The administrator can create valid future non-overlapping slots and close or reopen unbooked slots.
- Invalid, past, overlapping, and booked-slot closure requests are rejected without partial changes.

### History

- The administrator can review paginated current and historical bookings and events.
- A customer sees only the individually authorized booking history.
- Creation, rescheduling, and cancellation event details are chronologically correct.

### Delivery

- `docker compose up --build` starts the application and PostgreSQL from a clean checkout.
- Migrations apply to an empty database.
- All required quality commands and CI jobs pass.
- The experiment record contains every required category.
- Independent review leaves no critical finding unresolved.

## Approved Assumptions

- The service has one bookable resource with capacity one.
- Availability uses explicit slots rather than recurrence rules.
- Customers do not create accounts.
- Full name and email are required; phone is optional.
- Confirmation is shown in the application because real delivery is out of scope.
- Customer access uses an unguessable capability credential and is scoped to one booking.
- Rescheduling preserves booking identity and contact details.
- Customer changes are allowed until the appointment starts.
- The administrator cannot cancel customer bookings in the initial scope.
- Database instants are stored in UTC and rendered in one configured service timezone.
- Booking history includes administrator-wide history and customer history for one authorized booking.
- Administrator history defaults to 50 records per page.
- The target is the latest two versions of major evergreen browsers.
- The default performance profile is a small service with up to 50 concurrent requests.

## Open-Decision Register

| Decision | Status | Milestone blocked | Notes |
| --- | --- | --- | --- |
| Service timezone identifier shown to users | `TBD` | M5 | Must be selected before user-visible slot formatting is finalized. |
| Standard appointment duration | `TBD` | M6 only if the availability UI derives an end time | Explicit start and end timestamps allow M0 through M5 and the persistence model to proceed. |
| Contact-data retention and anonymization period | `TBD` | M13 release with real customer data | Does not block development with synthetic data. |
| Public internet exposure | `TBD` | M13 release if public deployment is requested | M6 implements the approved single-administrator baseline. If public exposure is selected before M6, its stronger authentication requirements must be decided before M6 acceptance. |
| Recovery for lost customer management access | `TBD` | None for the approved initial behavior | M8 provides on-screen capability access only; M13 must document the limitation. |

No open product decision blocks M0 or M1.
