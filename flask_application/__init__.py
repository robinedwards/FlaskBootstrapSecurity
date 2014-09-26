import os
import sys
import logging

from flask import Flask
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.cache import Cache
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_bootstrap import Bootstrap

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))


app = Flask(
    __name__,
    template_folder=os.path.join(FLASK_APP_DIR, '..', 'templates'),
    static_folder=os.path.join(FLASK_APP_DIR, '..', 'static')
)

#  Config
app.config.from_object('flask_application.config.app_config')
app.logger.info("Config: %s" % app.config['ENVIRONMENT'])

#  Logging
logging.basicConfig(
    level=app.config['LOG_LEVEL'],
    format='%(asctime)s %(levelname)s: %(message)s '
           '[in %(pathname)s:%(lineno)d]',
    datefmt='%Y%m%d-%H:%M%p',
)

#  Email on errors
if not app.debug and not app.testing:
    import logging.handlers
    mail_handler = logging.handlers.SMTPHandler(
        'localhost',
        os.getenv('USER'),
        app.config['SYS_ADMINS'],
        '{0} error'.format(app.config['SITE_NAME']),
    )
    mail_handler.setFormatter(logging.Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
    '''.strip()))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    app.logger.info("Emailing on error is ENABLED")
else:
    app.logger.info("Emailing on error is DISABLED")

# Bootstrap
Bootstrap(app)

# Assets
assets = Environment(app)
# Ensure output directory exists
assets_output_dir = os.path.join(FLASK_APP_DIR, '..', 'static', 'gen')
if not os.path.exists(assets_output_dir):
    os.mkdir(assets_output_dir)

# Email
mail = Mail(app)

# Memcache
app.cache = Cache(app)

# Business Logic
# http://flask.pocoo.org/docs/patterns/packages/
# http://flask.pocoo.org/docs/blueprints/

from flask_application.controllers.frontend import frontend
app.register_blueprint(frontend)

app.db = SQLAlchemy(app)

from flask_application.models import User, Role
user_datastore = SQLAlchemyUserDatastore(app.db, User, Role)

# Setup Flask-Security
security = Security(app, user_datastore)

from flask_application.controllers.admin import admin
app.register_blueprint(admin)
