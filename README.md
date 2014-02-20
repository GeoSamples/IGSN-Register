# IGSN-Register
## Mobile application to register IGSN through mobile device

## Requirements

Installation instructions.  IGSN-Register is a [Django](http://www.djangoproject.com) app.  Installing Django is outside of the scope of this README.  Follow the instructions for installing Django for your system.  Then:

 * Clone this repository into your Django project
 * Rename the repository directory to `sesar_mobile` (this is for historical reasons, but code imports depend upon it being this name)
 * Edit `settings.py` and add `sesar_mobile` to the `INSTALLED_APPS` list at the end of the list.
 * Edit the `urls.py` for your Django project and add `sesar_mobile.urls` in at the appropriate point (see Django documentation for more details).  

Follow these instructions within your Django project directory to install the app:
 
     $ pip install lxml # requires libxml development packages be installed on your Linux distribution
     $ pip install requests
     $ pip install geojson
     $ python manage.py migrate
     $ python manage.py collectstatic # answer yes to the prompt
    
Now you should be able to start your Django server and run the application.  This will create a new endpoint at the URL you specified that serves up the mobile app and does back-end processing to authenticate and validate IGSN requests.



