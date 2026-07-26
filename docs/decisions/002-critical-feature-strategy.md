# ADR 002: Concurrent Booking Integrity Strategy

## Status

Accepted.

## Context

Two customers can view the same available slot and submit concurrently. If each request checks availability and then inserts independently, both checks can pass before either insert commits. Application checks or disabled browser buttons cannot prevent requests from different clients from racing.

The project requires PostgreSQL to be the source of truth and requires concurrency tests proving that duplicate active bookings cannot be created.

## Considered Alternatives

### Frontend Submission Suppression Only

Disable the submit button after one click. This improves usability but cannot coordinate browsers, devices, direct clients, or retries and therefore cannot protect data integrity.

### Application Availability Check Only

Query for an existing booking before inserting. This has a check-then-insert race and is insufficient.

### Row Lock Without A Unique Constraint

Lock the slot with `SELECT FOR UPDATE` and recheck occupancy. This coordinates correct application paths but a missing lock or direct write could still create duplicates.

### Serializable Transactions

Run all booking transactions at PostgreSQL `SERIALIZABLE` isolation and retry serialization failures. This can work but introduces broad retry complexity that is unnecessary for a single-slot invariant.

### Row Lock Plus Partial Unique Index

Use a short transaction and slot row lock for predictable coordination, with a PostgreSQL partial unique index as the final invariant.

## Decision

Use defense in depth:

1. Represent active occupancy as a booking with `status = 'confirmed'`.
2. Add a named PostgreSQL partial unique index on `booking(slot_id)` for confirmed rows.
3. Execute booking creation in one short transaction.
4. Lock the selected slot with `SELECT FOR UPDATE` before rechecking open, future, and occupancy state.
5. Create the booking and creation event in the same transaction.
6. Commit before returning confirmation.
7. Map the named uniqueness violation to `409 Conflict` with `slot_unavailable`.
8. Use a unique hashed idempotency identity and request fingerprint to recover successfully committed requests without creating duplicates.
9. Use the same slot-lock convention for administrator closure and target-slot rescheduling.

Conceptual database invariant:

```sql
CREATE UNIQUE INDEX uniq_confirmed_booking_per_slot
ON booking (slot_id)
WHERE status = 'confirmed';
```

Django's default PostgreSQL `READ COMMITTED` isolation is sufficient with these locks and constraints.

## Rationale

- The unique index is a non-bypassable database guarantee.
- Row locking makes normal conflicts predictable and coordinates booking with administration.
- A partial index allows a cancelled historical booking and one later confirmed booking to share a slot.
- Short `READ COMMITTED` transactions avoid unnecessary serializable retries.
- Idempotency distinguishes a duplicate delivery of one intent from competing customers.
- Current state and history cannot diverge because they commit together.

## Consequences

- PostgreSQL is mandatory for integration and concurrency tests.
- Constraint names become part of internal error mapping and must remain stable through migrations.
- Every mutation touching a booking or slot must follow a documented lock order.
- A losing customer receives a conflict and must select a new slot; the frontend cannot silently retry the same slot.
- A temporary or unknown network outcome may be retried only with the same idempotency identity and request data.
- Availability shown in the browser remains advisory, not a reservation.

## Known Risks

- Inconsistent lock order could create deadlocks.
- Catching all integrity errors as slot conflicts could hide unrelated defects; mapping must inspect the named constraint.
- Long transaction work could increase lock waits; rendering and external work must remain outside transactions.
- Idempotency-key reuse with changed data must be rejected explicitly.
- Concurrency tests can become flaky if they use timing sleeps rather than independent connections and barriers.
- A browser can suppress local double clicks but cannot enforce global uniqueness, commit atomicity, request ordering, or exactly-once response delivery.
