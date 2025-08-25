
# Smart Parking Finder — POC (20 Endpoints)

FastAPI + MongoDB (Motor) implementation of the 20 endpoints you specified. No `Depends` used for auth — every protected route validates `Authorization: Bearer <token>` manually.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# (optional) edit .env for Mongo, JWT secret, SMTP
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

## Seed Initial Data

Creates: 5 parking lots × 6 slots each (alternating car/bike) and one user (surendra / mypassword123).

```bash
python seed.py
```

## Endpoints (User + Parking + Booking + Notifications)

- POST `/user/register`
- POST `/user/login`
- GET `/user/profile` (auth)
- PUT `/user/profile/update` (auth)
- DELETE `/user/profile/delete` (auth)
- PUT `/user/password/change` (auth)
- POST `/user/password/forgot`
- POST `/user/password/reset`
- POST `/user/logout` (auth validation only)

- GET `/parkings`
- GET `/parkings/{parking_id}`
- GET `/parkings/{parking_id}/slots`
- GET `/parkings/{parking_id}/slots/available`

- POST `/bookings` (auth)
- GET `/bookings` (auth)
- GET `/bookings/{booking_id}` (auth)
- PUT `/bookings/{booking_id}` (auth)
- DELETE `/bookings/{booking_id}` (auth)
- POST `/bookings/{booking_id}/release` (auth)

- GET `/notifications` (auth)

## Notes
- Passwords hashed with bcrypt.
- JWT via PyJWT. Stateless logout (client discards token).
- Reset-token email uses SMTP stub; starts even if SMTP is unavailable.
