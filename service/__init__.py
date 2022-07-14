import os
import logging
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import service.models as models

app = Flask(__name__, template_folder='templete')
app.config.from_object("config")

try:
    models.init_db(app)
except Exception  as error:
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

print('Setting up logging for {}...'.format(__name__))
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.propagate = False
    # Make all log formats consistent
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
    )
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)
    app.logger.info("Logging handler established")

app.logger.info('Logging established')
app.logger.info("**********************************************")
app.logger.info(" P R O D U C T   S E R V I C E   R U N N I N G")
app.logger.info("**********************************************")

from service import routes

