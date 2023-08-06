# Authentication
A django user authentication and login application.
Demo Website: https://django-user-login.herokuapp.com/

### 1.  To install and use the package, use:
        
        pip install django-user-login

Instructions

### 2.	Add "authentication" to your INSTALLED_APPS setting like this:

        INSTALLED_APPS = [
            ...
            'authentication',
        ]

### 3.	The App requires [Django Sessions](https://docs.djangoproject.com/en/4.0/topics/http/sessions/#enabling-sessions)

### 4.	Include the authentication URLconf in your project urls.py like this:

		path('authentication/', include('authentication.urls')),

### 5.	Run `python manage.py migrate` to create the User models (you'll need the Admin app enabled).

### 6.  In your settings.py file include the following:

        SITE_TITLE = 'your site title'
        LOGIN_URL = '/authentication/'
        EMAIL_HOST = 'email-host'
        EMAIL_PORT = email-port
        EMAIL_HOST_USER = 'email-address'
        EMAIL_HOST_PASSWORD = 'email-password'
        EMAIL_USE_TLS = True
        FAVICON_URL = '/path/to/favicon.ico'

### 7 General layout of the starter template / [base template](https://docs.djangoproject.com/en/4.0/ref/templates/language/#template-inheritance-1)

        <!doctype html>
        <html lang="en">
            <head>
                ....
                ....

                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <!-- Required Authentication CSS -->
                <link rel="stylesheet" href="{% static 'authentication/css/layout.css' %}">

                ....
                ....
            </head>
            <body>
                ....
                ....

                <!-- Required Authentication Modals -->
                {% include 'authentication/auth_modals.html' %}

                <!-- Required Authentication JavaScript -->
                <script src="{% static 'authentication/js/login.js' %}"></script>
            </body>
        </html>

### 8.  For login and logout functionality, use - 
- #### To Login, use anyone of these

            - <a href="{% url 'authentication:login' %}">Login</a>
		    - <a href='/authentication/'>Login</a>
            - <button class="..." type="..." role="..." data-bs-toggle="modal" data-bs-target="#loginModal">Login</button>

- #### To Logout, use anyone of these

            - <a href="{% url 'authentication:logout' %}">Logout</a>
		    - <a href="/authentication/logout/">Logout</a>
            - <a href="" onclick="logout(event);">Logout</a>

- #### To visit My Account page and edit profile credentials, use any one of these -

            - <a href="{% url 'authentication:account' username=request.user.username %}">Account</a>
            - <a href="/authentication/<username>/">Account</a>

### 9. This app uses Bootstrap, Bootstrap Icons, JQuery and Handlebars. These file can be accessed at -

            <link href="{% static 'authentication/assets/node_modules/bootstrap/dist/css/bootstrap.css' %}" rel="stylesheet">
            <link href="{% static 'authentication/assets/node_modules/bootstrap-icons/font/bootstrap-icons.css' %}" rel="stylesheet">

            <script src="{% static 'authentication/assets/node_modules/bootstrap/dist/js/bootstrap.bundle.js' %}"></script>
            <script src="{% static 'authentication/assets/node_modules/jquery/dist/jquery.js' %}"></script>
            <script src="{% static 'authentication/assets/node_modules/handlebars/dist/handlebars.js' %}"></script>


