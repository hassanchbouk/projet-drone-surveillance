# Django Starter

This starter template for Django projects streamlines the setup of Django projects within a GitHub Codespaces environment.

## Get Started

### Create a codespace

Once the repository created from this template, click on *Code* / *Codespaces* / *Create codespace on main* .

Then, a tab opens with the *Visual Studio Code* environment.

If it closes, you can find it in the codespaces list in *Code* / *Codespaces* and click on it to resume your session. 

### Initialize the virtual environment

In VS Code, use the command palette to launch *Python: Create environment*, then choose venv and the latest version of python.

Activate it with : `source .venv/bin/activate`, so the prompt changes and shows `(.venv)`.

Type `pip install Django` in the terminal to install the Django framework. Then `pip freeze > requirements.txt` to update dependency requirements. 

### Save changes

Regularly commit your changes (once checked) to your github repository, from VS Code :
- click on the left icon *Source control* (third from the top),
- enter a *Message* to keep track of changes made,
- click on *Commit*,
- confirm the unindexed changes prompt,
- click on *Synchronize* to send changes from your local codespace to the github repository.  

### Django project creation

Create a Django project with `django-admin startproject yourproject .` where `yourproject` is your project name without space.

A Django project is made of applications which act as modules for grouping related features. Create first (maybe single) with `django-admin startapp yourapp .` where `yourapp` is the name of your first module.

Activate the app in `settings.py` by adding `"yourapp"` it in the `INSTALLED_APPS` list.

### Database and backend 

For user management and soon for your app, create the database with the `python manage.py migrate` command.

Create your first administrator to access the admin panel by :
- typing `python manage.py createsuperuser --username admin --email youremail@company.example`
- entering a password and a confirmation (min. length 8 characters). 

### Launch server

Add the line `CSRF_TRUSTED_ORIGINS = ['https://localhost:8000']` at the end of `settings.py`.

Use this command : `python manage.py runserver` .

Add `/admin` to the url of the opening tab to go to the login page and authenticate as admin thanks to the newly created user.

## Entities

Add application entities in `yourapp/models.py` accoding [this documentation](https://docs.djangoproject.com/en/6.0/topics/db/models/).

Add models to the admin pages by adding in `yourapp/admin.py` :

```py
from .models import MyModel

admin.site.register(MyModel)
```

Create the migration to adapt the database structure with `python manage.py makemigrations`.

Apply them `python manage.py migrate` to the database structure.

Restart the server to ensure your changes are loaded.
