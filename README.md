# auth_api_service (Django Auth API)

This project provides an authentication API with:
- Register (with email verification)
- Login (JWT via Simple JWT)
- Token refresh
- Logout (token blacklist)
- Password reset (request + confirm)

## Run locally

1. Unzip the project and `cd` into the folder.
2. Create a virtualenv and activate it:
    python -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate    # Windows
3. Install dependencies:
    pip install -r requirements.txt
4. Make migrations and migrate:
    python manage.py makemigrations
    python manage.py migrate
5. Run the server:
    python manage.py runserver

Emails are printed to the console by default (console email backend).

## Deploying to a cloud host (high-level)

Recommended hosts: Render, Heroku, Railway.
- Use a managed Postgres database in production.
- Set environment variables for SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, and any email API keys.
- Run `python manage.py collectstatic --no-input` during build/deploy so WhiteNoise can serve static files.

See platform docs for exact steps (we include links in the project's README in the zip).
