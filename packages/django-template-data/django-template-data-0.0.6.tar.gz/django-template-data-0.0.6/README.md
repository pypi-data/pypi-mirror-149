# Django Template Data

### Why?
You are working on a Django project and you want a way to update some strings 
or blocks without using a bare CMS or a WYSIWYG. Then this small module is for
 you. It does what you expect, load datas from database and send them via
 the context to the templates.

### Installation
    $ pip install django-template-data
    
### Usage
Add 'template_data' in INSTALLED_APPS  
```python
INSTALLED_APPS = [
    ...,
    'template_data',
    ...,
]
```
Then add `load_data()` to templates context processors
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                ...,
                'template_data.processors.load_data',
            ],
        },
    },
]
```
Finally migrate

    $ python manage.py migrate
    
### Tutorial
Let say you want a dynamic title, loaded from the database. First create a base
 template like this:
```html
{% load i18n %}
<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="shortcut icon" href="/static/front/img/favicon.png" type="image/x-icon">
    {% block full_title %}<title>{% block title %}{{ title }}{% endblock %} - Sitename</title>{% endblock %}

...
```
Go to your Django admin to manage TemplateData model. Create two rows, with these
values:  
key = "title", page = "index", value = "Home"  
key = "title", page = "signin", value = "Login in your account"  
As you can imagine the title of the index page will be "Home - Sitename" and
 for the signin page will be "Login in your account - Sitename"
 
You surely noticed how we appended "- Sitename" to the title in the template.
 We can do the same by using the inheriting feature.  
First we define this template:
```html
{% load i18n %}
<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="shortcut icon" href="/static/front/img/favicon.png" type="image/x-icon">
    <title>{% block title %}{{ title }}{% endblock %}</title>

...
```
Then create three rows of TemplateData with these values:  
key = "title", page = "global", value = "Sitename"  
key = "title", page = "index", inheriting_page = "global", value = "Home - {{ super }}"  
key = "title", page = "signin", inheriting_page = "global", value = "Login in your account - {{ super }}"  
You will have the same result.

### Contributing
Contributions are welcome. It is FOSS!

### License
Feel free to use it as you want.
