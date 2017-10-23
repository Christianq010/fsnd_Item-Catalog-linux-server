import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/fsnd_catalog_project/fsnd_Item-Catalog-linux-server/")

from fsnd_Item-Catalog-linux-server import app as application
application.secret_key = 'super_secret_key'