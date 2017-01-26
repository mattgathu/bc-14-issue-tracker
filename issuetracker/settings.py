"""
File      : settings.py
Date      : January, 2017
Author(s) : Matt Gathu <mattgathu@gmail.com>
Desc      : flask app settings module
"""
# ============================================================================
# necessary imports
# ============================================================================
import os

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///../sqlite.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
USER_SEND_REGISTERED_EMAIL = False
USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = True
TEMPLATES_AUTO_RELOAD = True
# ============================================================================
# EOF
# ============================================================================
