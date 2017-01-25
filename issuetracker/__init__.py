"""

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

from issuetracker.utils import random_string
# ============================================================================
# flask app initialization
# ============================================================================
app = Flask(__name__)
app.secret_key = random_string()

# ============================================================================
# load application configs from settings file
# ============================================================================
app.config.from_object('issuetracker.settings')

# ============================================================================
# setup application extensions
# ============================================================================
db = SQLAlchemy()
db.app = app
db.init_app(app)


import issuetracker.views
from issuetracker.models import *

user_manager = UserManager(db_adapter, app)
# ============================================================================
# EOF
# ============================================================================
