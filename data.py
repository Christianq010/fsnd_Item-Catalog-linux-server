from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

import json

engine = create_engine('postgresql://catalog:123456@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


category_json = json.loads("""{
  "Categories": [
    {
      "name": "Coffee"
    },
    {
      "name": "Tea"
    },
    {
      "name": "Bean"
    },
    {
      "name": "Tablet"
    }
  ]
}""")

# Add Categories
for e in category_json['Categories']:
  category_input = Category(
    name=str(e['name'])
    )
  session.add(category_input)
  session.commit()
print "added items!"
