# Loan Account Book Keeping
This Repo contains a software used by a firm to track loans given out to clients, As well as a book keeping software for the loan firm.

To begin use, clone the repo onto your device then change the 'Database Settings' in 'settings.py' to your own PostgreSQL database, 
Input your own secret key in [settings.py](../efeurban/efeurban/settings.py)
After code has been cloned and settings.py has been set up,

run `python manage.py makemigrations` and `python manage.py migrate`

When all this is done, activate your virtual environment if necessary, 
then run `pip install -r requirements.txt` to install all dependencies, and finally,
run `python manage.py runserver` to see the app in action.
