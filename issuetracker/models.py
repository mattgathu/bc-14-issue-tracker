"""
File      : models.py
Date      : January, 2017
Author(s) : Matt Gathu <mattgathu@gmail.com>
Desc      : orm models module
"""
# ============================================================================
# necessary imports
# ============================================================================
from datetime import datetime

from flask_user import UserMixin, SQLAlchemyAdapter

from issuetracker import db


# ============================================================================
# database models
# ============================================================================
class User(db.Model, UserMixin):
    """User

    """
    id = db.Column(db.Integer(), primary_key=True)

    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    reset_password_token = db.Column(db.String(), nullable=False, default='')

    email = db.Column(db.String(), nullable=True, unique=True)
    confirmed_at = db.Column(db.DateTime())

    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)

    issues = db.relationship('Issue', backref='user', lazy='dynamic')

    def is_active(self):
        return self.is_enabled

    def serialize(self):
        """serialize user Object

        """
        obj = {
            "username": self.username,
            "is_admin": self.is_admin,
        }

        return obj


class Issue(db.Model):
    """Issue

    """
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    summary = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    priority = db.Column(db.String(), nullable=False)
    department = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    comments = db.relationship('Comment', backref='issue', lazy='dynamic')
    assigned_id = db.Column(db.Integer)
    in_progress = db.Column(db.Boolean(), default=False)

    def serialize(self):
        """serialize Issue instance

        """
        keys = ["created_at", "id", "summary", "description", "priority",
                "department", "in_progress", "status"]
        data_dict = {key: getattr(self, key) for key in keys}

        # ====================================================================
        # add comments
        # ====================================================================
        comments = [cmt.serialize() for
                    cmt in Comment.query.filter_by(issue_id=self.id).all()]
        data_dict["comments"] = comments

        return data_dict

    def save(self):
        """Save issue to database

        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete issue from database

        """
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    """Comment

    """
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))

    text = db.Column(db.String(), nullable=False)

    def serialize(self):
        """serialize Issue instance

        """
        keys = ["text", "id", "issue_id"]
        data_dict = {key: getattr(self, key) for key in keys}

        return data_dict

    def save(self):
        """Save issue to database

        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete issue from database

        """
        db.session.delete(self)
        db.session.commit()


db_adapter = SQLAlchemyAdapter(db, User)
# ============================================================================
# EOF
# ============================================================================
