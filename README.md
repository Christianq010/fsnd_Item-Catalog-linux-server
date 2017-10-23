# Item Catalog
==============================================

## Description

> This repository contains a Web application that queries a database and then dynamically generates complete web pages and API endpoints.

_This project is served on an installation of a Linux distribution on a virtual machine - Amazon Lightsail._

> In this project we develop a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. Learn when to properly use the various HTTP methods available to you and how these methods relate to CRUD (create, read, update and delete) operations serve it over our instance of ubuntu created on AWS.

### About Our Project

> This project is a cloned version of the following repository, modified to run on AWS - Lightsail instead of on the local machine.
https://github.com/Christianq010/fsnd_Item-Catalog


#### Setting up our project to run on our Ubuntu server
* Create a catalog.wsgi file, with the following contents:
 ```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/fsnd_catalog_project/fsnd_Item-Catalog-linux-server/")

from catalog import app as application
application.secret_key = 'super_secret_key'
 ```
* Rename project.py to __init__.py `mv application.py __init__.py`

### Running the Database
* The PostgreSQL database server will automatically be started inside the VM.
 * Run `psql` inside the VM command-line tool to access it and run SQL statements: eg. `select * from table_name;`
* Populate the database with some dummy data by running `python data.py` inside the VM.


### Create Google Client ID & Secret
* Create and then Go to your app's page in the Google APIs Console — https://console.developers.google.com/apis
* From Credentials from the menu on the left.
* Create an OAuth 2.0 Client ID.
* Choose Web application.
* You can then set the authorized JavaScript origins to `http://localhost:5000`.

### Create Facebook Client and Secret
* Create and then Go to your app's page in the Facebook Developers Console — https://developers.facebook.com/apps/
* Go to Settings from the menu on the left and select Add Product.
* Create Facebook Log in, configure Client OAuth Settings and Valid OAuth redirect URIs (http://localhost:5000) etc and save changes.
* Add your relevant APP ID to the Facebook Log in Script in `login.html`.
* Set the APP ID and APP Secret in the `fb_client_secrets.json` file.

### API Endpoints
* Show all Catalog names in JSON - `/catalog/JSON`.
* Show Items in Specific Catalog Page in JSON - `/catalog/<int:category_id>/items/JSON`
* Show individual Items in the URL in JSON - `/catalog/<int:category_id>/items/<int:menu_id>/JSON`


### Resources
* Udacity FSND Webcast on setting up Vagrant - https://www.youtube.com/watch?v=djnqoEO2rLc
* Refactor Code to Python PEP 8 style guide
  * http://pep8online.com/checkresult
  * https://stackoverflow.com/questions/10739843/how-should-i-format-a-long-url-in-a-python-comment-and-still-be-pep8-compliant
  * https://stackoverflow.com/questions/1874592/how-to-write-very-long-string-that-conforms-with-pep8-and-prevent-e501
  * https://stackoverflow.com/questions/40003378/pep8-error-in-import-line-e501-line-too-long
