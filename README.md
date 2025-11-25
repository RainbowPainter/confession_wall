# Confession_Wall
​	This is a final assignment for learning Django and implementing a campus confession wall using the Django framework.



### What are its characteristics

​	This is a very simple little project that allows you to quickly get started with the basics of Django. Within the project, the confession wall has three user roles: guests, regular users, and administrators (including super administrators). Guests can browse the content on the confession wall; to like or comment, they need to register as a user. Administrators can review and manage the content and comments, and manage the community content. Super administrators can also appoint other confession wall users as administrators. Regular administrators, except for not being able to appoint new administrators, enjoy the same privileges as super administrators.



### Directory Structure

```
confession_wall/                   # Project root directory
├── media/                         # Media File Directory
│   └── confessions/               # User-uploaded confession images
├── static/                        # Static file directory
│   ├── css/                       # CSS style files
│   ├── js/                        # JavaScript directory
│   └── images/                    # still images
├── templates/                     # Template file directory
│   ├── base.html                  # Basic Template
│   └── confession/                # Confession Application Template
│       ├── home.html              # Homepage/Square
│       ├── hot.html               # Popularity Ranking Page
│       ├── my_confessions.html    # My confession page
│       ├── create_confession.html # Post a confession page
│       ├── login.html             # Login page
│       ├── register.html          # Registration page
│       └── admin_confessions.html # Management Page
├── confession_wall/               # Django Project Configuration
│   ├── __init__.py
│   ├── settings.py                # Project Setup
│   ├── urls.py                    # Project URL routing
│   └── wsgi.py
├── confession/                    # Main application
│   ├── migrations/                # Database migration files
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                   # Administrator backend configuration
│   ├── apps.py                    # Application Configuration
│   ├── forms.py                   # Form definition
│   ├── models.py                  # Data Model
│   ├── signals.py                 # signal processor
│   ├── urls.py                    # Application URL routing
│   └── views.py                   # View functions
├── db.sqlite3                     # SQLite database file
├── manage.py                      # Django management script
├── requirements.txt               # Project Dependencies
└── reset_db.py                    # Database reset script
└── clean_project.py			   # Project reset script
```



### How to run this project

​	After opening the project in the compiler, you can enter the project through the terminal. First, you can perform database and table creation and superuser creation operations using the following commands. Note that the superuser's username and password are also the same as the project's backend administrator's username and password;

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

​	After that, you can execute the command `python manage.py runserver`, and follow the prompts to access port 8000 on your local machine (e.g., 127.0.0.1:8000) to see the project running. You can then access the administrator page by visiting `127.0.0.1:8000/admin`.

​	Of course, if you are already proficient enough, you can modify and run this project according to your own ideas.
