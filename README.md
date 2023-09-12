
# PulsePoint
A comprehensive Digital Sanctuary

PulsePoint is a Django-based web application designed to track users' moods and connect with a community of like-minded individuals. With an intuitive interface and user-friendly navigation, PulsePoint offers tools like mood tracking and a community platform for users to share and connect.

## Prerequisites
Python 3.11

Django (version here is 4.2.4)

Virtual environment (optional, but recommended)

## Getting Started
### Clone the Repository:

```
git clone https://github.com/MagnumNight/PulsePoint.git

cd PulsePoint
```
### Set Up a Virtual Environment (Recommended):
```
python -m venv venv

source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies:

#### Navigate to the project directory (PulsePoint) and install the required packages:
```
pip install -r requirements.txt
```

### Secure your application:

#### In your terminal, type in:
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
``` 
This will print out a new secret key that you will use in the next step.

#### In the root folder, create a file named .env and fill it with YOUR info:
```
DJANGO_SECRET_KEY=whatever your secret key is
EMAIL_HOST_PASSWORD=whatever your host password is
DEBUG=True (if you want debugging on)
```
Debug should be off for production

#### In the root folder, create a file named .gitignore and fill it out with this:
```
*.pyc
__pycache__/
db.sqlite3
.env
```

### Set Up the Database:

#### Make & Apply migrations to initialize your database schema:
```
python manage.py makemigrations
python manage.py migrate
```
### Run the Development Server:
```
python manage.py runserver
```
You can now navigate to http://127.0.0.1:8000/ in your browser to see the PulsePoint application.

### Features
#### Mood Tracker: 
Allows users to record their moods over time and view trends.

#### Community: 
Connect, share, and discuss with a community of users.

#### Resources:
Allows users to get the help they need.

### License:
This project is licensed under the Apache License - please look at the LICENSE.txt file for details.
