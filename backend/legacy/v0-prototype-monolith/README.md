# CareerOS Working Model

This is a runnable end-to-end implementation of the CareerOS working model with:

- Auth (register/login)
- Career profile save/load
- Resume generation from profile data
- ATS scan scoring API
- Job match ranking API
- Dashboard metrics API

## Run

1. Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start server:

```powershell
uvicorn app.main:app --reload --port 8000
```

3. Open app:

- http://127.0.0.1:8000

## Notes

- Database: local SQLite file `careeros.db`
- This is a functional foundation for MVP, not final production hardening.
- Password hashing is SHA-256 for prototype speed; replace with `bcrypt` for production.
