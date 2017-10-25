# Item Catalog
==============================================

## Description

_This project is served on an installation of a Linux distribution on a virtual machine - Amazon Lightsail._

> In this project we develop a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. Learn when to properly use the various HTTP methods available to you and how these methods relate to CRUD (create, read, update and delete) operations serve it over our instance of ubuntu created on AWS.

### About Our Project

> This project is a cloned version of the following repository, modified to run on AWS - Lightsail instead of on the local virtual machine(vagrant).
https://github.com/Christianq010/fsnd_Item-Catalog

### *Item Catalog*
* We use an Object-Relational Mapping (ORM) layer - SQLAlchemy to interact with our database.
* `GET` and `POST` requests that translate to CRUD operations.
* Using the Flask framework for development of our application.

## Setting up our project to run on our Ubuntu server

> A detailed description of the steps taken to set up our Ubuntu server can be found here - 
https://github.com/Christianq010/fsnd_linux_config_aws

> These steps include 
  > Creating our .wsgi file, 
  > Installing our virtual environment(venv), flask and other dependencies. 
  > Installing and configuring our PostgreSQL database.
  > Configure / Enable a new virtual host (.conf file)


## Main Changes made to our Item Catalog Project.

* Rename project.py to __init__.py `mv application.py __init__.py`
* Refactor the following files - `__init__.py`,`database_setup.py`,`data.py` to contain our new database connection.
```python
engine = create_engine('postgresql://catalog:123456@localhost/catalog')
```
* Include the full file path on any code using the `.open` method.
```python
app_id = json.loads(open('/var/www/FlaskApp/FlaskApp/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
```
### Update Google / Facebook Sign in Info
* For our [Google Log in](https://console.developers.google.com/apis/credentials/)
* From Credentials from the menu on the left.
* Create an OAuth 2.0 Client ID.
* Choose Web application.
   * Add to our Authorized Javascript origins
   ```
   http://35.154.1.22
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com
   ```
   * Add to our Authorized redirect URIs
   ```
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com/catalog 
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com/login 
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com/gconnect 
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com/gdisconnect
   ```
   * Download the new client_secrets.json file and update our `/var/www/FlaskApp/FlaskApp/client_secret.json` with its contents.

* For our [Facebook Log in](https://developers.facebook.com/apps/)
   * On App, go to our Facebook Login Settings and save the following in the Valid OAuth redirect URIs
   ```
   http://35.154.1.22
   http://35.154.1.22/login
   http://35.154.1.22/catalog
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com/catalog 
   http://ec2-35-154-1-22.ap-south-1.compute.amazonaws.com/login
   ```
   * Add your relevant APP ID to the Facebook Log in Script in `login.html`.
   * Set the APP ID and APP Secret in the `fb_client_secrets.json` file.


## API Endpoints
* Show all Catalog names in JSON - `/catalog/JSON`.
* Show Items in Specific Catalog Page in JSON - `/catalog/<int:category_id>/items/JSON`
* Show individual Items in the URL in JSON - `/catalog/<int:category_id>/items/<int:menu_id>/JSON`


### Resources
* Refactor Code to Python PEP 8 style guide
  * http://pep8online.com/checkresult
  * https://stackoverflow.com/questions/10739843/how-should-i-format-a-long-url-in-a-python-comment-and-still-be-pep8-compliant
  * https://stackoverflow.com/questions/1874592/how-to-write-very-long-string-that-conforms-with-pep8-and-prevent-e501
  * https://stackoverflow.com/questions/40003378/pep8-error-in-import-line-e501-line-too-long
