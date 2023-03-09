
import os
from sys import exit

from flask_minify import Minify

from application2 import create_app
from application2.config import config_dict

# WARNING: Don't run with debug turned on in production!
# DEBUG = (os.getenv('DEBUG', 'False') == 'True')
DEBUG = True

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG))
    app.logger.info('FLASK_ENV        = ' + os.getenv('FLASK_ENV'))
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT)

if __name__ == "__main__":
    app.run()
