# Creating and Testing out our first Flask application

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# New imports for Login Session / Google Log in
from flask import session as login_session
import random, string

# Imports for GConnect
# store OAuth2 parameters
from oauth2client.client import flow_from_clientsecrets
# Catch error in case we run into error during OAuth
from oauth2client.client import FlowExchangeError
# comprehenive python http2 client library
import httplib2
# convert in memory python objects to JSON
import json
# converts our returned function to a real response method sent to our client
from flask import make_response
# apache library written in python
import requests

# For our Google Login
CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Item Catalog'


# Create an instance of this class with __name__ as the running argument
app = Flask(__name__)

# create Session and connect to DB
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Note: app.route('/') - is python decorator - when browser uses URL, the function specific to that URL gets executed

# =================================================================
# ------------------------ Login / Signup ---------------------------
# =================================================================


# Create a state token to prevent request
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)for x in xrange(32))
    login_session['state'] = state
    # Show our validation in a string - return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# ------------------------------ Google Log in ---------------------------------- /

# Server side code accepting token
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token (client sent to server matches server sent to client)
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        login_session['credentials'] = credentials
        response = make_response(json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # When you log in via Gmail, create new user_id if does not exist in DB
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Welcome, You are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Use login_session to create a New User when signed in
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Pass a user.id into this method return a User object with the associated id number from the DB
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Take am email address and return a user.id if the email exists
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For some reason token was Invalid
        response = make_response(json.dumps('Failed to revoke token for user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# ---------------------------------- Facebook Log in --------------------------------- /

# Log in using facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    # strip expire tag from access token
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    # sys.stdout = open('output.logs', 'w')
    # print (data["name"]) # Nothing appears below
    # print (data["email"]) # Nothing appears below
    # print (data["id"]) # Nothing appears below
    # sys.stdout = sys.__stdout__ # Reset to the standard output
    # open('output.logs', 'r').read()
    # return "OK"
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Ok"

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Disconnect from Facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]


# Global disconnect function
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        flash("You've been successfully logged out.")
        return render_template('logout.html')
    else:
        flash("You weren't signed in.")
        return render_template('logout.html')

# =================================================================
# -------------------------- Catalog ------------------------------
# =================================================================

# Show entire Catalog
@app.route('/')
@app.route('/catalog/')
def showCategory():
    categories = session.query(Category).all()
    users = session.query(User).all()
    if 'username' not in login_session:
        return render_template('publicCatalog.html',categories=categories, users=users)
    return render_template('category.html', categories=categories)


# Create new Category
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
        # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Add Catalog")
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template('newCategory.html')

# Edit an existing Category
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
        # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Edit Catalog")
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategory'))
    else:
            return render_template('editCategory.html', category=editedCategory)

# Delete an existing Category
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
        # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Delete Catalog")
        return redirect('/login')
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


# =================================================================
# ---------------------------- Catalog Items ----------------------
# =================================================================

# Show a Catalog Item
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def catalogItemList(category_id):
    # Add entire catalog and items to page
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    # Render templates in folder and pass our queries above as arguments for our template
    return render_template('item.html', category=category, items=items)

# Add a new Catalog Item
@app.route('/catalog/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newItem(category_id):
    # Look for POST request
    if request.method == 'POST':
        # extract 'name' from our form using request.form
        newItem = Item(name=request.form['name'],category_id=category_id)
        session.add(newItem)
        session.commit()
        # Our flask message
        flash("New item for category created!")
        return redirect(url_for('catalogItemList', category_id=category_id))
    # If a POST request was not received
    else:
        return render_template('newItem.html', category_id=category_id)

# Edit an existing Catalog Item name
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('catalogItemList', category_id=category_id))
    else:
        return render_template(
            'editItem.html', category_id=category_id, item_id=item_id, item=editedItem)

# Delete an existing Catalog Item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('catalogItemList', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# ======================================================================================
# ---------------------------------- JSON Endpoints ------------------------------------ 
# ======================================================================================

# Show Items in Catalog Page in JSON
@app.route('/catalog/<int:category_id>/items/JSON')
def catalogItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    # Return jsonify class and use loop to serialize all our DB entries
    return jsonify(Items=[i.serialize for i in items])

# Show individual Items in the URL in JSON
@app.route('/catalog/<int:category_id>/items/<int:menu_id>/JSON')
def itemJSON(category_id, menu_id):
    item = session.query(Item).filter_by(id=menu_id).one()
    return jsonify(Item=item.serialize)

# Show all Catalog names in JSON
@app.route('/catalog/JSON')
def catalogJSON():
    catalog = session.query(Category).all()
    return jsonify(catalog=[r.serialize for r in catalog])





# if executed via python interpreter run this function
if __name__ == '__main__':
    # Secret key for flask message flashing (sessions)
    app.secret_key = 'super_secret_key'
    # reload server when code change detected and run debug in browser
    app.debug = True
    # use to run local server with our application
    # special config for vagrant machine by making our host publicly available
    app.run(host='0.0.0.0', port=5000)

