from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalogitems.db')
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


# Items for Electronics
electronics = Category(name="Electronics")

session.add(electronics)
session.commit()


item1 = Item(name="TVs", description="Television is a telecommunication medium used for transmitting moving images in monochrome, or in color, and in two or three dimensions and sound.",
                    category=electronics)

session.add(item1)
session.commit()

item2 = Item(name="Computers", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                    category=electronics)

session.add(item2)
session.commit()

item3 = Item(name="Speakers / Audio Devices", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                    category=electronics)

session.add(item3)
session.commit()

item4 = Item(name="Cameras", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                    category=electronics)

session.add(item4)
session.commit()


# Menu for Phones
phones_tablets = Category(name="Phones and Tablets")

session.add(phones_tablets)
session.commit()

item1 = Item(name="iPhone", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                    category=phones_tablets)

session.add(item1)
session.commit()




print "added items!"
