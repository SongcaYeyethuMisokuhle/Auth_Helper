<<<<<<< HEAD
# auth_api_service (Django Auth API)

This project provides an authentication API with:
- Register (with email verification)
- Login (JWT via Simple JWT)
- Token refresh
- Logout (token blacklist)
- Password reset (request + confirm)

## Run locally

1. Clone the repository (Take the following steps):
    Navigate to the folder where you want the project to live. For example: cd C:\Users\Admin\Desktop
    Run git clone: git clone https://github.com/SongcaYeyethuMisokuhle/Auth_Helper.git 
    Enter the project folder cd repo-name

2. Create a virtualenv and activate it:
    python -m venv venv
    venv\Scripts\activate
    If you see an error related to the virtual environment, please remove the one currently on the project and create a new one:
    Remove-Item -Recurse -Force venv (This will delete the current virtual env giving issues, create a new virtualenv and activate it)

3. Install dependencies:
    pip install -r requirements.txt

4. Make migrations and migrate:
    python manage.py makemigrations
    python manage.py migrate

5. Run the server:
    python manage.py runserver

Emails are printed to the console by default (console email backend).