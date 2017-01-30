"""

"""
# ============================================================================
# necessary imports
# ============================================================================
import json
import unittest

from flask_sqlalchemy import SQLAlchemy
from flask_fixtures import FixturesMixin

from issuetracker import app
from issuetracker.models import db, Issue, User


# ============================================================================
# load application configs from test configs file
# ============================================================================
app.config.from_object('issuetracker.testconfig')



# ============================================================================
# test class
# ============================================================================
class TestIssueTracker(unittest.TestCase, FixturesMixin):
    fixtures = ['data.json']
    testclient = app.test_client()
    app = app
    db = db
    db.app = app
    db.init_app(app)

    def setUp(self):
        self.issues = Issue.query.all()
        self.sample_data = {
            "summary": "New Test Issue",
            "description": "New Desc",
            "priority": "low",
            "department": "Finance",
            "in_progress": False,
            "status": "open"
        }

    def test_issues_count(self):
        self.assertEqual(len(self.issues), 6)

    def test_closed_issues_count(self):
        self.assertEqual(Issue.query.filter_by(status="closed").count(), 2)

    def test_issue_serialization_keys(self):
        issue_dict = self.issues[0].serialize()
        keys = ["created_at", "id", "summary", "description", "priority",
                "department", "in_progress", "status", "comments"]
        for key in keys:
            self.assertIn(key, issue_dict)

    def test_issue_serialization_type(self):
        issue_dict = self.issues[0].serialize()
        self.assertIsInstance(issue_dict, dict)

    def test_issue_delete(self):
        issue_id = self.issues[0].id
        self.issues[0].delete()

        self.assertIsNone(Issue.query.get(issue_id))

    def test_issue_save(self):
        new_issue = Issue(**self.sample_data)
        new_issue.save()

        self.assertIsNotNone(Issue.query.filter_by(summary=self.sample_data["summary"]).first())

    def test_api_authorization(self):
        response = json.loads(self.testclient.get('/api/issues').get_data(as_text=True))

        self.assertIn("error", response)


if __name__ == '__main__':
    unittest.main()
# ============================================================================
# EOF
# ============================================================================
