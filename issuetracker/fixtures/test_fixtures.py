"""

"""
# ============================================================================
# necessary imports
# ============================================================================
import unittest

from .. import app
from ..models import db, Issue

from flask.ext.fixtures import FixturesMixin

# ============================================================================
# initialize the fixtures mixin class
# ============================================================================
FixturesMixin.init_app(app, db)

# ============================================================================
# test class
# ============================================================================
class TestIssueTracker(unittest.TestCase, FixturesMixin):
    fixtures = ['data.json']

    def test_issues(self):
        issues = Issue.query.all()
        assert len(issues) == Issue.query.count() == 4

if __name__ == '__main__':
    unittest.main()
# ============================================================================
# EOF
# ============================================================================
