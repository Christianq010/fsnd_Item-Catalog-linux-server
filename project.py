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


# app.route('/') - is python decorator - when browser uses URL, the function specific to that URL gets executed

# Show entire Catalog
@app.route('/')
@app.route('/catalog/')
def showCategory():
    categories = session.query(Category).all()
    return render_template('category.html', categories=categories)


# Create new Category
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
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
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


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

