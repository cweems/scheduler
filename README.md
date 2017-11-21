# Scheduler
A simple demo scheduling application written in approximately 5 hours with Python/Django. Since many of my Github contributions were part of larger projects, I wanted an example of what I can build solo without too much time.

[A live instance of the app is running on heroku.](https://scheduler-11-2017.herokuapp.com/) Note that Heroku's free tier takes 5-10 seconds to spin up.

### Specifications:
* Team members must be able to add meetings with a start and end time.
* New meetings can't overlap with one of a team member's own pre-existing meetings.
* Team members must be able to see what times everyone is free.

### Implementation Notes:

The most complex/interesting algorithms can be found in the [model validations](https://github.com/cweems/scheduler/blob/master/main/models.py#L17) (checking that a user's new meeting doesn't overlap with an existing one) and in the [free_time_finder utility](https://github.com/cweems/scheduler/blob/master/main/utils.py#L5) (finding blocks of free time between all users).

## Setup:
Create a virtual environment: `python3 -m venv env`

Source the virtual environment: `source env/bin/activate`

Install requirements: `pip install -r requirements.txt`

Create the PostgreSQL database:
```
psql
CREATE DATABASE scheduler;
\q
```

Make and run migrations: `python manage.py makemigrations && python manage.py migrate`

Start server: `python manage.py runserver`

