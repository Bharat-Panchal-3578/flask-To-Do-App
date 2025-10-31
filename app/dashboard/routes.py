from . import dashboard_bp
from flask import render_template

@dashboard_bp.route('/tasks')
def dashboard():
    return render_template('tasks.html',show_logout=True)