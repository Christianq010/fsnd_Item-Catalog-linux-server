import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/fsnd_catalog_project/fsnd_Item-Catalog-linux-server/")

from fsnd_Item-Catalog-linux-server import app as application
<<<<<<< HEAD
application.secret_key = 'super_secret_key'
=======
application.secret_key = 'super_secret_key'
>>>>>>> 8503587c9bac4771736e535885a7e9012d47135d
