"""
File      : views.py
Date      : January, 2017
Author(s) : Matt Gathu <mattgathu@gmail.com>
Desc      : flask views module
"""
# ============================================================================
# necessary imports
# ============================================================================
from flask import request, jsonify, abort, make_response, render_template
from flask import redirect, url_for
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
    """get currently logged in user """
    return jsonify({"user": current_user.serialize()})

@app.route('/api/logout')
def logout_current_user():
    """log out current user """
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/users')
def get_all_users():
    users = [user.serialize() for user in models.User.query.all()]

    return jsonify({"users": users})

# ============================================================================
# issues api
# ============================================================================
@app.route('/api/issues', methods=['GET'])
def get_issues():
    """fetch issues based on user"""
    issues = []
    if current_user.is_admin:
        issues = [issue.serialize() for issue in reversed(models.Issue.query.all())]
    else:
        issues = [issue.serialize() for issue in
                  reversed(models.Issue.query.filter_by(user_id=current_user.id).all())]

    return jsonify({"issues": issues})


@app.route('/api/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    """fetch issue of id issue_id """
    issue = models.Issue.query.get(issue_id)
    if not issue:
        abort(404)
    return jsonify({'issue': issue.serialize()})

@app.route('/api/issues', methods=['POST'])
def create_issue():
    """create a new issue """
    # ========================================================================
    # check json data, form data and url encoded data (fuck polymer)
    # ========================================================================
    if not request.json and not request.form and not request.args:
        abort(400)

    # ========================================================================
    # aggregate into a dictionary
    # ========================================================================
    if request.form:
        keys = ["summary", "description", "low", "medium", "high", "department", "status"]
        data_dict = {key: request.form.get(key) for key in keys if key in request.form}
    elif request.json:
        data_dict = request.json
    elif request.args:
        keys = ["summary", "description", "low", "medium", "high", "department", "status"]
        data_dict = {key: request.args.get(key) for key in keys if key in request.args}
    # ========================================================================
    # rename keys
    # ========================================================================
    for key in ("low", "medium", "high"):
        if key in data_dict:
            data_dict["priority"] = key
            data_dict.pop(key)
    # ========================================================================
    # add user id
    # ========================================================================
    data_dict['user_id'] = current_user.id
    # create and save new issue
    new_issue = models.Issue(**data_dict)
    new_issue.save()

    return jsonify({"issue": new_issue.serialize()})


@app.route('/api/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    """update issue of id issue_id """
    issue = models.Issue.query.get(issue_id)
    if not issue:
        abort(404)
    data_dict = request.json

    # ========================================================================
    # if data not passed as json try getting it from url parameters
    # ========================================================================
    if not data_dict:
        keys = ["summary", "description", "low", "medium", "high", "department", "in_progress", "status"]
        data_dict = {key: request.args.get(key) for key in keys if key in request.args}
    for key in ("low", "medium", "high"):
        if key in data_dict:
            data_dict["priority"] = key
            data_dict.pop(key)

    issue.summary = data_dict.get('summary', issue.summary)
    issue.description = data_dict.get('description', issue.description)
    issue.priority = data_dict.get('priority', issue.priority)
    issue.department = data_dict.get('department', issue.department)
    issue.in_progress = data_dict.get('in_progress', issue.in_progress)
    issue.status = data_dict.get('status', issue.status)
    issue.save()

    return jsonify({'issue': issue.serialize()})


@app.route('/api/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    """delete issue of id issue_id """
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
    """fetch all comments of an issue """
    comments = [comment.serialize() for comment in
                models.Comment.query.all() if comment.issue_id == issue]

    return jsonify({"comments": comments})


@app.route('/api/comments', methods=['POST'])
def create_comment():
    """create a new commentInput """
    if not request.json and not request.form and not request.args:
        abort(400)
    #=========================================================================
    # aggregate into a dictionary
    #=========================================================================
    if request.form:
        keys = ["issue_id", "text"]
        data_dict = {key: request.form.get(key) for key in keys if key in request.form}
    elif request.json:
        data_dict = request.json
    elif request.args:
        keys = ["issue_id", "text"]
        data_dict = {key: request.args.get(key) for key in keys if key in request.args}

    # ========================================================================
    # add user id
    # ========================================================================
    data_dict['user_id'] = current_user.id

    new_issue = models.Comment(**data_dict)
    new_issue.save()

    return jsonify({"issue": new_issue.serialize()})


# ============================================================================
# error handler
# ============================================================================
@app.errorhandler(404)
def not_found(error):
    """404 error handler """
    return make_response(jsonify({'error': '{}'.format(error)}), 404)


# ============================================================================
# one signal js libraries
# ============================================================================
@app.route('/OneSignalSDKUpdaterWorker.js')
def get_onesignal_updater():
    return app.send_static_file('OneSignalSDKUpdaterWorker.js')

@app.route('/OneSignalSDKWorker.js')
def get_onesignal_worker():
    return app.send_static_file('OneSignalSDKWorker.js')

@app.route('/manifest.json')
def get_app_manifest():
    return app.send_static_file('manifest.json')

# ============================================================================
# EOF
# ============================================================================
