from flask import Blueprint, render_template, jsonify, current_app as app
from datetime import datetime

views = Blueprint('Views', __name__, url_prefix='/')

@views.route('/')
def index():
    # Render the HTML page
    return render_template('index.html')

@views.route('/log_entries')
def log_entries():
    data = app.db.find().sort('timestamp', -1)

    formatted_data = []
    for entry in data:
        timestamp = datetime.fromisoformat(entry.get('timestamp')).strftime('%d %b %Y - %I:%M %p UTC')
        if entry.get('action') == 'pushed':
            formatted_data.append(f"{entry.get('author')} {entry.get('action')} to {entry.get('to_branch')} on {timestamp}")
        elif entry.get('action') == 'submitted a pull request':
            formatted_data.append(f"{entry.get('author')} {entry.get('action')} from {entry.get('from_branch')} to {entry.get('to_branch')} on {timestamp}")
        elif entry.get('action') == 'merged branch':
            formatted_data.append(f"{entry.get('author')} {entry.get('action')} {entry.get('from_branch')} to {entry.get('to_branch')} on {timestamp}")

    return jsonify(entries=formatted_data)
