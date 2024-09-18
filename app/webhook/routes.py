from flask import Blueprint, request, jsonify, current_app as app
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def handle_push_event(data):
    """Handle a push event from GitHub."""
    author = data.get('pusher', {}).get('name')
    to_branch = data.get('ref', '').split('/')[-1]
    commit_hash = data.get('head_commit', {}).get('id')
    return {
        'request_id': commit_hash,
        'author': author,
        'action': 'pushed',
        'from_branch': None,
        'to_branch': to_branch,
        'timestamp': datetime.now().isoformat()
    }

def handle_pull_request_event(data):
    """Handle a pull request event from GitHub."""
    action_type = data.get('action')
    author = data.get('sender', {}).get('login')
    from_branch = data.get('pull_request', {}).get('head', {}).get('ref')
    to_branch = data.get('pull_request', {}).get('base', {}).get('ref')
    pr_id = data.get('pull_request', {}).get('id')

    if action_type == 'opened':
        action_message = 'submitted a pull request'
    elif action_type == 'closed':
        action_message = 'merged branch' if data.get('pull_request', {}).get('merged') else 'closed pull request'
    else:
        action_message = 'performed an action on pull request'

    return {
        'request_id': pr_id,
        'author': author,
        'action': action_message,
        'from_branch': from_branch,
        'to_branch': to_branch,
        'timestamp': datetime.now().isoformat()
    }

@webhook.route('/receiver', methods=['POST'])
def receiver():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        event_data = handle_push_event(data)
    elif event_type == 'pull_request':
        event_data = handle_pull_request_event(data)
    else:
        return jsonify({"status": "error", "message": "Unsupported event type"}), 400

    # Save to MongoDB
    app.db.insert_one(event_data)

    return jsonify({"status": "success"}), 200
