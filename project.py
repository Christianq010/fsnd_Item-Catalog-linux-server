# Creating and Testing out our first Flask application

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Create an instance of this class with __name__ as the running argument
app = Flask(__name__)

# create Session and connect to DB
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

"""

# Show Restaurant menu Page in JSON
@app.route('/catalog/<int:catalog_id>/items/JSON')
def restaurantMenuJSON(catalog_id):
    restaurant = session.query(Restaurant).filter_by(id=catalog_id).one()
    items = session.query(MenuItem).filter_by(catalog_id=catalog_id).all()
    # Return jsonify class and use loop to serialize all our DB entries
    return jsonify(MenuItems=[i.serialize for i in items])


# Show individual menuItems in the URL in JSON
@app.route('/catalog/<int:catalog_id>/items/<int:menu_id>/JSON')
def menuItemJSON(catalog_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


# Show all restaurants in JSON
@app.route('/catalog/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])

"""

# app.route('/') - is python decorator - when browser uses URL, the function specific to that URL gets executed

# Show all Restaurants
@app.route('/')
@app.route('/catalog/')
def showCategory():
    categories = session.query(Category).all()
    return render_template('category.html', categories=categories)


"""

# Create new Restaurant
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# Edit an existing Restaurant
@app.route('/catalog/<int:catalog_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(catalog_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            return redirect(url_for('showRestaurants'))
    else:
            return render_template('editRestaurant.html', restaurant=editedRestaurant)


# Delete an existing Restaurant
@app.route('/catalog/<int:catalog_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(catalog_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(url_for('showRestaurants', catalog_id=catalog_id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)

"""

# Show a Restaurant Menu
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def catalogItemList(category_id):
    # Add all restaurants and menu items to page
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    # Render templates in folder and pass our queries above as arguments for our template
    return render_template('item.html', category=category, items=items)


"""

# Add a new Menu Item
@app.route('/catalog/<int:catalog_id>/items/new/', methods=['GET', 'POST'])
def newMenuItem(catalog_id):
    # Look for POST request
    if request.method == 'POST':
        # extract 'name' from our form using request.form
        newItem = MenuItem(name=request.form['name'],catalog_id=catalog_id)
        session.add(newItem)
        session.commit()
        # Our flask message
        flash("New menu item created!")
        return redirect(url_for('restaurantMenu', catalog_id=catalog_id))
    # If a POST request was not received
    else:
        return render_template('newmenuitem.html', catalog_id=catalog_id)


# Edit an existing Menu Item
@app.route('/catalog/<int:catalog_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(catalog_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', catalog_id=catalog_id))
    else:
        return render_template(
            'editmenuitem.html', catalog_id=catalog_id, menu_id=menu_id, item=editedItem)


# Delete an existing Menu Item
@app.route('/catalog/<int:catalog_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(catalog_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('restaurantMenu', catalog_id=catalog_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)

"""

# if executed via python interpreter run this function
if __name__ == '__main__':
    # Secret key for flask message flashing (sessions)
    app.secret_key = 'super_secret_key'
    # reload server when code change detected and run debug in browser
    app.debug = True
    # use to run local server with our application
    # special config for vagrant machine by making our host publicly available
    app.run(host='0.0.0.0', port=5000)

