"""

"""
# ============================================================================
# necessary imports
# ============================================================================
from email.utils import formatdate

from flask import request, jsonify, abort, make_response, render_template, redirect, url_for
from flask_user import login_required
from flask_user import current_user
from flask_login import logout_user

from issuetracker import app, models


# ============================================================================
# index view
# ============================================================================
@app.route('/', methods=['GET'])
@login_required
def index():
    """Index view"""

    return render_template("index.html")


# ============================================================================
# user api
# ============================================================================
@app.route('/api/currentuser')
def get_current_user():
    return jsonify({"user": current_user.serialize()})

@app.route('/api/logout')
def logout_current_user():
    logout_user()
    return redirect(url_for('index'))

# ============================================================================
# issues api
# ============================================================================
@app.route('/api/issues', methods=['GET'])
def get_issues():
    issues = [issue.serialize() for issue in models.Issue.query.all()]
    return jsonify({"issues": issues})


@app.route('/api/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = models.Issue.query.get(issue_id)
    if not issue:
        abort(404)
    return jsonify({'issue': issue.serialize()})

@app.route('/api/issues', methods=['POST'])
def create_issue():
    # check json data, form data and url encoded data (fuck polymer)
    if not request.json and not request.form and not request.args:
        abort(400)

    # aggregate into a dictionary
    if request.form:
        keys = ["summary", "description", "low", "medium", "high","department", "status"]
        data_dict = {key: request.form.get(key) for key in keys if key in request.form}
    elif request.json:
        data_dict = request.json
    elif request.args:
        keys = ["summary", "description", "low", "medium", "high","department", "status"]
        data_dict = {key: request.args.get(key) for key in keys if key in request.args}

    # rename keys
    for key in ("low", "medium", "high"):
        if key in data_dict:
            data_dict["priority"] = key
            data_dict.pop(key)
    # create and save new issue
    new_issue = models.Issue(**data_dict)
    new_issue.save()

    return jsonify({"issue": new_issue.serialize()})

@app.route('/api/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    issue = models.Issue.query.get(issue_id)
    if not issue:
        abort(404)
    data_dict = request.json

    # if data not passed as json try getting it from url parameters
    if not data_dict:
        keys = ["summary", "description", "low", "medium", "high","department"]
        data_dict = {key: request.args.get(key) for key in keys if key in request.args}
    for key in ("low", "medium", "high"):
        if key in data_dict:
            data_dict["priority"] = key
            data_dict.pop(key)

    issue.summary = data_dict.get('summary', issue.summary)
    issue.description = data_dict.get('description', issue.description)
    issue.priority = data_dict.get('priority', issue.priority)
    issue.department = data_dict.get('department', issue.department)
    issue.save()

    return jsonify({'issue': issue.serialize()})

@app.route('/api/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    issue = models.Issue.query.get(issue_id)
    if not issue:
        abort(404)

    issue.delete()

    return jsonify({'result': True})


# ============================================================================
# comments api
# ============================================================================
@app.route('/api/comments/<int:issue>', methods=['GET'])
def get_comments(issue):
    comments = [comment.serialize() for comment in
                models.Comment.query.all() if comment.issue_id == issue]

    return jsonify({"comments": comments})


@app.route('/api/comments', methods=['POST'])
def create_comment():
    if not request.json and not request.form and not request.args:
        abort(400)

    # aggregate into a dictionary
    if request.form:
        keys = ["issue_id", "text"]
        data_dict = {key: request.form.get(key) for key in keys if key in request.form}
    elif request.json:
        data_dict = request.json
    elif request.args:
        keys = ["issue_id", "text"]
        data_dict = {key: request.args.get(key) for key in keys if key in request.args}

    new_issue = models.Comment(**data_dict)
    new_issue.save()

    return jsonify({"issue": new_issue.serialize()})


# ============================================================================
# error handler
# ============================================================================
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
# ============================================================================
# EOF
# ============================================================================
